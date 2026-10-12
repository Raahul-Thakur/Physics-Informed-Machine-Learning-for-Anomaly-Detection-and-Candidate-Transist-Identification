# Recorded diagnostic review

Review mode: assistant-assisted visual inspection of all ten saved diagnostic figures and their extracted measurements, on 2026-09-16. This is not expert astrophysical vetting. No external catalogue identity or discovery claim is inferred from appearance alone.

The selection rule is recorded in the input archive's `reporting_plan.json`. It was fixed after aggregate results were known, before these plots were inspected. Two objects were selected from each requested category using rank and TIC tie-breaks. These ten illustrations do not estimate the prevalence of any failure mode. Target ranks use method-specific maxima across sectors; the plotted sector follows the category's selection rule. Period comparisons below use representative catalogue periods, not every planet in each system.

## Selected by both BLS and hybrid

**TIC 164173105, sector 16 — [diagnostic](figures/diagnostics/both_tic164173105_s16.png).** BLS rank 4, hybrid rank 10. The raw and detrended curves show large, smooth, repeating variability. The fold is broad and rounded rather than an isolated short dip on a flat baseline. BLS selects 0.585768 days, versus the representative catalogue period of 3.072643 days. Event-depth relative MAD is 0.429 and local-noise beta is 5.41. These measurements and the visible waveform demonstrate that selecting a catalogue-positive host does not establish recovery of its catalogued transit. The physical origin of the variability is unresolved here.

**TIC 236387002, sector 24 — [diagnostic](figures/diagnostics/both_tic236387002_s24.png).** BLS rank 31, hybrid rank 16. Several narrow dips recur in both raw and detrended photometry; the zoomed fold has a well-defined trough. The fitted period, 7.193160 days, is close to the representative 7.200861 days. Event-depth relative MAD is 0.0084. Upward spikes are also visible. The full-phase median bins dilute the narrow dip, which remains clear in the transit zoom; the binning itself must not be treated as a nondetection. The observed recurrence is consistent with a coherent transit-like signal, without independent planetary validation.

## BLS-only top-100 hosts

**TIC 86396382, sector 20 — [diagnostic](figures/diagnostics/bls_only_tic86396382_s20.png).** BLS rank 40, hybrid rank 164. Many dips recur against a relatively stable baseline; the fold has a broad bottom and repeatable ingress/egress structure. The fitted 1.091407-day period closely matches the representative 1.091430 days. Event-depth relative MAD is 0.0195 and local-noise beta is 1.24. The frozen ensemble score is 0.525. This is an example of a coherent catalogue-period signal that is not highly anomalous under the fitted feature population; the figures do not establish which individual feature caused its rank.

**TIC 27848472, sector 26 — [diagnostic](figures/diagnostics/bls_only_tic27848472_s26.png).** BLS rank 41, hybrid rank 167. Repeated dips and a well-defined folded transit are visible. The fitted 1.846669-day period closely matches 1.846834 days. Event-depth relative MAD is 0.0180 and the frozen ensemble score is 0.510. Together with TIC 86396382, this illustrates a possible tradeoff between selecting unusual photometry and retaining otherwise regular transit-like systems. This is an association across selected examples, not causal model attribution.

## Hybrid-only top-100 hosts

**TIC 202426247, sector 15 — [diagnostic](figures/diagnostics/hybrid_only_tic202426247_s15.png).** BLS rank 107, hybrid rank 49. The raw curve has strong smooth variability. Much is removed by detrending, but structured residuals and sharp behavior near segment boundaries remain. The strongest BLS period is 11.784928 days, far from the representative 1.066208 days. The event-dominance proxy is 0.802 and local-noise beta is 7.38; depth-consistency is unavailable. This is an additional host selected by hybrid ranking, but the selected signal is not demonstrated to be the known planet's transit. Detrending-boundary effects and residual variability are plausible contributors requiring further checks, not established causes.

**TIC 168699373, sector 23 — [diagnostic](figures/diagnostics/hybrid_only_tic168699373_s23.png).** BLS rank 133, hybrid rank 54. Repeated dips are visible despite a noisier baseline; the folded transit is resolved. The fitted 4.298504-day period is close to the representative 4.301197 days. Depth-consistency MAD is 0.0380, local-noise beta 1.25, and frozen ensemble score 0.9275. This provides a contrasting hybrid-only example with a coherent signal near the catalogue period. It does not establish an overall recovery benefit: gains must be weighed against the BLS-only losses.

## Catalogue false positives

**TIC 159510109, sector 15 — [diagnostic](figures/diagnostics/false_positive_tic159510109_s15.png).** BLS rank 3, hybrid rank 1. The light curve contains two deep dips and a shallower dip between them. The BLS period of 8.478031 days is close to half the representative 16.948709 days. The folded curve mixes distinct depths; the odd/even flux difference is about 0.132. Broad brightening shoulders appear around the deep events after detrending. This eclipse-like morphology illustrates that extreme anomaly scores can accompany known false positives and harmonics. The plot alone does not establish the system's detailed astrophysical configuration.

**TIC 420645189, sector 25 — [diagnostic](figures/diagnostics/false_positive_tic420645189_s25.png).** BLS rank 42, hybrid rank 8. One dominant deep event is visible over the observed baseline, with a brightening shoulder in detrended flux. The selected 11.764467-day period is not the representative 48.534039-day period, which lies outside the search range. The dominance proxy is 0.999994 and local-noise beta is 7.63. Folding can make a single strong event appear like a clean transit; the time-domain plot and event count are therefore essential. Periodicity of the dip is not established by this figure.

## Highest-ranked unlabelled backgrounds

**TIC 240947891, sector 17 — [diagnostic](figures/diagnostics/background_tic240947891_s17.png).** BLS rank 1, hybrid rank 2. The raw curve has repeated very deep dips with shallower intervening minima. Detrending leaves substantial structured modulation. The BLS depth is about 0.414, and the secondary-scan depth ratio is 0.193. The large amplitude and multiple minima are eclipse-like features, but this object remains unlabelled in the experiment; it is not a validated binary or planet discovery.

**TIC 445133704, sector 17 — [diagnostic](figures/diagnostics/background_tic445133704_s17.png).** BLS rank 2, hybrid rank 3. Large-amplitude continuous periodic modulation and multiple alternating minima are visible in the full fold. The BLS depth is 0.138; the secondary-scan depth ratio exceeds one (1.21). The selected transit zoom shows only one part of this richer waveform. Such morphology can receive a high anomaly rank without demonstrating an isolated planetary transit. A harmonic interpretation and alternative astrophysical explanations require independent follow-up.

## What the review supports

The selected examples show regular catalogue-period dips among BLS-only hosts, both coherent and mismatched signals among hybrid-only hosts, and extreme or event-dominated morphology among highly ranked non-positive references. These are descriptive observations consistent with anomaly ranking favoring unusual photometric properties. They do not identify causal feature contributions, establish calibrated significance, validate new planets, or quantify a manual-workload reduction.

The main 28-versus-33 comparison remains a count of catalogue-positive hosts in inspection lists. This review strengthens the reason to avoid calling it a count of validated planet detections. A future ephemeris- and signal-matched recovery study should use a newly defined protocol and, if tuned using these findings, another untouched evaluation population.
