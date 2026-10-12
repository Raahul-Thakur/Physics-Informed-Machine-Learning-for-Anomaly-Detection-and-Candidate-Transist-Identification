"""Repository-maintenance helper to generate thin CLI wrappers and inspection notebooks."""

import copy
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WRAPPERS = {
    "download_sample": "download",
    "preprocess": "preprocess",
    "run_bls": "bls",
    "extract_features": "features",
    "train_models": "train",
    "evaluate": "evaluate",
    "generate_figures": "figures",
    "run_pipeline": "all",
    "generate_report": "report",
    "abstract_results": "abstract",
    "injection_recovery": "injection",
}
for name, stage in WRAPPERS.items():
    (ROOT / f"scripts/{name}.py").write_text(
        f'"""Run the {stage} stage; see --help for configuration options."""\n'
        "from tess_anomaly.pipeline import main\n\n"
        f'if __name__ == "__main__":\n    main("{stage}")\n',
        encoding="utf-8",
    )
small = yaml.safe_load((ROOT / "config/small_test.yaml").read_text())
large = copy.deepcopy(small)
large["workspace"] = "experiments/default"
large["data"].update(
    sample_size_planets=300,
    sample_size_false_positive=300,
    sample_size_background=500,
    max_sectors_per_target=2,
    sectors=list(range(1, 14)),
)
(ROOT / "config/default.yaml").write_text(yaml.safe_dump(large, sort_keys=False))
sanity = copy.deepcopy(small)
sanity["workspace"] = "experiments/sanity"
sanity["data"].update(
    sample_size_planets=3,
    sample_size_false_positive=0,
    sample_size_background=0,
    sanity_tics=[25155310, 261136679, 307210830],
)
(ROOT / "config/sanity.yaml").write_text(yaml.safe_dump(sanity, sort_keys=False))
setup = (
    "from pathlib import Path\nimport pandas as pd\nimport numpy as np\n"
    "from tess_anomaly.config import load_config\n"
    'ROOT = Path.cwd()\nif ROOT.name == "notebooks": ROOT = ROOT.parent\n'
    'cfg = load_config(ROOT / "config/small_test.yaml")\n'
)
notebooks = {
    "01_data_exploration": (
        "Catalogue and retained photometry",
        [
            'sample = pd.read_csv(ROOT / "data/catalog/sample.csv")\nsample.groupby("label").size()',
            "sample.head()",
            'import matplotlib.pyplot as plt\nmanifest = pd.read_csv(ROOT / "data/raw/manifest.csv")\n'
            "with np.load(ROOT / manifest.iloc[0].raw_path) as lc:\n"
            '    plt.plot(lc["time"], lc["flux"], ".", ms=1)\n'
            'plt.xlabel("Time [BTJD]"); plt.ylabel("PDCSAP flux [electron/s]")',
        ],
    ),
    "02_bls_analysis": (
        "Independent BLS search and catalogue period checks",
        [
            "from tess_anomaly.bls import search_bls, phase\n"
            'features = pd.read_csv(ROOT / "data/features/features.csv")\n'
            "with np.load(ROOT / features.iloc[0].processed_path) as archive:\n"
            '    curve = dict(archive)\nresult, periodogram = search_bls(curve, cfg["bls"])\nresult',
            'import matplotlib.pyplot as plt\nplt.plot(periodogram["period"], periodogram["power"])\n'
            'plt.xlabel("Period [days]"); plt.ylabel("BLS power")',
            'plt.scatter(phase(curve["time"], result["best_period"], result["transit_epoch"]), curve["flux"], s=1)\n'
            'plt.xlabel("Time from transit [days]"); plt.ylabel("Relative flux")',
            'pd.read_csv(ROOT / "outputs/tables/period_sanity.csv").head(20)',
        ],
    ),
    "03_feature_analysis": (
        "Feature distributions, missingness, correlations and PCA",
        [
            'from tess_anomaly.features import FAMILIES\nfeatures = pd.read_csv(ROOT / "data/features/features.csv")\n'
            'features[FAMILIES["generic"]].describe()',
            'pd.read_csv(ROOT / "outputs/tables/missing_data.csv")',
            'features[FAMILIES["all"]].corr(method="spearman")',
            'from IPython.display import Image, display\ndisplay(Image(filename=str(ROOT / "outputs/figures/pca_projection.png")))',
        ],
    ),
    "04_anomaly_detection": (
        "Fitted anomaly models and transparent rankings",
        [
            'import joblib\nmodels = joblib.load(ROOT / "outputs/models/models.joblib")\nlist(models)',
            'rankings = pd.read_csv(ROOT / "outputs/rankings/ranked_light_curves.csv")\n'
            'rankings.sort_values("ensemble_score", ascending=False).head(20)',
            'models["transform"].columns',
        ],
    ),
    "05_results": (
        "Descriptive results; no assumed ML improvement",
        [
            f'pd.read_csv(ROOT / "outputs/tables/{table}.csv")'
            for table in ["model_performance", "correlations", "ablation_results", "top_candidates"]
        ],
    ),
}
(ROOT / "notebooks").mkdir(exist_ok=True)
for name, (title, cells) in notebooks.items():
    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
        },
        "cells": [
            {
                "cell_type": "markdown",
                "id": "intro",
                "metadata": {},
                "source": [
                    f"# {title}\nRun the CLI experiment first. All calculations live in the package."
                ],
            }
        ],
    }
    for i, source in enumerate([setup] + cells):
        nb["cells"].append(
            {
                "cell_type": "code",
                "id": f"cell-{i}",
                "metadata": {},
                "execution_count": None,
                "outputs": [],
                "source": source.splitlines(keepends=True),
            }
        )
    (ROOT / f"notebooks/{name}.ipynb").write_text(json.dumps(nb, indent=2), encoding="utf-8")
