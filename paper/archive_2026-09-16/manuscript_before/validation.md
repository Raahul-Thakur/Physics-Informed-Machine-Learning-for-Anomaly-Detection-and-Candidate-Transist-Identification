# Verification record

This file records executed checks. The final small-sample results belong in the generated `outputs/research_summary.md`; no placeholder scientific results are supplied here.

## Environment

Windows, Python 3.11.9, CPU. Dependencies installed successfully in the sibling `.venv` during development. Both the main scientific stack and optional PyTorch installed. The exact validated package set is captured in `requirements-lock.txt` and each run's metadata. Source Git repository initialized; a Git commit is reported only when one actually exists.

## Real-data validation before the main experiment

Two public SPOC sector-1 light curves were downloaded with Lightkurve from MAST, with quality masking disabled at download to preserve the original arrays. Catalogue values came from the NASA TOI snapshot, not manually invented labels.

| TIC | Catalogue period (days) | Independent BLS period (days) | Relative period error |
|---|---:|---:|---:|
| 25155310 | 3.288790 | 3.289159 | 0.01122% |
| 261136679 | 6.267814 | 6.269787 | 0.03147% |

Both recovered the fundamental rather than requiring a half/double-period interpretation. The first diagnostic image was visually inspected: panels, axes, transit zoom, periodogram and metadata were readable, and transit dips remained after detrending. These deliberately selected known systems are software sanity checks, not evidence that anomaly detection adds value.

## Synthetic checks

Initial injected period 3.2 days was recovered as 3.1987725 days. At injected depths 0.001, 0.003 and 0.010, recovered box depths were approximately 0.0008342, 0.0025102 and 0.0094475. This deliberately simple validation shows sensitivity and a measurable depth bias from the detrending/search setup; it does not establish survey completeness. Ground truth and numerical results are stored separately in `outputs/tables/injection_*`.

Tests exercise invalid-array masks, gaps, all detrending choices, duplicate times, missing versus invalid errors, injection recovery, physical proxies, IF/LOF score orientation, novelty scoring, feature whitelist, training-only imputation, target aggregation, unlabelled exclusion from AUCs, unavailable metrics, catalogue sample integrity, cache invalidation and an offline pipeline producing figures/tables/reports. Optional autoencoder testing checks finite nonnegative MSE, determinism and target-group separation.

The final suite passed **21 tests in 22.74 seconds**; Ruff reported no errors and all 42 Python files passed its format check. The single warning concerns Lightkurve's optional pixel-model dependency `oktopus`, which this light-curve pipeline does not use. All five notebook files passed nbformat validation. Regression tests cover the sampling-pool correction, opt-in catalogue-derived model proxies, and download failures with cached successes. The corrected sample was verified to contain 30 planet/candidate hosts, 30 false positives and 50 backgrounds, with 110 unique TICs and no duplicates. The originally failed labelled download succeeded on retry. This correction preserved the same seeded labelled samples and restored the intended control group.

## External-access issues and fixes

The initial sandboxed Python request was blocked by the environment's network proxy. Authorized execution outside the network sandbox successfully reached NASA and MAST. The initially attempted `tess.stsci.edu` target-list hostname did not resolve. The implementation was corrected to use official MAST sector light-curve bulk manifests at `archive.stsci.edu`; their filenames define genuine observed TIC IDs. Manifest scripts are parsed, never executed. There is no synthetic or invented-catalogue fallback.

## Scope limits

A separate nine-target cached real-data probe (three targets from each group) completed preprocessing, BLS, features, IF/LOF, evaluation, ablations, figure generation and reporting. Its 17 PNG and 17 PDF figures and feature table were checked; numeric feature values contained no infinities. This probe lives under `experiments/cached_probe/` and is not the primary result sample. Its initial configuration predates the default exclusion of catalogue-dependent physical proxies; its outputs are retained only as an engineering check.

Before evaluating the full sample, the input-coverage audit found that 11 of the 30 planet/candidate reference periods exceeded 12 days. Planet labels comprised 20 PC, 9 CP and 1 KP. Stellar radii were available for 28 planet/candidate and 28 false-positive targets but no backgrounds. The final default therefore excludes stellar-catalogue-dependent proxies from ML while retaining their extracted measurements, without selecting this policy on model performance.

The larger configuration has not been claimed as executed. Multi-sector aggregation is implemented and unit tested, but the main small experiment selects one sector per target. No GPU is required. The optional autoencoder is separately tested and disabled in the default experiment. No planetary validation, pixel-level centroid vetting, dilution correction, limb-darkened transit fit, occurrence-rate inference or external held-out ML generalisation claim is made.


## Completed primary experiment (2026-09-09)

All 110 requested unique targets produced usable feature rows: 50 background, 30 planet, 30 false_positive. No final download/preprocessing/BLS/feature failure rows remained. The final model uses 41 explicitly selected features and excludes stellar-catalogue-dependent proxies.

| Method | Recovered in top 11 | Recall@11 | ROC-AUC (CP/KP vs FP/FA) | Average precision |
|---|---:|---:|---:|---:|
| bls_max_power | 2/30 | 0.0667 | 0.5567 | 0.2914 |
| depth_snr | 2/30 | 0.0667 | 0.5567 | 0.2914 |
| isolation_forest_score | 3/30 | 0.1000 | 0.4067 | 0.2225 |
| lof_score | 1/30 | 0.0333 | 0.4500 | 0.2357 |
| ensemble_score | 1/30 | 0.0333 | 0.4283 | 0.2266 |
| hybrid_score | 2/30 | 0.0667 | 0.4867 | 0.2574 |

At top 11, the hybrid tied BLS; at top 20 it recovered 5/30 versus 4/30 for BLS. These selected-sample differences do not establish generalisation or statistical improvement. The top-five hybrid candidates contained four catalogue false positives and one unlabelled control.

All five notebooks executed successfully against the final real outputs. The main run produced 21 PNG/PDF figure pairs, with two additional known-system validation pairs retained separately. Final tests: 21 passed (22.74 s), one nonblocking Lightkurve optional-dependency warning; lint and formatting passed.

Final resume verification reused all eight stages in 4.50 seconds. Ranking and performance CSVs remained byte-identical. No fresh remote downloads or scientific recomputation were needed.
