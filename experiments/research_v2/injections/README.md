# Real-noise injection validation

Attempted 216 trials; 0 failed. Failures remain explicit in injection_trials.csv; summary recovery rates condition on successful processing.

Identical trapezoid signals and phases are added multiplicatively before preprocessing for both detrenders. Original flux errors and observed noise are retained; photon noise is not re-simulated. Raw files are never overwritten and their hashes are checked. Uninjected controls may contain real variability or transits, so their peaks are not automatically false alarms.

Period recovery uses the blind strongest BLS peak, with direct and harmonic matches separate. This is period retrieval, not detection at a calibrated false-alarm rate. Paired template-depth bias compares detrended injected/control flux ratios at the known injected ephemeris. Grid eligibility and sampled event counts are recorded. Trapezoids approximate transit morphology; this experiment does not establish real-planet purity or limb-darkened transit completeness.
