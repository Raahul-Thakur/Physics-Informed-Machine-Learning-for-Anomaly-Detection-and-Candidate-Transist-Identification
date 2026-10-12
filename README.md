# TESS anomaly research

**Physics-Informed Machine Learning for Anomaly Detection and Candidate Transit Identification in TESS Light Curves**

This repository asks whether anomaly scores add useful prioritisation information to conventional Box Least Squares (BLS) transit searches. The hypothesis is that transit morphology and approximate physical consistency features may improve known-host recovery relative to generic variability features. An improvement is **not** assumed. All reported numbers are calculated from downloaded photometry and catalogue snapshots.

The [submitted abstract](RESEARCH_GUIDE.md#submitted-research-specification) is preserved verbatim. Here, **physics-informed** means astrophysically motivated feature engineering, not physical equations enforced during training. The [V3 workflow](RESEARCH_GUIDE.md#research-v3) freezes unsupervised IF/novelty-LOF models and a separate semi-supervised label-spreading experiment before evaluating unseen targets. Labels remain excluded from unsupervised fitting. The original pipeline commands below also support the earlier exploratory experiment; they are not the frozen V3 evaluation commands.

The [additional evidence protocol](RESEARCH_GUIDE.md#abstract-evidence-plan) documents completed 14,400-trial injection validation, controlled input interventions, ephemeris checks and a separately locked statistical reference/test cohort. Score explanations concern model behaviour, not astrophysical causation. Ranking percentiles are not p-values; the separate statistical test has an explicit population and assumptions. Recovery includes catalogue candidates, so confirmed/known systems are reported separately. Neither planetary validation nor reduced human review time follows from running this code.

## Install

Python 3.11+ is required. The main experiment runs on a CPU. From this directory:

```powershell
# Windows PowerShell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

```bash
# Linux/macOS
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

The development session may use the sibling environment `../.venv`; it is not part of the portable repository. `requirements.txt` is an alternative editable installation entry point. `requirements-lock.txt`, when present, records the environment actually used for validation. Optional autoencoder: `python -m pip install -e '.[autoencoder]'` and set `models.autoencoder.enabled: true`. Jupyter is only for inspection notebooks.

## Reproduce the small experiment

```bash
python scripts/run_pipeline.py --config config/small_test.yaml --resume
python scripts/abstract_results.py --config config/small_test.yaml
```

The small configuration requests 30 confirmed/known planet or planet-candidate hosts, 30 false-positive/false-alarm hosts, and 50 unlabelled background targets from sectors 1â€“5. Sampling is seeded **before** the photometry is examined. Only targets in the official SPOC light-curve observing manifests for these sectors enter the sampling frame. This improves download availability but is an explicit observing-selection bias. One 120-second SPOC sector is used per target; no labelled quota is filled by inventing rows or relabelling background targets. Runtime and download volume depend on archive latency (typically hundreds of MB, with serial downloads).

The two-minute observing manifests describe product availability, not a magnitude-complete stellar population. The catalogue snapshot evolves upstream; retain `data/catalog/` to reproduce the same sample. A genuinely new sample requires a separate output workspace and optionally `--force` to refresh upstream catalogues.

## Larger experiment and sanity checks

```bash
python scripts/run_pipeline.py --config config/default.yaml --resume
python scripts/run_pipeline.py --config config/sanity.yaml --resume
python scripts/injection_recovery.py --config config/small_test.yaml
python -m pytest -q
ruff check src tests scripts
```

The larger configuration requests 300 planet/candidate hosts, 300 false-positive hosts and 500 controls, up to two sectors each, from sectors 1â€“13. It writes under `experiments/default/`, so it cannot overwrite the small experiment. Catalogue availability may yield fewer hosts, which is logged. The sanity configuration independently searches three known TESS systems in `experiments/sanity/`; catalogue periods are used **only after** BLS has completed. The injection script writes explicitly synthetic ground truth separately and never supplies primary research data.

## Architecture and individual stages

```text
config/                  YAML small, larger and known-system configurations
src/tess_anomaly/
  catalog.py             NASA TOI / ExoFOP / local CSV; MAST sampling manifests
  download.py            Serial Lightkurve/MAST downloads and per-target caches
  preprocessing.py       Quality filtering, segments and masked trend estimation
  bls.py                 Astropy BLS, phase folding and period/harmonic checks
  features.py             Explicit generic, BLS and physical/morphology families
  dataset.py              Training/reference missingness selection and scaling
  anomaly/               Isolation Forest, LOF, optional CPU autoencoder, ensemble
  evaluation.py          Unique-target rankings, recovery, AUCs and correlations
  plots.py               PNG/PDF exploratory and candidate diagnostic figures
  pipeline.py            CLI orchestration, ablations and result-derived reports
  utils.py               Provenance and isolated synthetic validation generators
scripts/                 Thin stage entry points; no hidden scientific code
tests/                   Offline scientific and end-to-end checks
notebooks/               Five inspection notebooks calling package functionality
RESEARCH_GUIDE.md        Methods, workflows, research questions and validation record
data/{catalog,raw,processed,features,cache}/
outputs/{figures,tables,models,rankings,logs}/
```

Each stage can be run independently after its upstream stages:

```bash
python scripts/download_sample.py --config config/small_test.yaml
python scripts/preprocess.py --config config/small_test.yaml
python scripts/run_bls.py --config config/small_test.yaml
python scripts/extract_features.py --config config/small_test.yaml
python scripts/train_models.py --config config/small_test.yaml
python scripts/evaluate.py --config config/small_test.yaml
python scripts/generate_figures.py --config config/small_test.yaml
python scripts/generate_report.py --config config/small_test.yaml
```

`--resume` reuses valid caches. Raw data are retained by default; scientific cache keys include input bytes, processing configuration and package source hash. `--force` refreshes catalogue snapshots and recomputes derived products; Lightkurve can still reuse original FITS downloads. Paths inside a configuration resolve relative to its experiment workspace. A per-target error is logged with a traceback and recorded in a failure CSV; other targets continue. If every target fails, the stage raises an error.

## Data sources and manual fallback

Primary catalogue: [NASA Exoplanet Archive TOI table](https://exoplanetarchive.ipac.caltech.edu/docs/API_TOI_columns.html), queried through [TAP](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html). The API uses `tid`, `tfopwg_disp`, `pl_orbper`, and `st_rad`; do not substitute guessed column names. The fallback is [ExoFOP's downloadable TOI CSV](https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=csv). MAST [sector bulk-download manifests](https://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_ffi-tp-lc-dv.html) provide the observing-selected population. These scripts are parsed as text and **never executed**. Photometry uses [Lightkurve's search/download interface](https://lightkurve.github.io/lightkurve/reference/search.html).

If both catalogue APIs fail, download a TOI CSV manually from one of these sources and set `data.catalog_csv` to its path. Accepted native NASA/ExoFOP headings are mapped in `catalog.py`; a normalized local CSV must contain `tic_id,disposition` and may contain `toi_id,catalog_period,stellar_radius,stellar_mass`. Periods are days, radii solar radii, masses solar masses. Retain a `catalog_source` column with provenance. A `data.background_csv` must contain genuine TIC IDs, and may contain uniformly sourced stellar parameters; known TOIs are excluded before seeded control sampling. No authenticated account is required for these public services.

CP/KP/PC are catalogue-positive for recovery metrics. FP/FA form the false-positive group. Hosts with both positive and false-positive dispositions are excluded as ambiguous; other ambiguous dispositions are not used as labelled negatives. All TOI rows remain available for multi-planet period checks. The row with the lowest TOI ID supplies target metadata, and this choice is documented rather than treated as a unique physical planet model.

## Scientific choices

* Analysis row: one TIC-sector. Metrics: one TIC, taking each method's maximum sector score. With multiple sectors, more observing opportunities can bias maxima; match sector counts in follow-up experiments.
* Raw PDCSAP photometry, errors, quality flags and FITS files are retained. Time is BTJD = BJD_TDB âˆ’ 2457000. Missing errors are represented as missing, never fabricated; completely absent errors trigger unweighted BLS. Partially invalid errors are removed with aligned cadence masks.
* The default quality bitmask is 175. `0` disables quality-bit rejection. Nonfinite/nonpositive flux and invalid measured errors are rejected. There is no flux sigma-clipping that deletes transit dips.
* Default detrending uses a 1.5-day Savitzkyâ€“Golay window within segments separated by gaps exceeding 0.25 day. Three residual-masking iterations protect both positive and negative events while estimating the trend; all retained photometric points remain in the search. Interpolation is confined to trend estimation within a segment. Median normalization and rolling-median alternatives are configurable. Compare windows via injections before interpreting shallow signals.
* BLS searches 0.5â€“12 days, capped at half the actual baseline, with 1â€“4-hour durations. Astropy's duration-based frequency grid uses factor 5 for the initial economical run; reduce it to 1 or below for finer searches. A peak is a search statistic, not a significance-calibrated planet detection. The robust peak statistic is not a false-alarm probability. Under objective `snr`, peak BLS power and depth SNR coincide, so those baselines are redundant by construction; `likelihood` supplies a different power objective.
* Stellar mass is not supplied by the TOI table. Duration-consistency features remain missing unless a real mass is supplied. Both `radius_earth_proxy` and `duration_ratio_proxy` are excluded from ML by default (`models.use_stellar_catalog_features: false`) because stellar information is catalogue-dependent in this initial sample. The values are still extracted where available. Enable them only after obtaining uniformly sourced stellar metadata for all groups; otherwise missingness can reveal the sampling class. Transit-derived radius ratio and morphology remain in the physics feature family. Do not infer mass without an explicitly validated model.
* This is **transductive descriptive outlier detection**: IF/LOF and their feature transform fit the unlabelled observed sample, then rank that sample. It is not a held-out classifier experiment. LOF fit-time scores use `-negative_outlier_factor_`; separate novelty helpers exist for genuinely unseen samples.
* All anomaly scores have higher = more anomalous. Equal-weight percentile ensembles and BLS/anomaly hybrids are fixed in advance. Feature selection is explicit; IDs, sector, class codes and catalogue periods are excluded. Missing-feature thresholds and medians are fitted on the reference population. Ablations independently fit the same fixed procedure to each feature family.

## Generated outputs

| Artifact | Meaning |
|---|---|
| `data/catalog/toi_snapshot.csv` | Original source snapshot, with provenance |
| `data/catalog/normalized_catalog.csv` | All normalized TOI entries, including multi-planet hosts |
| `data/catalog/sample.csv` | Exact requested target sample and labels |
| `data/catalog/tesscurl_sector_*_lc.sh` | Archived MAST observing manifests, parsed only |
| `data/raw/manifest.csv`, `data/raw/*.npz`, `data/raw/mast/` | Successful product metadata, unfiltered arrays and FITS downloads |
| `data/processed/manifest.csv`, `*.npz` | Aligned retained photometry, normalization, trend, detrended flux and segment IDs |
| `data/cache/*_bls.json`, `*_power.npz` | Versioned BLS solutions, periodograms and phase coordinates |
| `data/cache/download_*.csv`, `stage_*.json` | Per-target product caches and content-checked stage completion receipts |
| `data/features/features.csv` | Identifiers, reference labels and interpretable numeric measurements |
| `outputs/models/` | Fitted transform, model bundle, numeric feature matrix and aligned `feature_matrix_rows.csv`; load only trusted joblib files |
| `outputs/rankings/ranked_light_curves.csv` | Scores per TIC-sector; sortable by any method |
| `outputs/rankings/ranked_targets.csv` | One row per TIC with per-method sector maxima |
| `outputs/tables/missing_data.csv` | Missing fractions and selected/dropped feature decisions |
| `summary_statistics.csv`, `group_statistics.csv` | Feature summaries, class score distributions, exploratory Mannâ€“Whitney tests |
| `model_performance.csv` | Top-K catalogue-positive yield/recall, ranks, ROC-AUC and average precision where valid |
| `correlations.csv`, `feature_score_correlations.csv` | Scoreâ€“score and featureâ€“score Spearman correlations with pair counts |
| `ablation_results.csv` | Generic, BLS, morphology/physics, and all-feature ranking comparisons |
| `sector_coverage.csv` | Usable sector counts by reference group; generated with the report |
| `top_candidates.csv` | Highest hybrid-ranked unique targets with full metadata for inspection |
| `period_sanity.csv` | Recovered/catalogue periods and P/2, P, 2P mismatch checks for every available host |
| `pca_loadings.csv`, `pca_coordinates.csv` | PCA directions and per-TIC-sector coordinates in the scaled feature space |
| `injection_recovery.csv`, `injection_truth_*.json` | Optional isolated synthetic validation results and ground truth |
| `outputs/figures/*.png`, `*.pdf` | Correlations, PCA, score distributions, BLS/anomaly scatter and recovery curves |
| `outputs/figures/candidates/` | Raw/detrended photometry, periodogram, folded transit, zoom and metadata per top target |
| `outputs/logs/` | Timestamped logs and explicit per-stage target failure tables |
| `outputs/config_used.yaml`, `run_metadata.json` | Configuration, random seed, package versions, UTC time, Git hash if available and sample IDs |
| `outputs/research_summary.md`, `abstract_results.txt` | Actual calculated results with unavailable metrics explained |

## Interpretation and next experiments

The completed [paper reporting workflow](RESEARCH_GUIDE.md#paper-workflow) preserves the inspected independent result, generates final tables and figures, adds paired target-bootstrap uncertainty, and records a ten-object diagnostic review. Start with `paper/final/manuscript.md`; reproduce into a fresh folder using `python scripts/paper_report.py --reproduce --archive paper/archive_2026-09-16 --output paper/reproduction`. The primary independent result remains hybrid 28/300 versus BLS 33/300 at K=100, with no demonstrated workload reduction.

The implemented [frozen research extension](RESEARCH_GUIDE.md#research-v2) adds target-disjoint evaluation, transit-coherence features, compact training-only redundancy selection, exposure-controlled and search-eligible comparisons, fixed-budget complementary inspection, and paired injections into real photometry. It writes separate experiment outputs and preserves the original descriptive baseline. Follow its commands to acquire new evaluation targets without fitting models on them.

Anomaly â‰  exoplanet; BLS peak â‰  confirmed planet. High scores may reflect eclipsing binaries, stellar variability, instrument systematics, contamination/blending or data quality. Catalogue incompleteness means background stars are not verified negatives. Catalogue-positive yield is not planet purity. Candidate labels are excluded from binary AUCs; CP/KP versus FP/FA AUCs still measure a selected reference sample, not survey completeness. Class balance is imposed by design. Harmonics, correlated noise and multiple comparisons affect interpretation. PCA is an inspection tool, not proof of class separation.

A known-host catalogue label does not establish that its planet transited during the selected sector. Some catalogue periods and durations are outside the initial search grid, and the pipeline searches only the strongest box signal. Multiple planets, non-observed events and period limits can therefore reduce known-host recovery even when the code is functioning correctly. Unweighted BLS statistics should not be compared quantitatively to error-weighted statistics without a separate noise calibration; the real-data weighted/unweighted status is exported.

For research claims, repeat on independent sectors/hosts, uniformly acquire TIC stellar properties for every class, match magnitude/noise/cadence distributions, quantify injection recovery and false alarms, bootstrap at TIC level, and assess fixed hybrid rankings on a locked evaluation population. Audit highly ranked false positives as carefully as known planets. A failure to outperform BLS is a valid outcome and must be reported unchanged.

Detailed equations and assumptions: [methodology](RESEARCH_GUIDE.md#methodology). Research questions: [research_questions](RESEARCH_GUIDE.md#research-questions). Actual verification and results: [validation](RESEARCH_GUIDE.md#validation), plus the generated report after a completed run.

After generating outputs, run `python scripts/verify_output_corrections.py --config config/default.yaml` to verify every BLS trial against its configured and baseline-dependent bounds, exactly reproduce primary scores by refitting the original feature order, and compare every all-feature ablation metric against the primary metrics. It writes `outputs/tables/correction_verification.json` within the configured experiment workspace. The check does not establish astrophysical validation or independent predictive performance.
# Completed research extension (11 October 2026)

The fresh Python environment is `../.venv`. The prospective V3 workflow is documented in
[RESEARCH_GUIDE.md#research-v3](RESEARCH_GUIDE.md#research-v3), with the exact submitted title/abstract and a
[claim-to-evidence checklist](RESEARCH_GUIDE.md#submitted-research-specification). The new manuscript
is [paper/v3/manuscript.md](paper/v3/manuscript.md); the completed V2 paper and its negative
independent comparison remain preserved in `paper/final` and `paper/archive_2026-09-16`.
The completed V3 primary comparison is semi-hybrid 24/300 versus BLS 32/300 catalogue-positive
targets at K=100. The separate corrected significance test has zero rejections. All 14,400
injection trials completed, but inspection savings and astrophysical causation remain
unsubstantiated. Read the [completed evidence](paper/v3/completed_evidence.md) and
[implementation status](RESEARCH_GUIDE.md#implementation-v3) before using claims in the poster.

## GitHub publication and final poster

See [publication file guidance](RESEARCH_GUIDE.md#github-release) for retained evidence and local-only artifacts. The final editable poster and print PDF are in [poster/overleaf_polished](poster/overleaf_polished/README.md).
