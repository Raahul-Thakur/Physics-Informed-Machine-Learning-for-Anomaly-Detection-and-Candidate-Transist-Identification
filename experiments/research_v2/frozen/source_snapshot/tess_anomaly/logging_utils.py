"""Persistent stage and failure logging."""

import logging
from pathlib import Path


def configure(root: Path) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(root / "outputs/logs/pipeline.log", encoding="utf-8"),
        ],
        force=True,
    )
    # PDF font embedding emits extensive INFO chatter; retain warnings and errors.
    logging.getLogger("fontTools.subset").setLevel(logging.WARNING)
