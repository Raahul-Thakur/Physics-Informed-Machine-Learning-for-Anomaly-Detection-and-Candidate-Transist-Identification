"""Optional CPU autoencoder with target-group validation and early stopping."""

import copy

import numpy as np
from sklearn.model_selection import GroupShuffleSplit


def fit(
    matrix: np.ndarray,
    groups: np.ndarray,
    cfg: dict,
    seed: int,
    split: tuple[np.ndarray, np.ndarray] | None = None,
) -> tuple[dict, np.ndarray]:
    import torch
    from torch import nn

    if len(np.unique(groups)) < 5:
        raise ValueError("Autoencoder requires at least five independent target groups")
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)
    train, valid = (
        split
        if split is not None
        else next(
            GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(
                matrix, groups=groups
            )
        )
    )
    width = matrix.shape[1]
    model = nn.Sequential(
        nn.Linear(width, 64),
        nn.ReLU(),
        nn.Linear(64, 32),
        nn.ReLU(),
        nn.Linear(32, 8),
        nn.ReLU(),
        nn.Linear(8, 32),
        nn.ReLU(),
        nn.Linear(32, 64),
        nn.ReLU(),
        nn.Linear(64, width),
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg["learning_rate"])
    x = torch.tensor(matrix, dtype=torch.float32)
    best, state, stale, history = float("inf"), None, 0, []
    for epoch in range(cfg["epochs"]):
        model.train()
        optimizer.zero_grad()
        loss = ((model(x[train]) - x[train]) ** 2).mean()
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            val = float(((model(x[valid]) - x[valid]) ** 2).mean())
        history.append(dict(epoch=epoch, train_loss=float(loss.detach()), validation_loss=val))
        if val < best:
            best, state, stale = val, copy.deepcopy(model.state_dict()), 0
        else:
            stale += 1
        if stale >= cfg["patience"]:
            break
    if state is None:
        raise ValueError("Autoencoder did not produce a finite validation loss")
    model.load_state_dict(state)
    with torch.no_grad():
        scores = ((model(x) - x) ** 2).mean(dim=1).numpy()
    return dict(
        state_dict=state,
        input_width=width,
        history=history,
        train_indices=train,
        validation_indices=valid,
    ), scores
