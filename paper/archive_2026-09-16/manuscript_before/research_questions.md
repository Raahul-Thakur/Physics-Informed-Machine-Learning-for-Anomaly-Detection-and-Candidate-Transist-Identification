# Research questions and planned comparisons

1. **RQ1:** Do anomaly scores rank known transit-hosting systems differently from the broader observed population? Compare class distributions and known-host recovery; include false positives as their own group.
2. **RQ2:** How strongly do anomaly scores correlate with BLS power and depth SNR? Report Spearman correlations and scatter; note default SNR-power redundancy.
3. **RQ3:** Does a fixed BLS/anomaly hybrid improve top-ranked known-host recovery over BLS alone? Report improvements, ties and degradations without selecting a favourable formula after observing labels.
4. **RQ4:** Do astrophysical morphology/consistency features improve rankings relative to generic statistics? Compare four predeclared feature families; audit missingness and observing-property confounding.
5. **RQ5:** Which photometric and temporal properties are associated with high anomaly scores? Inspect feature correlations, PCA, top-target tables and diagnostic light curves, including high-ranked binary/systematic cases. These are associations, not causal explanations or formal per-object model attribution.
6. **RQ6:** Can anomaly-based or hybrid prioritisation reduce manual inspection workload while retaining useful candidates on an independent evaluation population? Current fixed-budget recovery metrics describe the same unlabelled sample used for fitting and do not establish such a reduction or generalisation.

The current experiment is descriptive validation of a research pipeline. Before paper-level inference, lock a target-disjoint evaluation sample, uniformly obtain stellar metadata, specify primary K and confidence-interval procedures, and assess selection and detection biases. A negative result is scientifically informative: it can identify the limits of unsupervised anomaly prioritisation and which false positives it promotes.
