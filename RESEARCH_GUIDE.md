# Research guide

This guide consolidates all former documentation files. The submitted title and abstract are preserved. Earlier workflows, audits and manuscript text retain their historical claims and dates; they are not new evaluations. The completed V3 evidence is in [paper/v3/completed_evidence.md](paper/v3/completed_evidence.md). At K=100 the primary V3 hybrid recovered 24/300 catalogue-positive targets versus BLS 32/300; the archived V2 result is 28/300 versus 33/300. Neither result demonstrates reduced inspection workload.

Machine-readable audit data remains separately available in [output_audit.json](output_audit.json), unchanged byte for byte. Historical archived manifests keep their original paths and checksums.

## Contents
- [Submitted Research Specification](#submitted-research-specification)
- [Abstract Evidence Plan](#abstract-evidence-plan)
- [Research V3](#research-v3)
- [Implementation V3](#implementation-v3)
- [Github Release](#github-release)
- [Methodology](#methodology)
- [Research Questions](#research-questions)
- [Manuscript](#manuscript)
- [Abstract](#abstract)
- [Paper Workflow](#paper-workflow)
- [Research V2](#research-v2)
- [Research V2 Validation](#research-v2-validation)
- [Validation](#validation)
- [Output Audit](#output-audit)
- [Historical repository inventory](#historical-repository-inventory)
- [Consolidation provenance](#consolidation-provenance)

<a id="submitted-research-specification"></a>

## Submitted Research Specification

<!-- BEGIN submitted_research_specification -->
### Physics-Informed Machine Learning for Anomaly Detection and Candidate Transit Identification in TESS Light Curves

#### Submitted abstract (verbatim)

The Transiting Exoplanet Survey Satellite (TESS) has generated high-cadence photometric observations for millions of stars, creating an increasingly large search space for identifying transit-like signals and unusual stellar variability. While conventional transit-search algorithms such as the Box Least Squares method remain highly effective, automated machine-learning approaches can complement these techniques by identifying patterns that are difficult to specify explicitly and by prioritising unusual light curves for further investigation.
This work investigates a physics-informed machine-learning framework for detecting and characterising anomalous transit-like signatures in publicly available TESS light curves. The pipeline first performs photometric preprocessing, including quality filtering, normalisation, detrending, and segmentation. Candidate periodic signals are identified using conventional period-search techniques, while statistical and astrophysically motivated features describing transit depth, duration, periodicity, local variability, and signal morphology are extracted from each light curve.
These representations are subsequently analysed using unsupervised and semi-supervised anomaly-detection methods to identify observations that deviate significantly from dominant stellar variability patterns. Known exoplanet systems and labelled false-positive events are used as reference populations for evaluating whether the anomaly score provides additional discriminatory information beyond conventional detection statistics.
Particular emphasis is placed on interpretability rather than treating the machine-learning model as an independent discovery mechanism. The objective is to determine which photometric and temporal properties cause individual systems to be identified as anomalous and whether these properties correspond to physically meaningful transit characteristics.
The study demonstrates a computational framework in which machine learning acts as a candidate-prioritisation layer alongside established astronomical techniques, potentially reducing the number of light curves requiring manual inspection while retaining physically interpretable criteria for subsequent validation.

#### Definitions and claim-to-evidence checklist

Completed-run assessment (11 October 2026): see [the full evidence report](paper/v3/completed_evidence.md).
All 14,400 injection trials and the new independent evaluation are complete. The primary V3
semi-hybrid recovers 24/300 catalogue-positive targets versus BLS's 32/300 at K=100;
the corrected significance test rejects 0/20 targets. Software intervention effects are
measured, but astrophysical causation and reduced inspection workload are not demonstrated.
The checklist below maps implementations; the completed report determines evidential support.

The submitted text is preserved as the research specification. It does not override the evidence. Physics-informed means astrophysically motivated feature engineering, not equations enforced during training. Catalogue-dependent stellar-radius/duration proxies remain excluded from default ML inputs.

| Abstract statement | Code / experiment | Paper evidence and limitation |
| --- | --- | --- |
| Public TESS photometry | `src/tess_anomaly/download.py`, product manifests | V2 Data; V3 prospective acquisition |
| Quality filtering, normalisation, detrending, segmentation | `preprocessing.py`, `scripts/injections_v3.py` | Methods; expanded real-noise injection run must be completed before interpreting its results |
| Conventional periodic search | `bls.py`; strict period limits | Methods; grid eligibility is not observed-transit visibility |
| Astrophysical/statistical features | `features.py`, `coherence.py`, frozen feature-selection table | Methods; approximate morphology rather than physical training constraints |
| Unsupervised and semi-supervised analysis | `scripts/research_v3.py`: `fit`, `score`, limited training labels | IF/novelty LOF remain label-free; label spreading uses labelled and unlabelled training observations. Reference-class affinity modulates anomaly priority; not a calibrated planetary classifier |
| Significantly unusual | Frozen ranking `significance_policy`; separate `scripts/abstract_evidence.py` experiment | Percentiles are not p-values. Additional reference/test cohort locked before scoring, with conservative rank p-values and Holm correction; results and exchangeability limitations must be reported |
| Additional discriminatory information | `reports`, `bootstrap`, `sensitivity` | All methods compared with BLS; no outcome selected for favourable appearance |
| Properties that cause anomalous classification | `explain`; controlled raw-light-curve interventions | 54 paired synthetic input cases completed. Effects concern software scores; real-star diagnostics remain associations, not astrophysical causation or additive attribution |
| Candidate transit identification | `candidates`, optional explicit ephemeris table | Period/epoch agreement separated from host recovery; no planet validation |
| Potential inspection reduction | Recovery curves, budgets at fixed recall, gained/lost hosts | Must be evaluated on untouched targets; improvement not guaranteed |
| Inspection time | Blinded-review template and `review-times` command | Descriptive timing only after actual human review; no synthetic time-saving claims |

The preserved V2 result is hybrid 28/300 versus BLS 33/300 hosts at K=100, with a paired difference interval of [-13, +3]. V3 uses a new sample for new independent claims. No code can guarantee improved results or substantiate causal/significance language merely because it appears in the submitted abstract.
<!-- END submitted_research_specification -->

<a id="abstract-evidence-plan"></a>

## Abstract Evidence Plan

<!-- BEGIN abstract_evidence_plan -->
### Additional evidence for the submitted abstract

Protocol established on 3 October 2026, before examining prospective V3 scores.
The submitted title and abstract remain verbatim in `submitted_research_specification.md`.
The abstract is a research specification, not a requirement that an experiment succeed.
The original independent result remains hybrid 28/300 versus BLS 33/300 at K=100.

#### Separation and immutable ranking

The V3 model, its preprocessing, feature definitions, calibration and rankings are frozen in
`experiments/research_v3/frozen`. The new script `scripts/abstract_evidence.py` adds separate
experiments; it does not change the frozen ranking code or original no-significance V3 protocol.
The prospective acquisition selected 1,032 targets: 300 hosts, 232 catalogue false positives
and 500 unlabelled backgrounds, in sectors 27–39, excluding previously inspected targets.
These are requested/selected counts, not completed-analysis counts. Attrition must be reported.
Catalogue snapshots and original product manifests must be retained.

#### A precisely limited statistical-significance experiment

Before reading new scores, `lock-cohort` randomly assigned the 500 selected background IDs
to 480 reference and 20 test targets with seed 20261003. Assignment uses only IDs and group.
The hash-sealed cohort, selected sample and protocol are in
`experiments/abstract_evidence/significance_cohort`.
One sector is selected per target by valid cadence count, then baseline, then sector number,
using the same rule in both groups. The statistic is the negative raw Isolation Forest
`score_samples` output from the already frozen training model. The new reference observations
are not used to fit that model or choose the statistic.

The null population is the **selected unlabelled SPOC stellar population under the same
acquisition, coverage-selection and preprocessing rules**. Background status does not mean
verified nonplanet or clean stellar inlier. This experiment does not test planetary origin,
astrophysical novelty, or departure from every dominant stellar-variability class.

For score s and n available reference scores, the upper-tail p-value is
`(1 + number of reference scores >= s) / (n + 1)`. Ties are conservative.
Holm adjustment controls the family-wise error rate at 0.05 over all 20 planned test targets,
provided the marginal p-values are valid. Missing test observations remain in that family
with p=1 and an explicit unavailable status. Missing reference observations are counted;
role-dependent selection or acquisition would compromise the exchangeability assumption.

The 20/480 split was selected for finite-sample resolution, before seeing scores:
the smallest p-value is 1/481, below the first Holm threshold 0.05/20. With substantial
reference attrition, any rejection may become unattainable; this is reported rather than
changing the family or reference split. Passing numerical tests does not empirically prove
exchangeability, and the error guarantee is marginal over reference/test sampling rather
than conditional on this particular reference set. A null result remains a result.

See [Bates et al., Testing for Outliers with Conformal p-values](https://arxiv.org/abs/2104.08279)
for conformal outlier testing and the distinction between marginal and conditional validity,
and [Holm's sequentially rejective procedure](https://www.jstor.org/stable/4615733).
Our implementation uses the basic conservative rank p-value and Holm correction, not a
claim to implement all stronger procedures in Bates et al.

#### Controlled effects on software output

`config/abstract_interventions.yaml` fixes six signal cases and three phases on each of the
three real development stars already selected across low, medium and high noise for the
injection smoke test. The reference injection has period 3.2 days, depth 0.003 and duration
1.5 hours. Variants change only period (1.2 or 8 days), depth (0.001 or 0.01), or duration
(3 hours). Each is inserted into a fresh copy of raw photometry before detrending.
The frozen pipeline is rerun, including blind BLS, feature extraction and all ranking scores.
Uninjected controls and paired differences from the reference injection are retained.

This experiment can establish the response of this deterministic software to controlled
synthetic input changes. It cannot establish what physically caused the original stellar
variability. Period changes hold phase fraction fixed; event count, sampling and recovered
aliases can change. The experiment measures the total pipeline response, not the isolated
effect of one downstream feature. Repeated phases on one star are dependent measurements.
The three-star experiment is a diagnostic demonstration, not population-wide causal evidence.

Existing per-object training-reference percentiles and feature replacement diagnostics remain
useful descriptions of score behaviour. Correlated-feature replacements can be unrealistic;
they are not astrophysical causal attribution. Literal causal language in a poster must specify
whether it concerns controlled changes to software input or merely associations in real stars.

#### Sensitivity and potential inspection reduction

The full development injection experiment uses 30 distinct real stars and 14,400 paired
method-trials. It measures direct/alias period retrieval, processing failures and paired depth
distortion across noise strata. It does not measure real-candidate purity or a calibrated
false-alarm rate. Preprocessing changes motivated by its results require another frozen model;
the currently running independent V3 evaluation continues with its existing frozen settings.

The untouched V3 evaluation compares all six frozen rankings and BLS using recovery-versus-
budget curves, K=100 paired target-bootstrap differences, and the budget needed for the
predefined 10% catalogue-host recall. All-sector and exposure-controlled results, eligibility,
additional recovered hosts and missed hosts must be shown. Host recovery is not transit-signal
recovery. Period/epoch agreement needs a reviewed, reliable ephemeris table; no fabricated
ephemerides or automatic conversion of missing labels to negatives is permitted.

A lower inspection budget at the predefined recall would support a limited catalogue-recovery
claim on this sample. It would not establish human time savings, planetary purity or universal
superiority. If the hybrid is worse or the comparison inconclusive, the poster must report that.

#### Reproduction

##### Ephemeris and reference-label addendum (6 October 2026)

Before examining V3 scores, the NASA Planetary Systems table was downloaded with explicit
time-system and uncertainty metadata. `scripts/prepare_ephemerides.py` selects period and
epoch from the same literature row, requires BJD-TDB, finite positive uncertainties, no limit
flags and no flagged transit-timing variations. Among eligible solutions it prefers the archive
default, then the newest publication, with deterministic ties. This metadata reliability screen
retained 91 solutions across 79 selected targets; it is not a reanalysis of the cited papers.
The frozen matcher assumes zero period–epoch covariance and excludes ephemerides with
propagated uncertainty exceeding half the measured duration. Unknown time standards remain
untestable rather than being silently interpreted as TDB. See the
[NASA column definitions](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html).

The pipeline's `planet` reference group includes PC dispositions. The 300 selected positive
targets comprise 124 with a CP/KP disposition and 176 candidate-only targets. Retain this
combined group for the frozen primary metric, but call it **catalogue-positive recovery**.
Report CP/KP and candidate-only recoveries separately as supplementary descriptive analyses.
Neither the combined group nor all of its members should be called confirmed exoplanet hosts.
The selection audit and snapshot are retained under `experiments/abstract_evidence/ephemerides`.
The same audit of V2 found 151 CP/KP and 149 PC-only targets among its 300 positive references.
Its preserved 28/300 versus 33/300 result concerns the combined catalogue-positive group.

##### Commands

Run from `F:\Projects\YATI\tess-anomaly-research`, using the pinned environment:

```powershell
..\.venv\Scripts\python.exe -m pytest tests/test_abstract_evidence.py -q
..\.venv\Scripts\python.exe scripts/abstract_evidence.py lock-cohort --input experiments/independent_v3/data/catalog/sample.csv --output experiments/abstract_evidence/significance_cohort
..\.venv\Scripts\python.exe scripts/abstract_evidence.py interventions --output experiments/abstract_evidence/interventions
```

The cohort and intervention output already exist once started; do not overwrite or reselect.
After acquisition, feature extraction and provenance-checked export in `research_v3.md`:

```powershell
..\.venv\Scripts\python.exe scripts/abstract_evidence.py significance --input experiments/independent_v3/evaluation_features.csv --cohort experiments/abstract_evidence/significance_cohort --output experiments/abstract_evidence/significance
```

The evidence script is hash-locked by cohort creation. Any correction after locking must be
documented explicitly; it must not silently change cohort roles or the statistical hypothesis.

For the ephemeris-supported evaluation, use the selected catalogue file:

```powershell
..\.venv\Scripts\python.exe scripts/prepare_ephemerides.py --snapshot experiments/abstract_evidence/ephemerides/ps_transiting_snapshot.csv --sample experiments/independent_v3/data/catalog/sample.csv --output experiments/abstract_evidence/ephemerides/selection
..\.venv\Scripts\python.exe scripts/research_v3.py evaluate --input experiments/independent_v3/evaluation_features.csv --ephemerides experiments/abstract_evidence/ephemerides/selection/ephemerides.csv --output experiments/independent_v3/evaluation
..\.venv\Scripts\python.exe scripts/summarize_abstract_evidence.py --output experiments/abstract_evidence/final_summary
..\.venv\Scripts\python.exe scripts/review_v3.py --output experiments/abstract_evidence/diagnostic_review
```

The deterministic review selects up to two cases per group at K=100: combined positive
recoveries shared by BLS and semi-hybrid, BLS-only, semi-hybrid-only, labelled false positives,
and unlabelled backgrounds. It uses semi-hybrid rank except for BLS-only cases, which use BLS
rank; ties use TIC and sector. This rule was written before viewing V3 scores. These selected
illustrations describe failure modes and morphology; they do not estimate population prevalence.

#### Completed development evidence

All 14,400 injection method-trials completed successfully. Savitzky–Golay retrieved the injected
period directly in 3,924/7,200 trials (54.5%), compared with 3,703/7,200 (51.4%) for rolling
median. Their median paired depth biases were −5.27% and −1.83%, respectively. A 5,000-repeat
paired whole-star bootstrap gave a retrieval-fraction difference of +3.07 percentage points,
95% interval [+1.58,+4.71]. This interval concerns this predefined injection grid and 30 selected
stars, not independent real-planet recovery. Tables and verified PNG/PDF figures are in
`experiments/abstract_evidence/development_summary`.
Of the 14,400 trials, 768 were outside their realised search grid; they remain in the headline
denominator. Thirty-six trials lacked enough sampled template points for a finite paired depth
estimate; depth-bias medians condition on the remaining estimates. All 30 original raw-file
hashes were independently checked unchanged after the run.

All 54 controlled intervention cases completed. Responses varied by star and parameter;
no universal monotonic relation between stronger transits and anomaly priority is established.
<!-- END abstract_evidence_plan -->

<a id="research-v3"></a>

## Research V3

<!-- BEGIN research_v3 -->
### V3 research extension and reproduction workflow

The exact submitted title and abstract are in `submitted_research_specification.md`, together with the claim-to-evidence checklist. V2 remains preserved: compact hybrid 28/300 versus BLS 33/300 at K=100. Both inspected populations are now development evidence for any V3 choices. V3 outcomes must not replace or conceal that result.

#### Environment and relocation

The working repository is now `F:\Projects\YATI\tess-anomaly-research`. Activate the fresh environment from its parent with `.\.venv\Scripts\Activate.ps1`, or use the explicit interpreter below. From the repository directory, every command uses project-relative paths. `config/independent_v2.yaml` now uses a relative workspace and an exclusion path relative to that workspace. Historical source, models, configurations and manifests remain unchanged; old absolute paths in those historical records describe the original run, not the new location.

```powershell
cd F:\Projects\YATI\tess-anomaly-research
..\.venv\Scripts\python.exe -m pip check
..\.venv\Scripts\python.exe -m pytest -q
```

The original environment was rebuilt with Python 3.11.9 and `requirements-lock.txt`. The extension introduces no additional dependencies. For a clean machine, create a Python 3.11 environment, install the lock file, and preserve its exact scientific package versions.

#### Development and freeze

```powershell
..\.venv\Scripts\python.exe scripts/research_v3.py prepare --output experiments/research_v3/development_features.csv
..\.venv\Scripts\python.exe scripts/research_v3.py sensitivity --input experiments/research_v3/development_features.csv --output experiments/research_v3/sensitivity
..\.venv\Scripts\python.exe scripts/research_v3.py freeze --input experiments/research_v3/development_features.csv --output experiments/research_v3/frozen
..\.venv\Scripts\python.exe scripts/research_v3.py prepare-evaluation --output config/independent_v3.yaml
```

Commands refuse to overwrite existing outputs. If these artifacts already exist, use them; do not rerun into the same destination. Changes after freezing require a new named experiment. Inspecting a new evaluation removes its untouched status permanently, even if its results are inconvenient.

Training uses sectors 1–13; calibration uses sectors 14–26. A target with calibration-sector observations is excluded from training. One sector per target is selected by valid cadence count, baseline, then smallest sector before fitting/calibrating. This controls exposure, but the deliberate separation of observing eras can introduce distribution shifts; it does not remove all instrumental confounding. Evaluation uses sectors 27–39 and excludes every previously inspected target, including earlier small studies. Evaluation contains all permitted sectors per target up to the frozen acquisition cap; all-sector and coverage-selected-sector results are both reported.

Imputation, robust scaling, missingness/constant-feature filtering and Spearman redundancy removal use training data only. IF and novelty LOF never receive catalogue labels. Label spreading builds a graph from the entire training feature matrix, with 20% of eligible CP/KP and FP/FA references selected reproducibly within class. Remaining labels, PC-only targets, conflicting dispositions and backgrounds are -1. Catalogue-host labels do not establish that a particular sector's signal is planetary. This weak-label limitation applies to the semi-supervised method as well as evaluation.

A development run with an unbounded radial-basis graph encountered numerical underflow on extreme scaled features; its failure records are retained in `experiments/research_v3/sensitivity`. The revised graph clips robust-scaled coordinates to [-5,5] for label spreading only, with the same bound at training and prediction. IF/LOF retain their original scaled inputs. `graph_clipped_features` flags affected observations; saturation can discard information about extreme feature magnitudes. This is a numerical modelling choice made on development data, not a physical constraint or a change selected using a new evaluation.

The semi-supervised reference-class affinity is converted to a fixed calibration percentile and modulates the anomaly priority: `semi_anomaly = anomaly * (0.5 + 0.5 * affinity_percentile)`. The primary `semi_hybrid` is the equal average of this priority and the calibrated BLS percentile. These are predefined experimental scores, not validated probabilities. Label spreading assumes feature-neighbourhood smoothness; this assumption may be inappropriate for some astrophysical populations. The method and available interfaces are described in the [official scikit-learn documentation](https://scikit-learn.org/stable/modules/semi_supervised.html).

Calibration percentiles are not p-values. The frozen V3 ranking experiment takes the no-significance-claim route. A subsequent, separately locked reference-population test is documented in `abstract_evidence_plan.md`; it does not change V3 ranking scores or establish planetary significance. The submitted abstract's significance wording must be qualified by the precise population, assumptions and actual test results.

Development sensitivity varies training subsets, seeds and available label fractions. It is not an independent validation or a confidence interval for model-fitting uncertainty. Failure rows remain in its table. Any feature/weight selection based on those outcomes remains label-informed model selection.

#### New evaluation acquisition and reporting

Only after freezing:

```powershell
..\.venv\Scripts\python.exe scripts/run_pipeline.py --config config/independent_v3.yaml --stage download --resume
..\.venv\Scripts\python.exe scripts/run_pipeline.py --config config/independent_v3.yaml --stage features --resume
..\.venv\Scripts\python.exe scripts/research_v3.py export-features --input experiments/independent_v3 --output experiments/independent_v3/evaluation_features.csv
..\.venv\Scripts\python.exe scripts/research_v3.py evaluate --input experiments/independent_v3/evaluation_features.csv --output experiments/independent_v3/evaluation
```

`export-features` records the feature hash, acquisition/search/preprocessing configuration and selected-target attrition table. Evaluation checks these against the frozen protocol as well as source/package versions, target exclusions and permitted sectors. A complete study must inspect attrition and acquisition failures and report actual counts. Do not silently change the requested sample to improve recovery.

The output includes candidate measurements/flags, six ranking methods, recovery at every inspection budget, budget to attain the predefined 10% catalogue-host recall, gained/lost hosts for 80/20 complementary lists, paired target-bootstrap intervals and model-behaviour diagnostics. Bootstrap replicates jointly resample targets and rerank fixed scores at K=100. These intervals condition on the fitted model/calibration and do not include label errors or selection bias. Sensitivity analyses address different sources of variation separately.

Each candidate retains TIC, sector, period, epoch, depth, duration and all measured detection/features. Signal agreement is only evaluated when an explicit ephemeris file is supplied through `--ephemerides path.csv`. Required columns: `tic_id,catalogue_id,period_days,epoch_bjd_tdb,period_error_days,epoch_error_days,reliable`. Period/epoch errors are nonnegative days, epochs must be BJD_TDB, and `reliable` must be explicitly true following catalogue/provenance review. Multiple planet rows per host are supported. Candidate time systems must be explicit. Missing/unknown time systems and ephemerides with propagated uncertainty greater than half the candidate duration are marked untestable. Direct period agreement uses 1% tolerance; epoch agreement uses half the measured duration. Agreement is neither planet validation nor proof that the correct physical source produced the dip. The ephemeris file is retained with the result.

`score_explanations.csv` replaces one feature at a time by its training median, and repeats with the 40th/60th percentiles. It reports score changes and sign stability. These contrasts are not additive SHAP values, may form unrealistic combinations of correlated features, and do not establish causation. BLS-derived feature replacement holds the separate BLS ranking statistic fixed unless the replaced feature is depth SNR itself. This is a score diagnostic, not a physical light-curve intervention.

#### Expanded injections

```powershell
..\.venv\Scripts\python.exe scripts/injections_v3.py --config config/default.yaml --settings config/injections_v3.yaml --output experiments/research_v3/injections
```

The predefined experiment selects 30 distinct development targets across three raw point-to-point-noise strata, using one sector per target. It tests five periods, four depths, four durations and three random phases, paired across two detrenders: 14,400 method-trials. This is a substantial computation. The generator injects multiplicative trapezoids before detrending, preserves the raw files, reports processing failures and separately records direct versus harmonic recovery. Noise-stratified recovery includes processing failures in its denominator. Raw noise/flux uncertainties are retained rather than drawing fresh photon noise. Synthetic retrieval is not real-planet purity or calibrated false-alarm performance.

Complete this development-only run before adopting any new preprocessing choice. The default V3 retains the existing Savitzky–Golay choice; merely providing this experiment does not claim that expanded injections have already been run.

#### Manual review time and release

For a timing experiment, randomise/blind the review order, use a consistent decision rubric and record reviewer, method, case ID, UTC start/end and decision in the generated template. Score-conditioned budget savings do not establish time savings. The following produces descriptive timing summaries only; it does not establish a causal advantage or adjust for reviewer/order effects:

```powershell
..\.venv\Scripts\python.exe scripts/research_v3.py review-times --input completed_review.csv --output experiments/research_v3/review_times
..\.venv\Scripts\python.exe scripts/research_v3.py release --output releases/research_v3
```

Supply `--input experiments/independent_v3/evaluation` to the release command once that evaluation exists. The local release candidate contains code, tests, configs, dependencies, frozen feature tables/models, protocol, sample IDs, provenance, paper drafts and SHA-256 manifests. It does not publish anything or assign a URL/DOI. Full raw/processed photometry is not bundled; restore the recorded MAST products for upstream reproduction. Preserve the full workspace and v2 archive separately. Author/affiliation metadata and a public repository/deposit remain author publication tasks.
<!-- END research_v3 -->

<a id="implementation-v3"></a>

## Implementation V3

<!-- BEGIN implementation_v3 -->
### Implementation and experiment status

Revision: 11 October 2026. The V3 evaluation, expanded injections, significance test and diagnostic review are complete. `paper/v3/manuscript.md` preserves the submitted title/abstract. Detailed outcomes and limitations are in `paper/v3/completed_evidence.md`; historical V2 source and results remain unchanged.

| Requested work | Implemented artifact | Remaining scientific or publication work |
| --- | --- | --- |
| Preserve specification | `RESEARCH_GUIDE.md#submitted-research-specification`; exact abstract; claim-to-evidence checklist | Submitted causal/significance wording remains qualified by the evidence |
| Portable project | Relative active config paths; new Python 3.11 environment; relocated workflow | Historical paths remain historical; full photometry must be restored when moving machines |
| Genuine semi-supervised experiment | Limited labels + unlabelled graph; completed independent comparison alongside IF/LOF and BLS | Primary hybrid 24/300 versus BLS 32/300 at K=100; no superiority demonstrated |
| Experimental separation | Frozen transforms and rankings applied to 1,032 new targets; zero overlap | This evaluation is now inspected; future changes need new untouched data |
| Significance language | Separately locked 480-reference/20-test rank calibration with Holm correction | Zero rejections; significant anomalies not demonstrated |
| Score explanations | Training feature percentiles; median replacement; reference-value sign stability; clipping flags | Candidate interpretation and physical follow-up pending |
| Candidate identification | Full measured-feature table and metadata-screened ephemeris matching; ten diagnostic plots reviewed | No new planetary validation; unknown/stale ephemerides remain untestable |
| Expanded injections | All 14,400 trials completed on 30 stars; paired star-bootstrap uncertainty and depth distortion | Synthetic sensitivity does not establish real-planet purity |
| Inspection reduction | Completed budget curves and complementary rankings | Primary hybrid needs 112 versus BLS 87 inspections for 10% recovery; human timing unmeasured |
| Uncertainty/tests | Paired target reranking; 18 development sensitivity configurations; regression and end-to-end tests | Sensitivity is not a confidence interval incorporating every uncertainty source |
| Paper/release | Updated results draft and claim assessment; preserved V2 results; local hashes | Author/affiliation details, venue formatting and public deposit/DOI pending |

The first unbounded graph run failed numerically on extreme development features; its failure rows are retained. Bounding graph coordinates was a development-only implementation correction. The revised sensitivity run completed all 18 seed/label-fraction/training-fraction configurations. No evaluation-driven winner selection was performed. The experiment is now frozen; changes to the scientific implementation require another experiment version.

The V2 result remains compact hybrid 28/300 versus BLS 33/300 at K=100; these are catalogue-positive references, including PC-only targets. The original implementation verification remains at `experiments/research_v3/implementation_verification.json`. Completed-run verification is separately recorded at `experiments/abstract_evidence/completion_verification.json`. Passing tests does not substantiate unsupported abstract claims.
<!-- END implementation_v3 -->

<a id="github-release"></a>

## Github Release

<!-- BEGIN github_release -->
### GitHub publication files

The repository keeps source, tests, configurations, dependency files, notebooks,
research tables, sample identifiers, catalogue snapshots, paper drafts and frozen
experiment provenance. These support the reported results and are not disposable.

The final editable poster is `poster/overleaf_polished/`; its `main.pdf` is the
print version. The local delivery PDF in `output/` and Overleaf ZIP in `poster/`
are ignored duplicates. They can be uploaded separately as GitHub release assets.

Downloaded and processed photometry, cached downloads, fitted model binaries,
audit snapshots and local release bundles remain on disk but are excluded from
Git. A clone is therefore not a full frozen-workspace backup. Preserve the local
workspace; use the reproduction instructions and recorded products to restore
photometry. Frozen-model reproduction also requires the separately retained
model artifacts. Do not remove ignored research data with `git clean -fdx`.

Temporary QR tooling, Python caches, LaTeX build products and superseded poster
exports were removed on 2026-10-12. Historical experiment and paper evidence was
preserved. Local duplicate release and reproduction-check folders are ignored.

From the repository root, review and prepare a commit:

```powershell
git status --short
git add .
git diff --cached --stat
git commit -m "Add TESS research pipeline, evidence and final poster"
git remote -v
```

Use the configured repository and branch for the subsequent push. This cleanup
has not committed or pushed any files and has not changed the remote settings.
<!-- END github_release -->

<a id="methodology"></a>

## Methodology

<!-- BEGIN methodology -->
### Methodology

#### Scope and terminology

The implemented experiment uses unsupervised anomaly detection. Catalogue labels are reserved for evaluation; a separate novelty-scoring helper does not establish a semi-supervised experiment. Physics-informed means astrophysically motivated features such as transit depth, duration, morphology and approximate radius ratio, rather than physical equations enforced during training. Stellar-catalogue-dependent radius and duration-consistency proxies are extracted when possible but excluded from default ML inputs because measurement availability differs between groups.

High anomaly scores describe unusual feature-space observations relative to the fitted reference population. They are not calibrated statistical significance. Feature correlations, ablations, PCA and diagnostic reports examine properties associated with high anomaly scores; they do not establish causation or provide formal per-object model attribution. The primary models fit and rank the same unlabelled sample. Reduced manual inspection workload and generalisation remain research questions requiring independent evaluation.

#### Population and unit of analysis

The experiment is a seeded, observing-selected, catalogue-stratified reference experiment, not a blind occurrence-rate survey. NASA TOI snapshot labels are CP/KP (confirmed/known), PC (candidate), FP (false positive), FA (false alarm) and ambiguous classes. Background means no TOI entry in the archived snapshot. It does not imply the absence of a transiting planet. Multi-disposition hosts with both positive and false-positive entries are excluded as ambiguous. Target properties use the first TOI entry; all entries are retained for period checks.

Features are measured per target-sector. Scores are aggregated per unique TIC by maximum across sectors for each method. Cross-method sector selection can differ; extra sectors confer extra opportunities for extreme scores. No sector is treated as an independent star in recovery metrics. The primary descriptive model fits the full unlabelled sample; claims about predictive generalisation require a separate target-disjoint experiment.

#### Preprocessing

Input PDCSAP flux is in electrons/second; times are BTJD in days. Discard nonfinite times/flux, nonpositive flux, partially invalid reported errors and selected quality bits. Entirely absent uncertainties remain missing and cause an explicitly recorded unweighted BLS search. Sort times and retain the first exact duplicate. Cadence arrays always share masks and ordering.

Normalize by the positive median flux, y_i=f_i/median(f). Split where consecutive times differ by more than the configured gap. For each segment use median normalization, a rolling median, or a second-order Savitzky–Golay trend with odd window approximately window_days/median_cadence. Short segments fall back to a constant median.

With transit preservation enabled, repeat trend fitting three times, temporarily masking residuals beyond 3 robust standard deviations only in the trend input. Interpolate the masked trend input within each segment; never fill observational gaps in the science time series. Divide normalized flux and errors by the trend. Dips are not deleted. This procedure still can distort long/low-SNR transits and must be tested with injections across duration and window choices.

#### BLS

Astropy `BoxLeastSquares` fits a periodic box to weighted photometry. At trial period P, duration D and epoch t0, the box separates in-transit and out-of-transit cadences, estimates their level difference δ and its uncertainty σδ, and maximizes either δ/σδ (`snr`) or the BLS likelihood objective. The default SNR objective makes maximum power and depth SNR identical.

The duration-driven automatic grid uses Astropy's frequency-factor control. Small factors produce finer sampling; the initial factor 5 is an economy setting and is not a guarantee of recovery at every phase. Search periods are capped by baseline/min_transits, with min_transits=2. This is a necessary baseline condition, not a guarantee of two observed events. The expected number counts transit centres within the time range; observed events count distinct epochs with at least one in-transit cadence and do not guarantee adequate event coverage.

The robust periodogram peak statistic is

    Z_BLS = (max(power) - median(power)) / [1.4826 median(|power - median(power)|)].

It is an empirical prominence measure, **not** a normal-tail significance or false-alarm probability. Constant power yields missing Z. The second peak is a local maximum outside a main-peak width heuristic ~3PD/baseline; it may still be a harmonic. P/2 and 2P searches are reported only within the configured period range. Catalogue period checks calculate |P_recovered-P_catalogue|/P_catalogue, and the minimum relative error to {P/2,P,2P}. Search inputs never contain the catalogue period.

Signed folded time is ((t−t0+P/2) mod P)−P/2. Plot bins use medians and never feed the search. Zoom limits use the measured duration. A box model does not distinguish planets from binary eclipses or instrumental dips.

#### Statistical and physical features

Flux features use detrended relative flux: mean, median, population variance/standard deviation, min/max, peak-to-peak, IQR, skewness, excess kurtosis and RMS about unity. Robust MAD is 1.4826 median(|x−median(x)|). Successive differences exclude segment boundaries; point-to-point scatter is MAD(Δx)/sqrt(2), difference RMS is sqrt(mean(Δx²)), and median absolute successive difference is median(|Δx|). Percentile amplitude is q95−q5. Duty cycle is min(1,N median_cadence/(baseline+median_cadence)); it is an approximate sampling occupancy, not a transit completeness estimate.

Transit morphology uses |folded_time|<D/2 and an out-of-transit buffer |folded_time|>D. Medians require at least three points. Measured depth is out-median minus in-median. Asymmetry compares pre-centre and post-centre in-transit medians; it is a proxy, not fitted ingress/egress timing. Odd/even differences compare alternating-event medians. Significance uses between-event scatter with at least two measurable events of each parity, preventing cadence-count inflation from being the sole uncertainty estimate. These small-sample proxy uncertainties are approximate. Secondary depth compares the out-of-transit median to a D-wide window at phase 0.5; eccentric binaries can have secondary eclipses elsewhere. No arbitrary V-shape feature is supplied.

For 0<δ<1, radius-ratio proxy k≈sqrt(δ). With a measured Rstar>0, Rp_proxy=Rstar sqrt(δ), converted from solar to Earth radii using Astropy constants. Assumptions: dark occultor, unblended flux, non-grazing transit, negligible limb-darkening effects. This is not a validated planet radius.

With measured positive Mstar and Rstar, a=(G Mstar P²/(4π²))^(1/3), and the circular central small-companion duration is Dcentral≈P/π asin(Rstar/a). Store D/Dcentral only if 0<Rstar/a<1. Missing mass is never inferred from a generic constant. Eccentricity, impact parameter, dilution, stellar-parameter errors and finite companion radius can invalidate this approximation. Catalogue availability patterns can leak source selection through missingness even when explicit labels are excluded.

#### Feature preprocessing and anomaly models

An explicit family whitelist excludes TIC, sector, TOI, disposition and catalogue periods. Replace infinities with missing, drop features above the missing-fraction threshold and constant features, median-impute remaining features, then use median/IQR RobustScaler (or StandardScaler). Save feature ordering and fitted transform. Transforming unseen data does not refit preprocessing. Primary fitting is on the full unlabelled reference population.

The default additionally excludes the stellar-catalogue-dependent radius-in-Earth-units and duration-consistency proxies from model fitting, while preserving their measured values in the feature table. In the initial sample, controls have no uniformly acquired stellar radii/masses, so imputation patterns could expose catalogue selection. `models.use_stellar_catalog_features` is an explicit opt-in for future samples with uniformly sourced stellar metadata. This choice is based on input coverage, not ranking results. The default physics family still contains transit morphology and the transit-depth radius-ratio proxy.

Isolation Forest uses random feature-space partitions. Short average isolation paths imply anomalies; use **negative `score_samples`** so larger values mean more anomalous. LOF compares a point's local reachability density to that of its neighbours. Primary fit-time LOF is `novelty=False` and uses **negative `negative_outlier_factor_`**. The separate novelty helper fits `novelty=True` and scores only excluded, unseen points. Neighbour count is capped at N−1. Contamination affects threshold labels, not the orientation of ranking scores.

The optional CPU autoencoder has widths d→64→32→8→32→64→d, ReLU hidden activations and linear output. Adam minimizes mean squared reconstruction error; early stopping uses a deterministic target-group validation split. A separate AE feature transform is fitted only on those training groups, then applied unchanged to validation and score rows. Anomaly score is mean_j (x_j−xhat_j)². Validation losses monitor reconstruction, not planet classification accuracy; scientific evaluation remains descriptive. Small samples and high-dimensional spaces can overfit.

#### Ensemble, hybrid and ablations

Percentile r_i=average_rank(score_i)/N, with average ranks for ties. Equal-weight ensemble is the mean percentile of enabled IF, LOF and optional AE scores. Hybrid is (percentile(depth_SNR)+percentile(ensemble))/2. The formula is fixed without fitting evaluation labels. A combined ranking is not presumed superior.

Four independently fitted representations are compared: generic statistics/observing properties; BLS quantities; transit morphology and physical proxies; all features. Missing/constant features are handled separately for each family. This ablation tests representations but is not a causal estimate of physics benefit; catalogue-dependent measurements and correlated features are confounders.

Every family uses the original feature-table fitting order and the same configured random seed. The all-features refit must reproduce the primary model; sorting by anomaly score before fitting changes Isolation Forest's sampled row identities and is not an acceptable ablation comparison.

Automatic BLS trial periods are explicitly filtered to the configured minimum and the smaller of the configured maximum and baseline/minimum-transits cap before power evaluation. The automatic grid's rounded endpoint is not allowed to extend the search interval.

#### Evaluation and uncertainty

Sort descending by score; deterministic TIC order breaks exact ties. Let N+ be catalogue-positive targets and H_K their count among the top min(K,N): catalogue-positive Precision@K=H_K/min(K,N); Recall@K=H_K/N+. Top 5%,10%,20% use ceil(fN). Report requested and effective K, mean/median positive rank, and undefined denominators explicitly. These precision values are known-host yield, not true planetary purity.

ROC-AUC and average precision are calculated only on CP/KP hosts versus FP/FA hosts and only when both classes exist. PC-only and unlabelled background do not enter these binary metrics. Average precision is the sklearn non-interpolated recall-weighted precision summary, not trapezoidal PR-AUC. Spearman correlations report finite-pair counts. Mann–Whitney tests compare each class against the rest; p-values are exploratory, uncorrected for multiplicity, and not sufficient evidence for a scientific claim. Target bootstrap confidence intervals, matched controls and a locked external evaluation are recommended next steps.

PCA is fitted to the scaled numeric feature space for inspection, with variance fractions and loadings exported. It does not validate astrophysical separation. Top-target feature tables and six-panel diagnostic figures support manual review but provide no planetary validation.

The generated report counts hosts whose representative catalogue period is outside the configured interval; this is not completeness over every planet in multi-planet systems, and individual-sector baseline caps restrict coverage further. It also tabulates usable sector counts by reference group. Max-across-sector ranking creates unequal opportunities for high scores when coverage differs. These comparisons are not exposure-matched. Top hybrid-ranked backgrounds remain unlabelled inspection candidates, not validated planets. Independent evaluation must account for search coverage and observing exposure before generalisation or reduced workload can be claimed.

#### Reproducibility and integrity

Store source catalogue snapshots, observing manifests, requested IDs, original FITS/NPZ, intermediate photometry, BLS caches, configuration, dependency versions and UTC run metadata. Scientific cache keys include input bytes, relevant parameters and source code hash. Original FITS download caching is separate. Individual target failures are explicit and contribute to sample attrition. A global stage failure raises an exception and cannot masquerade as a successful experiment. Synthetic injection truth is stored separately and never substitutes for real archive failures.

Sources: [Astropy BLS documentation](https://docs.astropy.org/en/stable/timeseries/bls.html), [NASA TOI definitions](https://exoplanetarchive.ipac.caltech.edu/docs/API_TOI_columns.html), [Lightkurve downloads](https://lightkurve.github.io/lightkurve/reference/search.html).
<!-- END methodology -->

<a id="research-questions"></a>

## Research Questions

<!-- BEGIN research_questions -->
### Research questions and planned comparisons

1. **RQ1:** Do anomaly scores rank known transit-hosting systems differently from the broader observed population? Compare class distributions and known-host recovery; include false positives as their own group.
2. **RQ2:** How strongly do anomaly scores correlate with BLS power and depth SNR? Report Spearman correlations and scatter; note default SNR-power redundancy.
3. **RQ3:** Does a fixed BLS/anomaly hybrid improve top-ranked known-host recovery over BLS alone? Report improvements, ties and degradations without selecting a favourable formula after observing labels.
4. **RQ4:** Do astrophysical morphology/consistency features improve rankings relative to generic statistics? Compare four predeclared feature families; audit missingness and observing-property confounding.
5. **RQ5:** Which photometric and temporal properties are associated with high anomaly scores? Inspect feature correlations, PCA, top-target tables and diagnostic light curves, including high-ranked binary/systematic cases. These are associations, not causal explanations or formal per-object model attribution.
6. **RQ6:** Can anomaly-based or hybrid prioritisation reduce manual inspection workload while retaining useful candidates on an independent evaluation population? Current fixed-budget recovery metrics describe the same unlabelled sample used for fitting and do not establish such a reduction or generalisation.

The current experiment is descriptive validation of a research pipeline. Before paper-level inference, lock a target-disjoint evaluation sample, uniformly obtain stellar metadata, specify primary K and confidence-interval procedures, and assess selection and detection biases. A negative result is scientifically informative: it can identify the limits of unsupervised anomaly prioritisation and which false positives it promotes.
<!-- END research_questions -->

<a id="manuscript"></a>

## Manuscript

<!-- BEGIN manuscript -->
### Physics-Informed Machine Learning for Anomaly Detection and Candidate Transit Identification in TESS Light Curves

#### Submitted abstract

The Transiting Exoplanet Survey Satellite (TESS) has generated high-cadence photometric observations for millions of stars, creating an increasingly large search space for identifying transit-like signals and unusual stellar variability. While conventional transit-search algorithms such as the Box Least Squares method remain highly effective, automated machine-learning approaches can complement these techniques by identifying patterns that are difficult to specify explicitly and by prioritising unusual light curves for further investigation.
This work investigates a physics-informed machine-learning framework for detecting and characterising anomalous transit-like signatures in publicly available TESS light curves. The pipeline first performs photometric preprocessing, including quality filtering, normalisation, detrending, and segmentation. Candidate periodic signals are identified using conventional period-search techniques, while statistical and astrophysically motivated features describing transit depth, duration, periodicity, local variability, and signal morphology are extracted from each light curve.
These representations are subsequently analysed using unsupervised and semi-supervised anomaly-detection methods to identify observations that deviate significantly from dominant stellar variability patterns. Known exoplanet systems and labelled false-positive events are used as reference populations for evaluating whether the anomaly score provides additional discriminatory information beyond conventional detection statistics.
Particular emphasis is placed on interpretability rather than treating the machine-learning model as an independent discovery mechanism. The objective is to determine which photometric and temporal properties cause individual systems to be identified as anomalous and whether these properties correspond to physically meaningful transit characteristics.
The study demonstrates a computational framework in which machine learning acts as a candidate-prioritisation layer alongside established astronomical techniques, potentially reducing the number of light curves requiring manual inspection while retaining physically interpretable criteria for subsequent validation.

#### 1. Study scope and interpretation

This draft retains the submitted title and abstract verbatim. Physics-informed denotes astrophysically motivated feature engineering, not equations enforced during training. The submitted abstract describes the research objectives. Statistical significance, astrophysical causation, planetary validation and workload reduction are not established by those objectives. High anomaly scores and controlled changes in model scores are the operational quantities tested here.

The study is organised into the completed V2 unsupervised experiment and a separate completed V3 extension. Previously inspected V2 populations are development evidence for V3. The original numerical result is preserved rather than replaced by a new model choice. V3 was evaluated on 1,032 unseen targets. Detailed tables, diagnostic review and claim limitations are recorded in [Completed V3 evidence](paper/v3/completed_evidence.md).

The Transiting Exoplanet Survey Satellite (TESS) provides time-series photometry for studying transiting planets and stellar variability ([Ricker et al., 2015](https://doi.org/10.1117/1.JATIS.1.1.014003)). Box Least Squares (BLS) searches for periodic, box-shaped decreases in brightness and supplies a conventional detection baseline ([Kovács et al., 2002](https://doi.org/10.1051/0004-6361:20020802)). The present study asks whether anomaly scores derived from measured light-curve properties add useful information to that baseline. A high anomaly score expresses unusualness relative to the fitted population; it is not a probability that a planet is present.

Machine learning has already been applied to transit classification. Shallue and Vanderburg trained a convolutional neural network to distinguish potential Kepler planet signals from false positives ([2018](https://doi.org/10.3847/1538-3881/aa9e09)). Yu et al. extended deep-learning methods to TESS candidate triage and vetting ([2019](https://doi.org/10.3847/1538-3881/ab21d6)). Those supervised, signal-level classification tasks differ from the present experiment, which fits anomaly models without labels and evaluates rankings at the host level. Their classification performance cannot be compared directly with the catalogue-host recovery measured here.

Unsupervised analysis of TESS photometry also has prior precedent. Crake and Martínez-Galarza applied an Unsupervised Random Forest to anomalous stellar light curves and discussed how the parent population affects the kinds of anomalies retrieved ([2023 preprint](https://arxiv.org/abs/2301.10264)). The CLARA framework investigates synthetic-data-guided Unsupervised Random Forests and morphological analysis for TESS transit detection ([Dasgupta, 2025 preprint](https://arxiv.org/abs/2508.04722v4)). These approaches establish relevant context, but Unsupervised Random Forests and the Isolation Forest used here are different algorithms. We do not claim that unsupervised transit analysis itself is new, nor do we reproduce these frameworks or compare their reported yields with our differently selected sample.

Our implementation combines Isolation Forest, which scores observations through random partitioning ([Liu et al., 2008](https://doi.org/10.1109/ICDM.2008.17)), with Local Outlier Factor (LOF), which measures local density differences ([Breunig et al., 2000](https://doi.org/10.1145/342009.335388)). Astrophysically motivated depth, duration, approximate radius-ratio and morphology measurements make the inputs inspectable. This use of physical motivation does not enforce physical equations during training, and feature inspection does not establish causal or formal model attribution.

Preprocessing can alter the transit signals being sought. The Wōtan study compares detrending methods with attention to transit preservation ([Hippke et al., 2019](https://doi.org/10.3847/1538-3881/ab3984)). That work motivates testing preprocessing through recovery experiments; the present small injection pilot compares our Savitzky–Golay and rolling-median implementations and is not a reproduction of Wōtan's benchmark. The contribution here is a frozen, target-disjoint comparison with BLS, accompanied by exposure controls, conditional uncertainty estimates and descriptive diagnostics, including an explicitly reported negative result at the primary inspection budget.

Do interpretable unsupervised anomaly scores add useful candidate-prioritisation information beyond conventional BLS statistics at a fixed inspection budget? An unusual light curve need not contain a planet. Catalogue-positive host recovery is the operational reference outcome; it is not confirmed transit recovery or true planetary purity.

#### 2. Completed V2 experiment: methods

Raw quality flags are retained during acquisition, then mask 175 is applied during preprocessing. Flux is normalised and detrended separately across gaps larger than 0.25 days, using a 1.5-day Savitzky–Golay window with iterative masking during trend estimation ([Savitzky and Golay, 1964](https://doi.org/10.1021/ac60214a047)). Non-finite and non-positive raw fluxes are removed; downward deviations in retained relative flux are not deleted as outliers. Masking and interpolation during trend fitting do not replace the retained observations. BLS searches use valid flux uncertainties as weights when available, trial periods from 0.5 days to the smaller of 12 days and half the observed baseline, durations of 1–4 hours, and the signal-to-noise ratio (SNR) objective. Automatic period-grid overshoots are explicitly removed. This baseline cap is a heuristic support criterion, not proof of observed transit visibility.

Feature families include generic variability/observing properties, BLS statistics, morphology proxies, all legacy features, compact morphology/coherence and an extended family. Event-depth and sampled-width consistency, event dominance, local binned-noise ratios, edge/centre morphology and a coarse secondary-phase scan are measured. These are approximate photometric diagnostics; none independently validates a planet. Feature definitions and missing-data/selection decisions accompany the supplement. Compact and extended redundancy removal uses absolute Spearman correlation ≥0.95 on training data only, in fixed feature order. Stellar-catalogue radius and duration-consistency proxies remain excluded by default because measurement availability is population-dependent.

The 796 training targets fit median imputation, robust scaling, Isolation Forest and novelty-enabled Local Outlier Factor without labels. LOF is configured with `novelty=True` before fitting, and calibration and evaluation observations are unseen during fitting, following the [scikit-learn novelty-scoring interface](https://scikit-learn.org/stable/modules/outlier_detection.html). The training population is not assumed to be a verified set of non-anomalous stars. Separate 200-target development calibration distributions fix midpoint empirical cumulative distribution function (CDF) score mappings; calibration uses one coverage-selected curve per target. Equal-weight Isolation Forest (IF) and LOF calibrated percentiles form the ensemble; BLS and ensemble percentiles form the fixed hybrid. Evaluation never refits transforms, models or score calibration. Choosing compact features was motivated by prior labelled development comparisons and is disclosed as label-informed experiment selection, despite unsupervised fitting.

The primary analysis takes each method's maximum score across sectors per TESS Input Catalog (TIC) identifier. A sensitivity analysis selects the sector with most valid cadences, then longest baseline, then smallest sector number, without reading scores or labels. Area under the receiver operating characteristic curve (ROC-AUC) and average precision (AP) use confirmed/known planet (CP/KP) hosts versus false-positive/false-alarm (FP/FA) references, excluding planetary-candidate-only (PC-only) hosts and backgrounds. These disposition definitions follow the [NASA Exoplanet Archive documentation](https://exoplanetarchive.ipac.caltech.edu/docs/API_TOI_columns.html). Full-sample recall retains all hosts; an additional denominator includes the 192 hosts whose representative periods lie within the effective grid. Fourteen hosts lack usable periods and 94 have known periods outside the effective grid. Eligibility is not an ephemeris-based visibility or multi-planet completeness calculation.

A fixed complementary list contains 80 BLS-selected targets plus the 20 highest anomaly-ranked targets not already selected. Additional and lost hosts are both reported. The reporting-stage uncertainty analysis resamples independent targets jointly for BLS and hybrid, then reranks the resampled target copies at K=100 (the number of targets selected for inspection) in 5,000 replicates. Percentile 95% intervals describe evaluation-sample and ranking variability conditional on the frozen models. They do not include training/calibration-refit uncertainty, label errors, or population-selection bias. The pre-existing complementarity intervals instead condition on fixed inspection lists; these two uncertainty definitions must not be conflated. No bootstrap interval is presented as a formal causal or discovery significance test.

#### 3. Completed V2 experiment: results

Reference-label audit: the 300 positive V2 targets comprise 151 systems with a CP/KP disposition and 149 PC-only targets. In the numerical comparisons below, "hosts" denotes this combined catalogue-positive reference group, not 300 confirmed exoplanet systems. The historical counts and frozen archives are preserved; the distinction corrects their interpretation.

The frozen primary compact hybrid recovers 28/300 hosts (9.3%) at K=100, versus 33/300 (11.0%) for BLS, a difference of -5 hosts (−1.7 percentage points of host recall). The paired reranked-bootstrap interval is [-13, 3] hosts. The single-sector comparison gives hybrid 30 versus BLS 34, difference -4, interval [-13, 4]. At the same all-sector budget, the compact ensemble recovers 23 hosts. The 80/20 complementary list recovers 27 versus 33 for BLS, gaining one and losing seven hosts. Under one-sector selection it recovers 28 versus 34. None of the alternative hybrid feature-family comparisons exceeds BLS at K=100. These comparisons are reported without choosing a new primary method after viewing independent outcomes.

All 216 pre-detrending injection trials completed without processing errors: 108 matched injected signals evaluated with each of the two methods, across six real light curves, three depths, three periods and two durations. Savitzky–Golay retrieved the injected period in 60/108 trials; rolling median in 55/108. Median paired template-depth bias was −7.3% and −1.6%, respectively. This small trapezoid-in-real-noise pilot indicates a depth-preservation/retrieval tradeoff, not general survey completeness. Existing noise and uncertainties were retained; no photon-noise realisation was regenerated. Uninjected controls can contain real signals and therefore do not establish calibrated false-alarm rates.

#### 4. V3 extension: predefined methods

The V3 development pool combines the two previously inspected populations. Training sectors 1-13, calibration sectors 14-26 and prospective evaluation sectors 27-39 are disjoint. Targets represented in calibration sectors are removed from training. Evaluation excludes every previously inspected target, including prior small studies. This partition is an exposure control, not a claim that different observing eras have identical distributions.

Training and calibration select one sector per target by valid cadence count, baseline, then sector number before reading model scores. Photometric compact features undergo training-only missingness/constant-feature filtering, redundancy selection, median imputation and robust scaling. Stellar-catalogue-dependent proxies remain excluded. Independent evaluation applies these transformations unchanged and reports both maximum-across-sector and coverage-selected-sector rankings.

Isolation Forest and novelty-mode Local Outlier Factor are fitted without labels. A separate label-spreading graph uses both labelled and unlabelled training observations. Its robust-scaled coordinates are clipped to [-5,5] at both training and prediction to prevent numerical underflow observed during development. IF/LOF inputs are not clipped. Clipped-feature counts are reported; graph saturation can lose information about extreme magnitudes. Twenty percent of eligible references in each of the CP/KP and FP/FA classes supply labels; planetary candidates, ambiguous/conflicting references and unlabelled backgrounds remain unknown. Host labels are weak references for a sector-level signal and may not identify the physical origin of the detected dip. The graph's neighbourhood-smoothness assumption is an experimental hypothesis. See the [scikit-learn semi-supervised documentation](https://scikit-learn.org/stable/modules/semi_supervised.html).

Fixed calibration percentiles combine IF/LOF anomaly scores. The semi-supervised reference-class percentile modulates anomaly priority by multiplication with (0.5 + 0.5 * percentile). The primary semi_hybrid averages this priority with the fixed BLS percentile. Six methods, including pure BLS, are reported. These affinities and percentiles are neither planet probabilities nor p-values; no formal anomaly-significance claim is made.

Independent reporting measures recovery at every target-inspection budget, the budget required for 10% catalogue-host recall, and gained/lost hosts under a fixed 80/20 BLS/additional-method allocation. Paired target bootstrap intervals resample and rerank while keeping fitted models and calibration fixed. Separate development sensitivity experiments vary seeds, training fractions and label fractions. These are not independent performance estimates or combined confidence intervals for every source of uncertainty.

Candidate tables preserve periods, epochs, depths, durations, scores and flags. Direct period agreement and epoch agreement are distinguished from catalogue-host recovery. An optional multi-planet ephemeris table requires explicit BJD_TDB epochs, period/epoch uncertainties and a reliability assessment. Unknown time systems and stale ephemerides are marked untestable rather than counted as validated signals. Matching does not establish planetary origin.

For individual scores, controlled feature replacements compare an observation with its training-median counterpart and vary the reference over the 40th-60th percentiles. These contrasts and sign-stability measures describe model behaviour. They are not additive attribution values or astrophysical causal effects; correlated features can produce unrealistic replacement combinations.

The expanded preprocessing protocol selects 30 distinct development targets across three measured noise strata and tests five periods, four depths, four durations and three phases with two detrenders (14,400 method-trials). Signals are inserted before detrending. Processing failures, harmonic/direct period recovery and depth distortion are retained. This planned run is separate from the completed 216-trial V2 pilot. Real noise and uncertainties are retained; synthetic completeness and real-planet purity are different quantities.

#### 5. V3 results

All 1,364 selected light curves from 1,032 targets yielded features, with no remaining acquisition or processing failures. The reference groups contain 300 catalogue-positive targets (124 CP/KP and 176 PC-only), 232 labelled false positives and 500 unlabelled backgrounds. There is no overlap with previously inspected targets and no out-of-range BLS solution.

At K=100, the predefined semi-supervised hybrid recovers 24/300 catalogue-positive targets versus BLS's 32/300. The paired target-bootstrap difference is -8, with 95% interval [-19,+2], conditional on frozen models and calibration. One-sector recovery is 22 versus 31, interval [-20,+1] for the difference. The inspection budget to recover 30 positive targets is 112 for the primary hybrid versus 87 for BLS (one-sector: 116 versus 88). The primary experiment does not demonstrate inspection reduction.

The secondary reference-class-affinity ranking recovers 37/300 at K=100, with a difference interval [-6,+16] versus BLS. It recovers 21 CP/KP systems versus BLS's 26; the larger combined count includes more PC-only targets. It is not substituted for the predefined primary method. All six rankings and both exposure analyses are retained in the supplement. The primary 80/20 complementary list gains four positives but loses six, recovering 30 versus BLS's 32. The search-eligible group contains 219 positive targets; BLS and the primary hybrid recover 31 and 21 respectively without changing the headline denominator.

Metadata-screened literature ephemerides provide testable selected-sector comparisons for 76 positive targets. The top 100 BLS and primary-hybrid lists contain 20 and nine period-and-epoch matches, respectively. Matching is distinct from host recovery and does not validate a new planet. Unavailable or imprecise ephemerides remain untestable.

The separately locked significance experiment scores 480 reference and 20 test targets. Conservative rank p-values and Holm correction at alpha=0.05 yield zero rejections; the smallest adjusted p-value is 0.08316. This test assumes exchangeability with the selected unlabelled reference population, not planetary origin. Thus this experiment does not demonstrate statistically significant anomalies. It supplements rather than changes the frozen V3 ranking protocol; see [Bates et al.](https://arxiv.org/abs/2104.08279) and [Holm](https://www.jstor.org/stable/4615733) for the statistical context.

All 14,400 expanded injection trials completed on 30 real development stars. Savitzky-Golay retrieves the injected period in 3,924/7,200 trials versus rolling median's 3,703/7,200. The paired whole-star bootstrap difference is +3.07 percentage points, 95% interval [+1.58,+4.71]. Median paired depth biases are -5.27% and -1.83%. The 768 out-of-grid trials remain in recovery denominators; depth medians exclude 36 unavailable estimates. Synthetic retrieval and attenuation do not measure real-planet purity.

All 54 controlled input-intervention cases completed, demonstrating star-dependent software responses to altered synthetic depth, duration and period. These effects do not establish the astrophysical causes of the original variability. Ten deterministically selected diagnostic plots show coherent signals recovered or missed by each ranking, high-scoring false positives, boundary-dominated structure and highly variable unlabelled backgrounds. Human review times have not been measured. The full visual review and claim-to-evidence assessment are in [Completed V3 evidence](paper/v3/completed_evidence.md).

#### 6. Conclusions supported at this revision

V2 did not demonstrate an advantage over BLS at K=100: the compact hybrid recovered 28/300 catalogue-positive targets versus 33/300 for BLS, with paired difference interval [-13,+3]. V3 executes both unsupervised and semi-supervised methods on an unseen population, but its predefined primary hybrid recovers 24/300 versus BLS's 32/300 and requires more inspections at the predefined recovery target. Secondary affinity-only results warrant further study but do not establish superiority. No test objects pass the separate corrected significance threshold. The framework supplies interpretable measurements, controlled software diagnostics and unvalidated candidate prioritisation; reduced workload, astrophysical causation and new planetary discovery are not demonstrated. Any changes informed by V3 evaluation require another untouched sample for subsequent independent claims.

#### Code and data availability

The original TESS observations are publicly available through [MAST](https://archive.stsci.edu/missions-and-data/tess); catalogue references are obtained from the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/docs/API_TOI_columns.html). The local project contains MIT-licensed source, dependency locks, configurations, sample identifiers, frozen models and data provenance. A local release-candidate command assembles the study-specific package with SHA-256 manifests. It does not publish the package; no public URL or DOI has been assigned. Full photometry is not included in the compact release. The V2 archive is preserved separately. Reproduction commands, acquisition assumptions and pending experiments are documented in `RESEARCH_GUIDE.md#research-v3`.

#### References

- Astropy Collaboration et al. (2022). The Astropy Project: Sustaining and Growing a Community-oriented Open-source Project and the Latest Major Release (v5.0) of the Core Package. *The Astrophysical Journal*, 935, 167. [doi:10.3847/1538-4357/ac7c74](https://doi.org/10.3847/1538-4357/ac7c74).
- Breunig, M. M., Kriegel, H.-P., Ng, R. T., and Sander, J. (2000). LOF: Identifying Density-Based Local Outliers. *Proceedings of ACM SIGMOD*. [doi:10.1145/342009.335388](https://doi.org/10.1145/342009.335388).
- Crake, D. A., and Martínez-Galarza, J. R. (2023). Linking Anomalous Behaviour with Stellar Properties: An Unsupervised Exploration of TESS Light Curves. *arXiv preprint*, [arXiv:2301.10264](https://arxiv.org/abs/2301.10264).
- Dasgupta, M. (2025). CLARA: A Modular Framework for Unsupervised Transit Detection Using TESS Light Curves. *arXiv preprint*, [arXiv:2508.04722v4](https://arxiv.org/abs/2508.04722v4).
- Ginsburg, A., et al. (2019). astroquery: An Astronomical Web-Querying Package in Python. *The Astronomical Journal*. [doi:10.3847/1538-3881/aafc33](https://doi.org/10.3847/1538-3881/aafc33).
- Hippke, M., David, T. J., Mulders, G. D., and Heller, R. (2019). Wotan: Comprehensive time-series de-trending in Python. *The Astronomical Journal*. [doi:10.3847/1538-3881/ab3984](https://doi.org/10.3847/1538-3881/ab3984).
- Kovács, G., Zucker, S., and Mazeh, T. (2002). A box-fitting algorithm in the search for periodic transits. *Astronomy & Astrophysics*, 391, 369–377. [doi:10.1051/0004-6361:20020802](https://doi.org/10.1051/0004-6361:20020802).
- Lightkurve Collaboration et al. (2018). Lightkurve: Kepler and TESS time series analysis in Python. *Astrophysics Source Code Library*, ascl:1812.013. [Official citation record](https://lightkurve.github.io/lightkurve/about/citing.html).
- Liu, F. T., Ting, K. M., and Zhou, Z.-H. (2008). Isolation Forest. *Eighth IEEE International Conference on Data Mining*, 413–422. [doi:10.1109/ICDM.2008.17](https://doi.org/10.1109/ICDM.2008.17).
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830. [Publisher record](https://jmlr.org/papers/v12/pedregosa11a.html).
- Ricker, G. R., et al. (2015). Transiting Exoplanet Survey Satellite (TESS). *Journal of Astronomical Telescopes, Instruments, and Systems*, 1, 014003. [doi:10.1117/1.JATIS.1.1.014003](https://doi.org/10.1117/1.JATIS.1.1.014003).
- Savitzky, A., and Golay, M. J. E. (1964). Smoothing and Differentiation of Data by Simplified Least Squares Procedures. *Analytical Chemistry*, 36, 1627–1639. [doi:10.1021/ac60214a047](https://doi.org/10.1021/ac60214a047).
- Shallue, C. J., and Vanderburg, A. (2018). Identifying Exoplanets with Deep Learning: A Five Planet Resonant Chain around Kepler-80 and an Eighth Planet around Kepler-90. *The Astronomical Journal*. [doi:10.3847/1538-3881/aa9e09](https://doi.org/10.3847/1538-3881/aa9e09).
- Yu, L., et al. (2019). Identifying Exoplanets with Deep Learning III: Automated Triage and Vetting of TESS Candidates. *The Astronomical Journal*. [doi:10.3847/1538-3881/ab21d6](https://doi.org/10.3847/1538-3881/ab21d6).

Archive and implementation documentation cited above was consulted on 17 September 2026. The reference-verification supplement records the primary sources used and distinguishes preprints from journal articles.
<!-- END manuscript -->

<a id="abstract"></a>

## Abstract

<!-- BEGIN abstract -->
### Physics-Informed Machine Learning for Anomaly Detection and Candidate Transit Identification in TESS Light Curves

The Transiting Exoplanet Survey Satellite (TESS) has generated high-cadence photometric observations for millions of stars, creating an increasingly large search space for identifying transit-like signals and unusual stellar variability. While conventional transit-search algorithms such as the Box Least Squares method remain highly effective, automated machine-learning approaches can complement these techniques by identifying patterns that are difficult to specify explicitly and by prioritising unusual light curves for further investigation.
This work investigates a physics-informed machine-learning framework for detecting and characterising anomalous transit-like signatures in publicly available TESS light curves. The pipeline first performs photometric preprocessing, including quality filtering, normalisation, detrending, and segmentation. Candidate periodic signals are identified using conventional period-search techniques, while statistical and astrophysically motivated features describing transit depth, duration, periodicity, local variability, and signal morphology are extracted from each light curve.
These representations are subsequently analysed using unsupervised and semi-supervised anomaly-detection methods to identify observations that deviate significantly from dominant stellar variability patterns. Known exoplanet systems and labelled false-positive events are used as reference populations for evaluating whether the anomaly score provides additional discriminatory information beyond conventional detection statistics.
Particular emphasis is placed on interpretability rather than treating the machine-learning model as an independent discovery mechanism. The objective is to determine which photometric and temporal properties cause individual systems to be identified as anomalous and whether these properties correspond to physically meaningful transit characteristics.
The study demonstrates a computational framework in which machine learning acts as a candidate-prioritisation layer alongside established astronomical techniques, potentially reducing the number of light curves requiring manual inspection while retaining physically interpretable criteria for subsequent validation.
<!-- END abstract -->

<a id="paper-workflow"></a>

## Paper Workflow

<!-- BEGIN paper_workflow -->
### Preserved final paper workflow

The inspected independent result is archived in `paper/archive_2026-09-16`. The evaluated compact hybrid recovered 28/300 catalogue-positive hosts at K=100, versus BLS's 33/300. This result must not become untouched validation again after model choices are motivated by it.

The final reporting package is `paper/final`. Start with `manuscript.md`, `diagnostic_review.md`, `figure_captions.md` and `REPRODUCE.md`. It includes machine-readable tables, eight summary figures and ten diagnostic figures in both PNG/PDF, and copies of selected diagnostic photometry. The prior abstract and methods remain in the archive; the current `RESEARCH_GUIDE.md#abstract` is updated to the independent result.

From the repository directory in the recorded environment, reproduce all numerical reporting and figures with:

```powershell
python scripts/paper_report.py --reproduce --archive paper/archive_2026-09-16 --output paper/reproduction
```

The destination must not already exist. The command verifies the input archive and referenced photometry checksums, performs paired target bootstrap resampling with reranking, and regenerates the paper tables, figures and manuscript template. It never fits a new model or changes the original evaluated rankings. Recorded visual-review notes and captions are editorial supplements, not algorithmic discoveries; preserve them alongside regenerated outputs.

The archive contains frozen models, source snapshot, reporting scripts, tests, requirements, package versions, acquisition configurations, target IDs, original result tables and hashes. The full raw/processed photometry is referenced in the experiment workspace by checksum, rather than duplicated into the archive. A clean-machine reproduction therefore requires restoring those files and the recorded scientific environment. Selected diagnostic data are copied into the final report for convenient inspection.

The paired 95% interval for the primary difference is [−13, +3] hosts, with an observed difference of −5. It reflects resampling of evaluation targets and reranking while models remain fixed. It does not include uncertainty from fitting a different model, changing calibration samples, label errors or population-selection bias. It supports no claim of improved recovery or reduced human inspection time.

The software and result reporting are ready for author review. Journal formatting, author/affiliation details, any required data-release arrangements remain manuscript submission tasks. Visual morphology review is not independent astrophysical validation.

The literature review and reference verification were completed in the editorial revision of 17 September 2026. See `paper/final/references_verification.md` and `paper/final/editorial_revision_2026-09-17.json`. Regeneration reproduces the original manuscript template, not this later editorial revision. The public release URL/DOI remains unassigned.

#### V3 continuation (2 October 2026)

The V2 paper and archive above remain historical. Current development continues in `paper/v3/manuscript.md` under the exact submitted title/abstract. Follow `RESEARCH_GUIDE.md#research-v3` for the new semi-supervised experiment. Both previously inspected populations are development evidence for V3; new independent results have not yet been obtained.
<!-- END paper_workflow -->

<a id="research-v2"></a>

## Research V2

<!-- BEGIN research_v2 -->
### Frozen research extension

This extension preserves `experiments/default/outputs` as the descriptive baseline. Its outputs live under `experiments/research_v2/`. It implements new experiments; it does not assert that recovery improves.

#### Frozen development and independent evaluation

`config/research_v2.yaml` specifies a compact primary representation, five comparison representations, a 20% calibration fraction, a 0.95 redundancy threshold for the new representations, and an 80% BLS / 20% additional-anomaly allocation at budget 100. The compact hypothesis was motivated by earlier labelled development results. This is label-informed experiment selection; IF/LOF fitting, calibration, and redundancy removal do not use labels.

Targets are split deterministically into training and calibration groups; sectors from a target never cross the split. All usable training sectors fit median imputation, robust scaling, Isolation Forest and novelty-enabled LOF. Calibration uses one coverage-selected curve per calibration target. It fixes empirical score distributions for IF, LOF, BLS depth SNR and the ensemble. Unseen scores use midpoint empirical CDF values against those saved calibration arrays. Equal-weight IF/LOF percentiles form the ensemble; the hybrid averages the fixed BLS and ensemble percentiles. Evaluation batches never refit transforms or recompute percentile distributions. This calibration differs from the original transductive, within-batch rank normalization and must be described as a new experiment.

The frozen directory includes models, selected features and redundancy decisions, source snapshot, package versions, UTC freeze time, original configuration, protocol, training/calibration IDs, and all excluded development IDs. The original 996 targets are development data. Targets from earlier small and cached-probe samples are also excluded, even when absent from the current 996. Their inclusion in the exclusion list does not add them to model fitting. Model checksums, source fingerprints and scientific dependency versions are checked on loading. Existing frozen directories cannot be overwritten.

Development calibration diagnostics are produced, but these targets were already part of the inspected development population and were used to calibrate scores. **These diagnostics are not independent evaluation.** The new evaluation sampling plan uses sectors 14–26, seed 2027, requested counts 300 planet/candidate hosts, 300 false positives and 500 backgrounds, subject to actual availability. This changes the observing population; target disjointness does not remove selection bias or sector-dependent distribution shifts. Sampling is catalogue-stratified, while model fitting is label-free.

The initial `development_calibration` report uses the one-sector calibration rows. To test exposure on all available sectors of those same calibration targets without changing the fitted models or calibration arrays, run:

```powershell
..\.venv\Scripts\python.exe scripts/development_exposure.py --frozen experiments/research_v2/frozen --output experiments/research_v2/development_exposure
```

This additional comparison remains development evidence. Training-target scores are not substituted for unseen LOF scores.

##### First freeze of a new version

From the repository directory in PowerShell:

```powershell
..\.venv\Scripts\python.exe scripts/research_experiment.py freeze --config config/default.yaml --protocol config/research_v2.yaml --output experiments/research_v2/frozen
```

Do not repeat this command for an existing frozen version. Changes to the scientific source require a new version or restoring the saved source snapshot and recorded dependencies. Keep new versions distinct, and do not call a population independent after inspecting it for model selection.

##### Prepare a new target-disjoint evaluation sample

```powershell
..\.venv\Scripts\python.exe scripts/research_experiment.py prepare-evaluation --frozen experiments/research_v2/frozen --workspace experiments/independent_v2 --config-output config/independent_v2.yaml
```

This only creates the locked acquisition configuration and references the frozen exclusion list. It does not download observations or produce independent evidence. It refuses an existing evaluation workspace/config. If the configuration has already been prepared, continue with acquisition:

```powershell
..\.venv\Scripts\python.exe scripts/run_pipeline.py --config config/independent_v2.yaml --stage download --resume
..\.venv\Scripts\python.exe scripts/run_pipeline.py --config config/independent_v2.yaml --stage features --resume
..\.venv\Scripts\python.exe scripts/research_experiment.py evaluate --frozen experiments/research_v2/frozen --evaluation-workspace experiments/independent_v2 --output experiments/independent_v2/frozen_evaluation
```

Use only download and features stages for these new observations. The ordinary `all` command would fit models on the evaluation population and would not be this independent experiment. The features stage performs preprocessing and BLS as needed. Frozen evaluation checks the sampling plan, preprocessing and BLS configuration, and rejects any development-target overlap. It reports requested, analysed and missing targets. Download shortages are not filled with fabricated observations.

#### Coherence and compact representations

The baseline feature families are preserved. New `compact` and `extended` representations add:

| Feature | Definition and limitations |
|---|---|
| Event-depth relative MAD | Local out-of-transit median minus each event median; MAD divided by absolute median depth, with at least three measurable events |
| Event-duration relative MAD | Scatter of sampled half-depth widths divided by median width, with at least three measurable events; a proxy, not a fitted physical duration |
| Single-event power fraction | Maximum positive depth-squared × in-transit count / local MAD-squared contribution divided by the event total; a dominance proxy, not exact BLS power attribution |
| Local noise beta | Scatter of duration/2-bin mean flux divided by expected white-noise scatter; bins stay within photometric segments and use local out-of-transit points |
| Edge-to-centre depth ratio | Median-based outer-transit depth divided by centre depth; approximate flat-bottomed versus V-shaped morphology |
| Ingress/egress difference | Median flux difference between the two outer transit regions |
| Secondary scan depth and ratio | Strongest median dip on an 80-position orbital-phase grid outside the primary region, and its ratio to the primary depth |

The secondary scan is a coarse feature measurement, not an exhaustive secondary-transit search. Narrow secondary events can fall between trial centres. Maximizing over phases introduces selection effects; the feature is not calibrated significance. Event widths and noise beta can be affected by sampling, spots, variability, and remaining systematics. Missing measurements remain NaN and use the training-only feature contract. No proxy establishes planetary origin or causation.

Compact features omit the repeated generic variance/amplitude family. New compact/extended transforms further remove features with absolute pairwise Spearman correlation at least 0.95, using at least 20 jointly observed training rows and deterministic whitelist order. The report records which retained feature made each removed feature redundant. This feature-selection rule does not examine calibration/evaluation labels or scores. Legacy families retain their existing feature-selection behavior for comparison.

#### Exposure and search coverage

Every representation has an all-sector comparison and a coverage-selected single-sector comparison. Selection uses most valid cadences, then longest baseline, then smallest sector number. The selection rule never reads scores or labels. Both comparisons apply the same frozen model; this tests score aggregation exposure, not a model refitted to one-sector training data.

`metrics.csv` retains full-population recall and adds eligible-positive recall at the same inspection budgets. The eligible-positive denominator includes hosts whose representative catalogue period lies within the configured minimum and at least one selected sector's baseline-limited maximum. The ranking pool is unchanged: out-of-grid and missing-period hosts are not silently removed or recast as false positives. The eligibility table distinguishes missing periods. This is grid eligibility, not proof that transits occurred in the observed windows or completeness over all planets in a system.

#### Complementarity and uncertainty

Inspect the first 80 BLS-ranked targets, then the highest 20 ensemble-ranked targets not already selected, at an effective budget of 100. Smaller populations use floor(0.8 × effective budget) BLS slots. TIC order resolves ties. Export actual selected IDs, gains, losses, and net catalogue-host recovery against the same-budget BLS list.

The paired target bootstrap resamples per-target differences between the two fixed inspection lists, with 1,000 replicates and percentile 95% intervals. These are conditional descriptive intervals: the lists are fixed, models are not refitted, and selection/training uncertainty is not included. Counts reflect catalogue-positive hosts, not validated planet purity. Additional recovery does not establish reduced human review time. The allocation is frozen before new evaluation; changing it based on development results must be disclosed and tested on untouched data.

#### Real-light-curve injection validation

```powershell
..\.venv\Scripts\python.exe scripts/real_injection_recovery.py --config config/default.yaml --settings config/real_injections.yaml --output experiments/research_v2/injections
```

The default experiment uses six deterministically selected real targets, one sector each, three periods, three depths, two durations, and one randomized phase per case. Each of the 108 signals is processed with Savitzky–Golay and rolling-median detrending, giving 216 paired trials. Signals are trapezoids injected multiplicatively into copies of the raw photometry before preprocessing. Raw-file hashes are verified, and observation files are never modified. The existing rolling median is a robust comparator; this implementation does not add Wōtan as a dependency.

The noise and original uncertainties are retained, not resimulated. The signal family approximates morphology without limb darkening or a physical orbital fit. Original light curves can contain real variability and transits. Uninjected controls are therefore not guaranteed null examples or false alarms.

Outputs separate blind direct-period and harmonic retrieval, sampled event counts, grid eligibility, and paired depth attenuation at the known injected ephemeris. Depth attenuation regresses the injected/control detrended flux ratio against the injection template. This isolates preprocessing response more directly than comparing a possibly unrelated winning BLS depth to the injected depth. Trial failures are explicit; summary recovery rates condition on successful processing. The small default experiment is a validation pilot, not a survey-completeness estimate. Its output never enters real-candidate rankings.
<!-- END research_v2 -->

<a id="research-v2-validation"></a>

## Research V2 Validation

<!-- BEGIN research_v2_validation -->
### Research extension implementation validation

Implemented and exercised on 2026-09-13. The original larger-run scientific outputs remain under `experiments/default/outputs`; this extension writes separate artifacts.

- Test suite: 31 passed. Ruff passes for source, tests and scripts.
- Frozen model fitting: 796 targets. Separate development calibration: 200 targets, one curve per target for calibration distributions.
- Additional exposure diagnostics: all 269 available curves of those 200 calibration targets versus 200 coverage-selected curves.
- Independent exclusion list: 1,064 unique previously inspected targets, including the current 996 and additional targets from earlier experiments.
- Six representation families fitted. Compact retains 15 features after one redundant feature is removed; extended retains 33 after 16 redundant features are removed. The original all-feature family retains 41.
- Frozen-model serialization, disjoint-target rejection, label-free scoring, score-batch invariance, training-only redundancy selection, unchanged transform statistics, source-version rejection, deterministic exposure selection, complementary-list deduplication and raw-file preservation are covered by tests.
- The frozen model/package/source checks pass on the saved real-data bundle.
- The independent acquisition configuration is prepared at `config/independent_v2.yaml`. No new evaluation observations have been downloaded by this implementation run, and no independent performance result is claimed.

#### Development exposure diagnostics

These results involve previously inspected calibration targets, not an independent sample. At K=100, among 63 catalogue-positive targets:

| Exposure | BLS recovered | Compact hybrid recovered | 80/20 complementary list recovered |
|---|---:|---:|---:|
| All available sectors | 39 | 37 | 37 |
| Coverage-selected single sector | 37 | 35 | 36 |

The compact complementary list gains two hosts and loses four relative to BLS with all sectors, a net difference of −2. Its conditional paired-bootstrap 95% interval is [−7, 3]. For one sector, it gains two and loses three, net −1 with interval [−5, 3]. These intervals condition on fixed inspection lists and do not include model-fitting uncertainty. Neither comparison demonstrates improvement over BLS. Forty-five of the 63 positive reference targets meet representative-period grid eligibility under these comparisons; full-sample metrics retain all 63.

#### Injection pilot

All 216 trials succeeded, with 12 successful uninjected controls and 216 finite paired template-depth estimates. Each detrending method processes the same 108 signals in six real target light curves.

| Detrender | Direct period retrieval | Median paired depth bias |
|---|---:|---:|
| Savitzky–Golay | 60/108 (55.6%) | −7.3% |
| Rolling median | 55/108 (50.9%) | −1.6% |

The pilot suggests a depth-preservation/retrieval tradeoff, not a universal winner. Savitzky–Golay remains the frozen default; no independent outcomes were used to select it. Synthetic signal retrieval is not real-planet validation, detection at a calibrated false-alarm rate, or a survey-wide completeness estimate.

#### Artifact locations

- `experiments/research_v2/frozen/protocol.json`: fixed settings, IDs, hashes, source/dependency versions and selection history.
- `experiments/research_v2/frozen/feature_selection_*.csv`: selected, missing, disabled and redundant features.
- `experiments/research_v2/development_exposure/`: scores, metrics, eligibility, selected sectors, complementary lists and report.
- `experiments/research_v2/injections/`: every trial, uninjected controls, method summaries, selected source curves and injection protocol.
- `experiments/research_v2/implementation_validation.json`: implementation-run status.

Commands and detailed definitions are in [research_v2.md](#research-v2).
<!-- END research_v2_validation -->

<a id="validation"></a>

## Validation

<!-- BEGIN validation -->
### Verification record

This file records executed checks. The final small-sample results belong in the generated `outputs/research_summary.md`; no placeholder scientific results are supplied here.

#### Environment

Windows, Python 3.11.9, CPU. Dependencies installed successfully in the sibling `.venv` during development. Both the main scientific stack and optional PyTorch installed. The exact validated package set is captured in `requirements-lock.txt` and each run's metadata. Source Git repository initialized; a Git commit is reported only when one actually exists.

#### Real-data validation before the main experiment

Two public SPOC sector-1 light curves were downloaded with Lightkurve from MAST, with quality masking disabled at download to preserve the original arrays. Catalogue values came from the NASA TOI snapshot, not manually invented labels.

| TIC | Catalogue period (days) | Independent BLS period (days) | Relative period error |
|---|---:|---:|---:|
| 25155310 | 3.288790 | 3.289159 | 0.01122% |
| 261136679 | 6.267814 | 6.269787 | 0.03147% |

Both recovered the fundamental rather than requiring a half/double-period interpretation. The first diagnostic image was visually inspected: panels, axes, transit zoom, periodogram and metadata were readable, and transit dips remained after detrending. These deliberately selected known systems are software sanity checks, not evidence that anomaly detection adds value.

#### Synthetic checks

Initial injected period 3.2 days was recovered as 3.1987725 days. At injected depths 0.001, 0.003 and 0.010, recovered box depths were approximately 0.0008342, 0.0025102 and 0.0094475. This deliberately simple validation shows sensitivity and a measurable depth bias from the detrending/search setup; it does not establish survey completeness. Ground truth and numerical results are stored separately in `outputs/tables/injection_*`.

Tests exercise invalid-array masks, gaps, all detrending choices, duplicate times, missing versus invalid errors, injection recovery, physical proxies, IF/LOF score orientation, novelty scoring, feature whitelist, training-only imputation, target aggregation, unlabelled exclusion from AUCs, unavailable metrics, catalogue sample integrity, cache invalidation and an offline pipeline producing figures/tables/reports. Optional autoencoder testing checks finite nonnegative MSE, determinism and target-group separation.

The final suite passed **21 tests in 22.74 seconds**; Ruff reported no errors and all 42 Python files passed its format check. The single warning concerns Lightkurve's optional pixel-model dependency `oktopus`, which this light-curve pipeline does not use. All five notebook files passed nbformat validation. Regression tests cover the sampling-pool correction, opt-in catalogue-derived model proxies, and download failures with cached successes. The corrected sample was verified to contain 30 planet/candidate hosts, 30 false positives and 50 backgrounds, with 110 unique TICs and no duplicates. The originally failed labelled download succeeded on retry. This correction preserved the same seeded labelled samples and restored the intended control group.

#### External-access issues and fixes

The initial sandboxed Python request was blocked by the environment's network proxy. Authorized execution outside the network sandbox successfully reached NASA and MAST. The initially attempted `tess.stsci.edu` target-list hostname did not resolve. The implementation was corrected to use official MAST sector light-curve bulk manifests at `archive.stsci.edu`; their filenames define genuine observed TIC IDs. Manifest scripts are parsed, never executed. There is no synthetic or invented-catalogue fallback.

#### Scope limits

A separate nine-target cached real-data probe (three targets from each group) completed preprocessing, BLS, features, IF/LOF, evaluation, ablations, figure generation and reporting. Its 17 PNG and 17 PDF figures and feature table were checked; numeric feature values contained no infinities. This probe lives under `experiments/cached_probe/` and is not the primary result sample. Its initial configuration predates the default exclusion of catalogue-dependent physical proxies; its outputs are retained only as an engineering check.

Before evaluating the full sample, the input-coverage audit found that 11 of the 30 planet/candidate reference periods exceeded 12 days. Planet labels comprised 20 PC, 9 CP and 1 KP. Stellar radii were available for 28 planet/candidate and 28 false-positive targets but no backgrounds. The final default therefore excludes stellar-catalogue-dependent proxies from ML while retaining their extracted measurements, without selecting this policy on model performance.

The larger configuration has not been claimed as executed. Multi-sector aggregation is implemented and unit tested, but the main small experiment selects one sector per target. No GPU is required. The optional autoencoder is separately tested and disabled in the default experiment. No planetary validation, pixel-level centroid vetting, dilution correction, limb-darkened transit fit, occurrence-rate inference or external held-out ML generalisation claim is made.


#### Completed primary experiment (2026-09-09)

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
<!-- END validation -->

<a id="output-audit"></a>

## Output Audit

<!-- BEGIN output_audit -->
### Larger-experiment output audit

#### Correction follow-up (2026-09-13)

The two implementation issues below have now been fixed and the derived outputs regenerated from the same cached observations. The original audit below is historical; its pre-fix numbers are preserved for comparison. Original outputs are retained in `experiments/default/audit_snapshots/before_boundary_order_fix_20260913_182142/`.

- All 1,353 target-sector rows from 982 targets were retained; no feature-stage failures occurred.
- Every saved BLS trial and winning period respects both configured bounds and the individual baseline cap. Exactly seven winning periods changed.
- Every all-feature refit score exactly reproduces its primary score (maximum absolute difference zero), and every all-feature ablation metric exactly matches its primary metric. Evaluation uses round-trip float parsing to preserve score ties after CSV serialization.
- Corrected top-99 recovery is BLS 44/297, Isolation Forest 21/297, LOF 22/297, ensemble 24/297, hybrid 26/297. The primary and all-feature hybrid results are now both 26, rather than the pre-fix 25 versus 26.
- The interpretation limits remain: 71/297 representative host periods are outside the configured interval, usable sector coverage differs by group, and all five top hybrid candidates are unlabelled backgrounds. No independent generalisation or workload reduction is established. The corrected hybrid still does not outperform BLS in this comparison.
- All 24 tests pass. Source, tests and scripts pass Ruff. The smaller 110-target experiment was also regenerated and passed exact score/metric and strict period-bound checks. Repository-wide Ruff additionally reports existing notebook formatting issues, outside these changes.

Machine-readable post-fix verification: `experiments/default/outputs/tables/correction_verification.json`. Updated results: `experiments/default/outputs/research_summary.md`. Reproduce the checks using `python scripts/verify_output_corrections.py --config config/default.yaml`.

#### Original pre-fix audit

Audited 2026-09-13 against `RESEARCH_GUIDE.md#abstract`, the saved configuration and artifacts in `experiments/default/`. This audit inspected existing results and refitted models in memory for verification. It did not change the scientific outputs, model settings or primary rankings. Machine-readable checks are in `output_audit.json`.

#### Verdict

The outputs support the revised abstract's **descriptive, unsupervised candidate-ranking framework**. They do not establish improved planet recovery, reduced inspection workload or independent generalisation. The main ranking results are numerically reproducible. Two implementation inconsistencies should be corrected before treating all tables as final paper results: ablation fitting order and strict BLS upper-period enforcement.

#### Verified data and model integrity

The configuration requests 300 planet/candidate hosts, 300 false positives and 500 backgrounds. The eligible catalogue/observing pool contained only 196 false positives; this shortage was explicitly logged. Consequently the actual selected sample contains 996 targets, not 1,100.

| Population | Selected | Analysed unique targets |
|---|---:|---:|
| Planet/candidate | 300 | 297 |
| False positive | 196 | 193 |
| Background/unlabelled | 500 | 492 |
| Total | 996 | 982 |

There are 1,353 target-sector feature rows, with no duplicate TIC-sector keys. The 14 targets absent from the final feature table are all accounted for by download failures. There are 25 failed download records for 25 distinct targets: 11 of those targets still supplied another usable sector. Preprocessing, BLS and feature-stage failure tables are empty. A completed pipeline run therefore does not mean every requested download succeeded.

Checks confirmed:

- Feature and score tables have identical TIC-sector keys, and labels match the selected catalogue sample.
- All 1,353 processed curves have aligned arrays, increasing unique times, finite detrended flux, positive trends and valid positive flux errors. Configured quality bits are filtered, and detrended flux equals normalized flux divided by the trend.
- No infinite numeric feature values were found. The transformed ML matrix is finite and matches its saved row order.
- The model uses 41 explicitly selected features. TIC, TOI, sector, labels, disposition and catalogue period are absent from the model feature list. Stellar-catalogue-dependent radius and duration-consistency proxies are excluded as configured.
- Every BLS search used measured errors. Saved IF scores match negative `score_samples`; saved LOF scores match negative fit-time outlier factors. The saved LOF reference matrix matches transformed training features.
- Equal-weight percentile ensemble and hybrid formulas reproduce the saved scores.
- Unique-target scores reproduce the documented per-method maximum across sectors.
- Every saved main-model top-K count, precision, recall, positive-rank summary, ROC-AUC and average precision was independently recomputed from the target rankings and agreed.
- Refitting on the original feature-table row order reproduces the saved primary model scores.
- All four ablation families, PCA coordinates for 1,353 rows, 250 feature-score correlation rows and 21 PNG/PDF figure pairs are present. One top-candidate diagnostic was visually inspected; this is not exhaustive astrophysical vetting of every target.

#### Main scientific results

At the top 99 of 982 targets (approximately 10%):

| Method | Catalogue-positive hosts recovered | Recall | ROC-AUC | Average precision |
|---|---:|---:|---:|---:|
| BLS depth SNR | 44/297 | 14.81% | 0.6434 | 0.5991 |
| Isolation Forest | 21/297 | 7.07% | 0.5382 | 0.4774 |
| LOF | 22/297 | 7.41% | 0.4226 | 0.4385 |
| Anomaly ensemble | 24/297 | 8.08% | 0.4843 | 0.4615 |
| Hybrid | 25/297 | 8.42% | 0.5663 | 0.5174 |

Recovery uses all 297 catalogue-positive hosts. The binary AUC/AP comparison uses a different subset: 169 hosts with a CP/KP disposition versus 193 FP/FA hosts (362 total). The 128 PC-only hosts and 492 unlabelled backgrounds are excluded from binary AUC/AP. These denominators must remain distinct in the paper.

BLS depth SNR and the ensemble have target-level Spearman rho = 0.330048. The scores therefore differ, but this correlation does not show that anomaly scores add useful independent discrimination. At the stated inspection budget, the ensemble and hybrid recover fewer catalogue-positive hosts than BLS. Maximum BLS power and depth SNR are identical in this SNR-objective experiment; they are not two independent baseline methods.

#### Corrections needed before final paper tables

##### 1. All-feature ablation does not reproduce the primary model

Training reads the original feature table. Evaluation instead refits ablations from the score table, which has been sorted by ensemble score. With a fixed random seed, Isolation Forest's sampled row indices refer to different objects after reordering. This changes the fitted finite ensemble and consequently some IF, ensemble and hybrid rankings.

The cause was verified in both directions: original-order refitting reproduces the primary scores; sorted-score-order refitting reproduces the saved all-feature ablation metrics. Nine method/cutoff combinations have different recovered counts. For example, at K=99 the primary IF recovers 21 while its all-feature ablation recovers 22; primary hybrid recovers 25 while the all-feature ablation recovers 26.

The main metrics remain valid. However, feature-family comparisons currently include a change in fitting order as well as representation. Use the same original target-sector order for every family, and verify that the all-feature ablation exactly reproduces the primary result. Prefer reusing the primary all-feature scores for that control. Regenerate ablation tables and the research report after correction. Do not claim a physics-feature benefit from the current ablation alone.

##### 2. Seven winning BLS periods slightly exceed the intended cap

Astropy's automatically sampled grid can place its last period just beyond the supplied upper endpoint. The code uses the resulting power array without explicitly removing out-of-range trials. Seven winning periods exceed `min(12 days, baseline/2)` by approximately 0.0116–0.0225 days. This is a small discretisation issue, not an array-alignment or flux-quality failure, but the output does not strictly satisfy the stated search cap.

Affected TIC-sector pairs: 42054565–3, 451599528–12, 148273382–7, 183537481–2, 159707889–11, 192559318–9 and 255400005–12. Exact values are in `output_audit.json`.

Explicitly constrain the trial-period array before selecting peaks and harmonics, add a boundary regression check, and regenerate dependent results. The effect of this correction on rankings has not been measured in this audit.

#### Interpretation limits relevant to the abstract

- The experiment fits and ranks the same unlabelled sample. Reference labels support retrospective evaluation, not semi-supervised learning or independent predictive validation.
- Physics-informed means feature engineering. No physical equations are enforced during training. The stellar duration-consistency feature is entirely missing here; the default physics family is chiefly morphology plus the depth-derived radius ratio.
- 71 of the 297 hosts' representative catalogue periods fall outside the nominal 0.5–12-day grid. A host label also does not guarantee that a transit occurred in the selected sector. Known-host recovery is not a measured planet-detection completeness rate.
- Repeated sectors are correctly aggregated for target-level metrics, but observing opportunities differ: two sectors are available for 132/297 planet hosts, 93/193 false positives and 146/492 backgrounds. Both maximum-score selection and fitting multiple rows per target can introduce observing-selection effects.
- The feature-score correlation table operates on target-sector rows. Its p-values should not be treated as independent-target inference because sectors from a common TIC can be correlated; target-level aggregation or clustered uncertainty estimates are needed for inferential use. Exploratory multiple-testing caveats also apply.
- All five top hybrid-ranked objects are unlabelled backgrounds, with fitted depths approximately 5–31%. The inspected leading target has deep repeated dips, a second dip away from phase 0.5, and visible detrending ripples. These observations warrant manual vetting; they do not justify calling these objects planet candidates. A secondary-eclipse proxy fixed at phase 0.5 can miss the second dip visible in this example.
- Correlations, PCA, ablations and diagnostic plots describe associations. They do not provide causation, formal per-object model attribution or calibrated anomaly significance. No study of actual human inspection time or independent generalisation has been performed.

#### Supported paper wording

“In a descriptive analysis of 1,353 TESS light curves from 982 targets, BLS depth-SNR ranking recovered 44 of 297 catalogue-positive hosts within the top 99 targets, compared with 24 for the anomaly ensemble and 25 for the hybrid. At this inspection budget, the tested anomaly-based rankings did not improve known-host recovery over BLS. The framework provides interpretable diagnostics for investigating high-scoring light curves; independent evaluation is required to assess generalisation and inspection-workload reduction.”

These numbers describe the currently saved outputs. Final publication values should be regenerated after the two implementation corrections above.
<!-- END output_audit -->

<a id="historical-repository-inventory"></a>

## Historical repository inventory

The original inventory below records the earlier layout; its old documentation paths are historical, not current links.

```text
.gitignore
LICENSE
README.md
config/default.yaml
config/sanity.yaml
config/small_test.yaml
docs/methodology.md
docs/research_questions.md
docs/validation.md
notebooks/01_data_exploration.ipynb
notebooks/02_bls_analysis.ipynb
notebooks/03_feature_analysis.ipynb
notebooks/04_anomaly_detection.ipynb
notebooks/05_results.ipynb
pyproject.toml
requirements-lock.txt
requirements.txt
scripts/abstract_results.py
scripts/create_support_files.py
scripts/download_sample.py
scripts/evaluate.py
scripts/extract_features.py
scripts/generate_figures.py
scripts/generate_report.py
scripts/injection_recovery.py
scripts/preprocess.py
scripts/run_bls.py
scripts/run_pipeline.py
scripts/train_models.py
scripts/validate_cached_subset.py
src/tess_anomaly/__init__.py
src/tess_anomaly/anomaly/__init__.py
src/tess_anomaly/anomaly/autoencoder.py
src/tess_anomaly/anomaly/ensemble.py
src/tess_anomaly/anomaly/isolation_forest.py
src/tess_anomaly/anomaly/lof.py
src/tess_anomaly/bls.py
src/tess_anomaly/cache.py
src/tess_anomaly/catalog.py
src/tess_anomaly/config.py
src/tess_anomaly/dataset.py
src/tess_anomaly/download.py
src/tess_anomaly/evaluation.py
src/tess_anomaly/features.py
src/tess_anomaly/logging_utils.py
src/tess_anomaly/pipeline.py
src/tess_anomaly/plots.py
src/tess_anomaly/preprocessing.py
src/tess_anomaly/utils.py
tests/test_autoencoder.py
tests/test_bls.py
tests/test_cache.py
tests/test_catalog.py
tests/test_download.py
tests/test_evaluation.py
tests/test_features.py
tests/test_models.py
tests/test_pipeline.py
tests/test_preprocessing.py
```

<a id="consolidation-provenance"></a>

## Consolidation provenance

Original source SHA-256 values before consolidation (2026-10-12):

| Former file | SHA-256 |
| --- | --- |
| `abstract.md` | `ff5c6de6ce9def3a5492da7ac2959577640469afafea6071ade919be2dcbd5f3` |
| `abstract_evidence_plan.md` | `2a06f679c8806b785c39547a1f03e96ae914f324d1d6c5c82f29408e47b71dfa` |
| `github_release.md` | `aea7f7f35d4bedf24a0eb62f0de099aa936dbb8fdeb44ca5a8cbc7422569ce6a` |
| `implementation_v3.md` | `8dbfe5b36393f6a83e24354c6ef8c107135187dd5415953a034695072f57e750` |
| `manuscript.md` | `fb4b2a3fcbe323443aaa03ab5b722d9b04fb2061f55098ba3594b918853c4247` |
| `methodology.md` | `4352b58fbaa9c79e4c4f0bb460c23237ac53401b375db36a5c68610c6471d7fc` |
| `output_audit.json` | `3f8d2e8df0d700d522eb6d92938687536a5aa69145b82b80e24400ebb5646840` |
| `output_audit.md` | `b7c4ee18f3ba8497efe567a496c5f0f90f11f478c722430355b89a642fc76751` |
| `paper_workflow.md` | `c2b9d4aa143027f3ff5afc58f55738203b36191d3fb04420b7cd150db54660bf` |
| `repository_files.txt` | `cc4206339ecfc4f412df922413e0866c1832007ece2739a451429c66dbe3a045` |
| `research_questions.md` | `78d8a26c797c9ca5b5ab98456e843fc4d568942b85a64feae14586c97e6a01c6` |
| `research_v2.md` | `680d1caaee289e3db2bfbd7d65d7d392fcf6426037d20ecbdf2b64ce068f1c83` |
| `research_v2_validation.md` | `c4031db5e23aa18eb5b3c5b3f25d8f660707304733903e722f61fce8b49dadcb` |
| `research_v3.md` | `5afc59201f2ff5405c3c1016042dbca0271f257549cae9e42a00448231e79ef4` |
| `submitted_research_specification.md` | `d6725b5382eda8eb03da895429046acb9fefd66ae99acc5936b1bb862e28df09` |
| `validation.md` | `7f69da38e8d874c4bbbadf001abc2bc44de624504b5291ee5307a5f5ab5f6efa` |
