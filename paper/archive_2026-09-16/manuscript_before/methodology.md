# Methodology

## Scope and terminology

The implemented experiment uses unsupervised anomaly detection. Catalogue labels are reserved for evaluation; a separate novelty-scoring helper does not establish a semi-supervised experiment. Physics-informed means astrophysically motivated features such as transit depth, duration, morphology and approximate radius ratio, rather than physical equations enforced during training. Stellar-catalogue-dependent radius and duration-consistency proxies are extracted when possible but excluded from default ML inputs because measurement availability differs between groups.

High anomaly scores describe unusual feature-space observations relative to the fitted reference population. They are not calibrated statistical significance. Feature correlations, ablations, PCA and diagnostic reports examine properties associated with high anomaly scores; they do not establish causation or provide formal per-object model attribution. The primary models fit and rank the same unlabelled sample. Reduced manual inspection workload and generalisation remain research questions requiring independent evaluation.

## Population and unit of analysis

The experiment is a seeded, observing-selected, catalogue-stratified reference experiment, not a blind occurrence-rate survey. NASA TOI snapshot labels are CP/KP (confirmed/known), PC (candidate), FP (false positive), FA (false alarm) and ambiguous classes. Background means no TOI entry in the archived snapshot. It does not imply the absence of a transiting planet. Multi-disposition hosts with both positive and false-positive entries are excluded as ambiguous. Target properties use the first TOI entry; all entries are retained for period checks.

Features are measured per target-sector. Scores are aggregated per unique TIC by maximum across sectors for each method. Cross-method sector selection can differ; extra sectors confer extra opportunities for extreme scores. No sector is treated as an independent star in recovery metrics. The primary descriptive model fits the full unlabelled sample; claims about predictive generalisation require a separate target-disjoint experiment.

## Preprocessing

Input PDCSAP flux is in electrons/second; times are BTJD in days. Discard nonfinite times/flux, nonpositive flux, partially invalid reported errors and selected quality bits. Entirely absent uncertainties remain missing and cause an explicitly recorded unweighted BLS search. Sort times and retain the first exact duplicate. Cadence arrays always share masks and ordering.

Normalize by the positive median flux, y_i=f_i/median(f). Split where consecutive times differ by more than the configured gap. For each segment use median normalization, a rolling median, or a second-order Savitzky–Golay trend with odd window approximately window_days/median_cadence. Short segments fall back to a constant median.

With transit preservation enabled, repeat trend fitting three times, temporarily masking residuals beyond 3 robust standard deviations only in the trend input. Interpolate the masked trend input within each segment; never fill observational gaps in the science time series. Divide normalized flux and errors by the trend. Dips are not deleted. This procedure still can distort long/low-SNR transits and must be tested with injections across duration and window choices.

## BLS

Astropy `BoxLeastSquares` fits a periodic box to weighted photometry. At trial period P, duration D and epoch t0, the box separates in-transit and out-of-transit cadences, estimates their level difference δ and its uncertainty σδ, and maximizes either δ/σδ (`snr`) or the BLS likelihood objective. The default SNR objective makes maximum power and depth SNR identical.

The duration-driven automatic grid uses Astropy's frequency-factor control. Small factors produce finer sampling; the initial factor 5 is an economy setting and is not a guarantee of recovery at every phase. Search periods are capped by baseline/min_transits, with min_transits=2. This is a necessary baseline condition, not a guarantee of two observed events. The expected number counts transit centres within the time range; observed events count distinct epochs with at least one in-transit cadence and do not guarantee adequate event coverage.

The robust periodogram peak statistic is

    Z_BLS = (max(power) - median(power)) / [1.4826 median(|power - median(power)|)].

It is an empirical prominence measure, **not** a normal-tail significance or false-alarm probability. Constant power yields missing Z. The second peak is a local maximum outside a main-peak width heuristic ~3PD/baseline; it may still be a harmonic. P/2 and 2P searches are reported only within the configured period range. Catalogue period checks calculate |P_recovered-P_catalogue|/P_catalogue, and the minimum relative error to {P/2,P,2P}. Search inputs never contain the catalogue period.

Signed folded time is ((t−t0+P/2) mod P)−P/2. Plot bins use medians and never feed the search. Zoom limits use the measured duration. A box model does not distinguish planets from binary eclipses or instrumental dips.

## Statistical and physical features

Flux features use detrended relative flux: mean, median, population variance/standard deviation, min/max, peak-to-peak, IQR, skewness, excess kurtosis and RMS about unity. Robust MAD is 1.4826 median(|x−median(x)|). Successive differences exclude segment boundaries; point-to-point scatter is MAD(Δx)/sqrt(2), difference RMS is sqrt(mean(Δx²)), and median absolute successive difference is median(|Δx|). Percentile amplitude is q95−q5. Duty cycle is min(1,N median_cadence/(baseline+median_cadence)); it is an approximate sampling occupancy, not a transit completeness estimate.

Transit morphology uses |folded_time|<D/2 and an out-of-transit buffer |folded_time|>D. Medians require at least three points. Measured depth is out-median minus in-median. Asymmetry compares pre-centre and post-centre in-transit medians; it is a proxy, not fitted ingress/egress timing. Odd/even differences compare alternating-event medians. Significance uses between-event scatter with at least two measurable events of each parity, preventing cadence-count inflation from being the sole uncertainty estimate. These small-sample proxy uncertainties are approximate. Secondary depth compares the out-of-transit median to a D-wide window at phase 0.5; eccentric binaries can have secondary eclipses elsewhere. No arbitrary V-shape feature is supplied.

For 0<δ<1, radius-ratio proxy k≈sqrt(δ). With a measured Rstar>0, Rp_proxy=Rstar sqrt(δ), converted from solar to Earth radii using Astropy constants. Assumptions: dark occultor, unblended flux, non-grazing transit, negligible limb-darkening effects. This is not a validated planet radius.

With measured positive Mstar and Rstar, a=(G Mstar P²/(4π²))^(1/3), and the circular central small-companion duration is Dcentral≈P/π asin(Rstar/a). Store D/Dcentral only if 0<Rstar/a<1. Missing mass is never inferred from a generic constant. Eccentricity, impact parameter, dilution, stellar-parameter errors and finite companion radius can invalidate this approximation. Catalogue availability patterns can leak source selection through missingness even when explicit labels are excluded.

## Feature preprocessing and anomaly models

An explicit family whitelist excludes TIC, sector, TOI, disposition and catalogue periods. Replace infinities with missing, drop features above the missing-fraction threshold and constant features, median-impute remaining features, then use median/IQR RobustScaler (or StandardScaler). Save feature ordering and fitted transform. Transforming unseen data does not refit preprocessing. Primary fitting is on the full unlabelled reference population.

The default additionally excludes the stellar-catalogue-dependent radius-in-Earth-units and duration-consistency proxies from model fitting, while preserving their measured values in the feature table. In the initial sample, controls have no uniformly acquired stellar radii/masses, so imputation patterns could expose catalogue selection. `models.use_stellar_catalog_features` is an explicit opt-in for future samples with uniformly sourced stellar metadata. This choice is based on input coverage, not ranking results. The default physics family still contains transit morphology and the transit-depth radius-ratio proxy.

Isolation Forest uses random feature-space partitions. Short average isolation paths imply anomalies; use **negative `score_samples`** so larger values mean more anomalous. LOF compares a point's local reachability density to that of its neighbours. Primary fit-time LOF is `novelty=False` and uses **negative `negative_outlier_factor_`**. The separate novelty helper fits `novelty=True` and scores only excluded, unseen points. Neighbour count is capped at N−1. Contamination affects threshold labels, not the orientation of ranking scores.

The optional CPU autoencoder has widths d→64→32→8→32→64→d, ReLU hidden activations and linear output. Adam minimizes mean squared reconstruction error; early stopping uses a deterministic target-group validation split. A separate AE feature transform is fitted only on those training groups, then applied unchanged to validation and score rows. Anomaly score is mean_j (x_j−xhat_j)². Validation losses monitor reconstruction, not planet classification accuracy; scientific evaluation remains descriptive. Small samples and high-dimensional spaces can overfit.

## Ensemble, hybrid and ablations

Percentile r_i=average_rank(score_i)/N, with average ranks for ties. Equal-weight ensemble is the mean percentile of enabled IF, LOF and optional AE scores. Hybrid is (percentile(depth_SNR)+percentile(ensemble))/2. The formula is fixed without fitting evaluation labels. A combined ranking is not presumed superior.

Four independently fitted representations are compared: generic statistics/observing properties; BLS quantities; transit morphology and physical proxies; all features. Missing/constant features are handled separately for each family. This ablation tests representations but is not a causal estimate of physics benefit; catalogue-dependent measurements and correlated features are confounders.

Every family uses the original feature-table fitting order and the same configured random seed. The all-features refit must reproduce the primary model; sorting by anomaly score before fitting changes Isolation Forest's sampled row identities and is not an acceptable ablation comparison.

Automatic BLS trial periods are explicitly filtered to the configured minimum and the smaller of the configured maximum and baseline/minimum-transits cap before power evaluation. The automatic grid's rounded endpoint is not allowed to extend the search interval.

## Evaluation and uncertainty

Sort descending by score; deterministic TIC order breaks exact ties. Let N+ be catalogue-positive targets and H_K their count among the top min(K,N): catalogue-positive Precision@K=H_K/min(K,N); Recall@K=H_K/N+. Top 5%,10%,20% use ceil(fN). Report requested and effective K, mean/median positive rank, and undefined denominators explicitly. These precision values are known-host yield, not true planetary purity.

ROC-AUC and average precision are calculated only on CP/KP hosts versus FP/FA hosts and only when both classes exist. PC-only and unlabelled background do not enter these binary metrics. Average precision is the sklearn non-interpolated recall-weighted precision summary, not trapezoidal PR-AUC. Spearman correlations report finite-pair counts. Mann–Whitney tests compare each class against the rest; p-values are exploratory, uncorrected for multiplicity, and not sufficient evidence for a scientific claim. Target bootstrap confidence intervals, matched controls and a locked external evaluation are recommended next steps.

PCA is fitted to the scaled numeric feature space for inspection, with variance fractions and loadings exported. It does not validate astrophysical separation. Top-target feature tables and six-panel diagnostic figures support manual review but provide no planetary validation.

The generated report counts hosts whose representative catalogue period is outside the configured interval; this is not completeness over every planet in multi-planet systems, and individual-sector baseline caps restrict coverage further. It also tabulates usable sector counts by reference group. Max-across-sector ranking creates unequal opportunities for high scores when coverage differs. These comparisons are not exposure-matched. Top hybrid-ranked backgrounds remain unlabelled inspection candidates, not validated planets. Independent evaluation must account for search coverage and observing exposure before generalisation or reduced workload can be claimed.

## Reproducibility and integrity

Store source catalogue snapshots, observing manifests, requested IDs, original FITS/NPZ, intermediate photometry, BLS caches, configuration, dependency versions and UTC run metadata. Scientific cache keys include input bytes, relevant parameters and source code hash. Original FITS download caching is separate. Individual target failures are explicit and contribute to sample attrition. A global stage failure raises an exception and cannot masquerade as a successful experiment. Synthetic injection truth is stored separately and never substitutes for real archive failures.

Sources: [Astropy BLS documentation](https://docs.astropy.org/en/stable/timeseries/bls.html), [NASA TOI definitions](https://exoplanetarchive.ipac.caltech.edu/docs/API_TOI_columns.html), [Lightkurve downloads](https://lightkurve.github.io/lightkurve/reference/search.html).
