# Research summary

These are descriptive results on a selected reference sample. Anomalies are not planet discoveries; PC labels are not confirmations.

- Requested 996 targets; analysed 1367 light curves from 996 unique targets.
- 0 requested targets produced no usable feature row.
- 72 of 300 hosts' representative catalogue periods lie outside the configured 0.5–12 day search interval; 6 have no usable representative period. Individual-sector baseline caps can restrict coverage further. This is not an all-planets completeness estimate.
- 5 of the top 5 hybrid-ranked inspection candidates are unlabelled backgrounds. These rankings do not validate planets.
- The analysed sample contains 300 planet targets.
- The analysed sample contains 196 false_positive targets.
- The analysed sample contains 500 background targets.
- depth_snr recovered 45/300 catalogue-positive targets (15.0%) in the top 100 targets.
- ensemble_score recovered 25/300 catalogue-positive targets (8.3%) in the top 100 targets.
- hybrid_score recovered 25/300 catalogue-positive targets (8.3%) in the top 100 targets.

## Ranking metrics
```
                method  requested_k   k   n  positive_total  recovered  precision_at_k  recall_at_k  mean_positive_rank  median_positive_rank  roc_auc  average_precision  binary_n                                         metric_note  recall_note
         bls_max_power            5   5 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power           10  10 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power           20  20 996             300          3           0.150     0.010000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power           50  50 996             300         15           0.300     0.050000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power          100 100 996             300         45           0.450     0.150000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power          200 200 996             300         92           0.460     0.306667          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr            5   5 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr           10  10 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr           20  20 996             300          3           0.150     0.010000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr           50  50 996             300         15           0.300     0.050000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr          100 100 996             300         45           0.450     0.150000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr          200 200 996             300         92           0.460     0.306667          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score            5   5 996             300          0           0.000     0.000000          488.966667                 472.0 0.542875           0.481508       367 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score           10  10 996             300          0           0.000     0.000000          488.966667                 472.0 0.542875           0.481508       367 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score           20  20 996             300          1           0.050     0.003333          488.966667                 472.0 0.542875           0.481508       367 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score           50  50 996             300          7           0.140     0.023333          488.966667                 472.0 0.542875           0.481508       367 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score          100 100 996             300         23           0.230     0.076667          488.966667                 472.0 0.542875           0.481508       367 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score          200 200 996             300         62           0.310     0.206667          488.966667                 472.0 0.542875           0.481508       367 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score            5   5 996             300          2           0.400     0.006667          516.790000                 521.0 0.421023           0.435616       367 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score           10  10 996             300          2           0.200     0.006667          516.790000                 521.0 0.421023           0.435616       367 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score           20  20 996             300          5           0.250     0.016667          516.790000                 521.0 0.421023           0.435616       367 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score           50  50 996             300          8           0.160     0.026667          516.790000                 521.0 0.421023           0.435616       367 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score          100 100 996             300         23           0.230     0.076667          516.790000                 521.0 0.421023           0.435616       367 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score          200 200 996             300         52           0.260     0.173333          516.790000                 521.0 0.421023           0.435616       367 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score            5   5 996             300          0           0.000     0.000000          502.273333                 485.0 0.483888           0.462409       367 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score           10  10 996             300          0           0.000     0.000000          502.273333                 485.0 0.483888           0.462409       367 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score           20  20 996             300          5           0.250     0.016667          502.273333                 485.0 0.483888           0.462409       367 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score           50  50 996             300         10           0.200     0.033333          502.273333                 485.0 0.483888           0.462409       367 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score          100 100 996             300         25           0.250     0.083333          502.273333                 485.0 0.483888           0.462409       367 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score          200 200 996             300         51           0.255     0.170000          502.273333                 485.0 0.483888           0.462409       367 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score            5   5 996             300          0           0.000     0.000000          439.436667                 392.5 0.562597           0.514575       367 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score           10  10 996             300          0           0.000     0.000000          439.436667                 392.5 0.562597           0.514575       367 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score           20  20 996             300          5           0.250     0.016667          439.436667                 392.5 0.562597           0.514575       367 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score           50  50 996             300         11           0.220     0.036667          439.436667                 392.5 0.562597           0.514575       367 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score          100 100 996             300         25           0.250     0.083333          439.436667                 392.5 0.562597           0.514575       367 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score          200 200 996             300         70           0.350     0.233333          439.436667                 392.5 0.562597           0.514575       367 Confirmed/known planets versus catalogue FP/FA only          NaN
```

## Correlations
```
               feature                  score   n  spearman_rho       p_value
         bls_max_power              depth_snr 996      1.000000  0.000000e+00
         bls_max_power isolation_forest_score 996      0.324239  8.185514e-26
         bls_max_power              lof_score 996      0.285364  4.065703e-20
         bls_max_power         ensemble_score 996      0.351742  2.222305e-30
         bls_max_power           hybrid_score 996      0.823546 5.484119e-247
             depth_snr          bls_max_power 996      1.000000  0.000000e+00
             depth_snr isolation_forest_score 996      0.324239  8.185514e-26
             depth_snr              lof_score 996      0.285364  4.065703e-20
             depth_snr         ensemble_score 996      0.351742  2.222305e-30
             depth_snr           hybrid_score 996      0.823546 5.484119e-247
isolation_forest_score          bls_max_power 996      0.324239  8.185514e-26
isolation_forest_score              depth_snr 996      0.324239  8.185514e-26
isolation_forest_score              lof_score 996      0.515629  9.502509e-69
isolation_forest_score         ensemble_score 996      0.853908 3.389472e-284
isolation_forest_score           hybrid_score 996      0.702642 4.406111e-149
             lof_score          bls_max_power 996      0.285364  4.065703e-20
             lof_score              depth_snr 996      0.285364  4.065703e-20
             lof_score isolation_forest_score 996      0.515629  9.502509e-69
             lof_score         ensemble_score 996      0.867896 2.641570e-304
             lof_score           hybrid_score 996      0.690518 5.433935e-142
        ensemble_score          bls_max_power 996      0.351742  2.222305e-30
        ensemble_score              depth_snr 996      0.351742  2.222305e-30
        ensemble_score isolation_forest_score 996      0.853908 3.389472e-284
        ensemble_score              lof_score 996      0.867896 2.641570e-304
        ensemble_score           hybrid_score 996      0.811823 1.723476e-234
          hybrid_score          bls_max_power 996      0.823546 5.484119e-247
          hybrid_score              depth_snr 996      0.823546 5.484119e-247
          hybrid_score isolation_forest_score 996      0.702642 4.406111e-149
          hybrid_score              lof_score 996      0.690518 5.433935e-142
          hybrid_score         ensemble_score 996      0.811823 1.723476e-234
```

## Group Statistics
```
                method          label   n    median      q25       q75  mann_whitney_p_vs_rest
         bls_max_power     background 500  6.626740 5.030909 20.254910            6.315962e-28
         bls_max_power false_positive 196 16.161729 9.068089 37.277457            1.251462e-08
         bls_max_power         planet 300 15.929983 7.994922 59.387273            2.460594e-12
             depth_snr     background 500  6.626740 5.030909 20.254910            6.315962e-28
             depth_snr false_positive 196 16.161729 9.068089 37.277457            1.251462e-08
             depth_snr         planet 300 15.929983 7.994922 59.387273            2.460594e-12
isolation_forest_score     background 500  0.369112 0.353860  0.399323            9.089356e-02
isolation_forest_score false_positive 196  0.373531 0.356601  0.410307            1.822387e-01
isolation_forest_score         planet 300  0.373574 0.355344  0.404809            4.923706e-01
             lof_score     background 500  1.216949 1.074758  1.509471            2.827871e-01
             lof_score false_positive 196  1.295937 1.119907  1.544998            4.091638e-03
             lof_score         planet 300  1.219110 1.073884  1.479076            1.877498e-01
        ensemble_score     background 500  0.493050 0.320958  0.721653            1.050459e-01
        ensemble_score false_positive 196  0.579920 0.402432  0.758961            1.861313e-02
        ensemble_score         planet 300  0.534199 0.344550  0.687637            7.851417e-01
          hybrid_score     background 500  0.439192 0.292063  0.628292            1.475382e-15
          hybrid_score false_positive 196  0.626463 0.450759  0.762299            2.970809e-07
          hybrid_score         planet 300  0.602323 0.402158  0.746525            2.098047e-05
```

## Ablation Results
```
                method  requested_k   k   n  positive_total  recovered  precision_at_k  recall_at_k  mean_positive_rank  median_positive_rank  roc_auc  average_precision  binary_n                                         metric_note  recall_note feature_family
         bls_max_power            5   5 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power           10  10 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power           20  20 996             300          3           0.150     0.010000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power           50  50 996             300         15           0.300     0.050000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power          100 100 996             300         45           0.450     0.150000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power          200 200 996             300         92           0.460     0.306667          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr            5   5 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr           10  10 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr           20  20 996             300          3           0.150     0.010000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr           50  50 996             300         15           0.300     0.050000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr          100 100 996             300         45           0.450     0.150000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr          200 200 996             300         92           0.460     0.306667          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score            5   5 996             300          0           0.000     0.000000          468.043333                 450.0 0.576173           0.498127       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score           10  10 996             300          0           0.000     0.000000          468.043333                 450.0 0.576173           0.498127       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score           20  20 996             300          2           0.100     0.006667          468.043333                 450.0 0.576173           0.498127       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score           50  50 996             300          6           0.120     0.020000          468.043333                 450.0 0.576173           0.498127       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score          100 100 996             300         20           0.200     0.066667          468.043333                 450.0 0.576173           0.498127       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score          200 200 996             300         67           0.335     0.223333          468.043333                 450.0 0.576173           0.498127       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score            5   5 996             300          2           0.400     0.006667          507.526667                 519.5 0.466613           0.488340       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score           10  10 996             300          3           0.300     0.010000          507.526667                 519.5 0.466613           0.488340       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score           20  20 996             300          3           0.150     0.010000          507.526667                 519.5 0.466613           0.488340       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score           50  50 996             300         12           0.240     0.040000          507.526667                 519.5 0.466613           0.488340       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score          100 100 996             300         28           0.280     0.093333          507.526667                 519.5 0.466613           0.488340       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score          200 200 996             300         51           0.255     0.170000          507.526667                 519.5 0.466613           0.488340       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score            5   5 996             300          0           0.000     0.000000          487.166667                 488.5 0.531388           0.488874       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score           10  10 996             300          1           0.100     0.003333          487.166667                 488.5 0.531388           0.488874       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score           20  20 996             300          3           0.150     0.010000          487.166667                 488.5 0.531388           0.488874       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score           50  50 996             300         12           0.240     0.040000          487.166667                 488.5 0.531388           0.488874       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score          100 100 996             300         27           0.270     0.090000          487.166667                 488.5 0.531388           0.488874       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score          200 200 996             300         57           0.285     0.190000          487.166667                 488.5 0.531388           0.488874       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score            5   5 996             300          0           0.000     0.000000          426.866667                 348.0 0.597431           0.542343       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score           10  10 996             300          0           0.000     0.000000          426.866667                 348.0 0.597431           0.542343       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score           20  20 996             300          5           0.250     0.016667          426.866667                 348.0 0.597431           0.542343       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score           50  50 996             300         13           0.260     0.043333          426.866667                 348.0 0.597431           0.542343       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score          100 100 996             300         35           0.350     0.116667          426.866667                 348.0 0.597431           0.542343       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score          200 200 996             300         79           0.395     0.263333          426.866667                 348.0 0.597431           0.542343       367 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power            5   5 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power           10  10 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power           20  20 996             300          3           0.150     0.010000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power           50  50 996             300         15           0.300     0.050000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power          100 100 996             300         45           0.450     0.150000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power          200 200 996             300         92           0.460     0.306667          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr            5   5 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr           10  10 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr           20  20 996             300          3           0.150     0.010000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr           50  50 996             300         15           0.300     0.050000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr          100 100 996             300         45           0.450     0.150000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr          200 200 996             300         92           0.460     0.306667          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score            5   5 996             300          0           0.000     0.000000          486.756667                 462.5 0.537654           0.485921       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score           10  10 996             300          0           0.000     0.000000          486.756667                 462.5 0.537654           0.485921       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score           20  20 996             300          2           0.100     0.006667          486.756667                 462.5 0.537654           0.485921       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score           50  50 996             300          8           0.160     0.026667          486.756667                 462.5 0.537654           0.485921       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score          100 100 996             300         24           0.240     0.080000          486.756667                 462.5 0.537654           0.485921       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score          200 200 996             300         63           0.315     0.210000          486.756667                 462.5 0.537654           0.485921       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score            5   5 996             300          0           0.000     0.000000          516.093333                 509.5 0.408521           0.413290       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score           10  10 996             300          0           0.000     0.000000          516.093333                 509.5 0.408521           0.413290       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score           20  20 996             300          1           0.050     0.003333          516.093333                 509.5 0.408521           0.413290       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score           50  50 996             300          6           0.120     0.020000          516.093333                 509.5 0.408521           0.413290       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score          100 100 996             300         18           0.180     0.060000          516.093333                 509.5 0.408521           0.413290       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score          200 200 996             300         48           0.240     0.160000          516.093333                 509.5 0.408521           0.413290       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score            5   5 996             300          0           0.000     0.000000          499.356667                 485.0 0.470164           0.437925       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score           10  10 996             300          0           0.000     0.000000          499.356667                 485.0 0.470164           0.437925       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score           20  20 996             300          2           0.100     0.006667          499.356667                 485.0 0.470164           0.437925       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score           50  50 996             300          7           0.140     0.023333          499.356667                 485.0 0.470164           0.437925       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score          100 100 996             300         19           0.190     0.063333          499.356667                 485.0 0.470164           0.437925       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score          200 200 996             300         45           0.225     0.150000          499.356667                 485.0 0.470164           0.437925       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score            5   5 996             300          0           0.000     0.000000          441.083333                 392.5 0.565073           0.520098       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score           10  10 996             300          0           0.000     0.000000          441.083333                 392.5 0.565073           0.520098       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score           20  20 996             300          4           0.200     0.013333          441.083333                 392.5 0.565073           0.520098       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score           50  50 996             300         14           0.280     0.046667          441.083333                 392.5 0.565073           0.520098       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score          100 100 996             300         31           0.310     0.103333          441.083333                 392.5 0.565073           0.520098       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score          200 200 996             300         69           0.345     0.230000          441.083333                 392.5 0.565073           0.520098       367 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power            5   5 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power           10  10 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power           20  20 996             300          3           0.150     0.010000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power           50  50 996             300         15           0.300     0.050000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power          100 100 996             300         45           0.450     0.150000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power          200 200 996             300         92           0.460     0.306667          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr            5   5 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr           10  10 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr           20  20 996             300          3           0.150     0.010000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr           50  50 996             300         15           0.300     0.050000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr          100 100 996             300         45           0.450     0.150000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr          200 200 996             300         92           0.460     0.306667          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score            5   5 996             300          0           0.000     0.000000          484.520000                 449.0 0.524138           0.471110       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score           10  10 996             300          1           0.100     0.003333          484.520000                 449.0 0.524138           0.471110       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score           20  20 996             300          2           0.100     0.006667          484.520000                 449.0 0.524138           0.471110       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score           50  50 996             300          8           0.160     0.026667          484.520000                 449.0 0.524138           0.471110       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score          100 100 996             300         24           0.240     0.080000          484.520000                 449.0 0.524138           0.471110       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score          200 200 996             300         69           0.345     0.230000          484.520000                 449.0 0.524138           0.471110       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score            5   5 996             300          1           0.200     0.003333          522.873333                 513.0 0.416637           0.413122       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score           10  10 996             300          1           0.100     0.003333          522.873333                 513.0 0.416637           0.413122       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score           20  20 996             300          2           0.100     0.006667          522.873333                 513.0 0.416637           0.413122       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score           50  50 996             300          6           0.120     0.020000          522.873333                 513.0 0.416637           0.413122       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score          100 100 996             300         21           0.210     0.070000          522.873333                 513.0 0.416637           0.413122       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score          200 200 996             300         48           0.240     0.160000          522.873333                 513.0 0.416637           0.413122       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score            5   5 996             300          0           0.000     0.000000          499.933333                 482.0 0.477086           0.441414       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score           10  10 996             300          1           0.100     0.003333          499.933333                 482.0 0.477086           0.441414       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score           20  20 996             300          2           0.100     0.006667          499.933333                 482.0 0.477086           0.441414       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score           50  50 996             300          8           0.160     0.026667          499.933333                 482.0 0.477086           0.441414       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score          100 100 996             300         24           0.240     0.080000          499.933333                 482.0 0.477086           0.441414       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score          200 200 996             300         53           0.265     0.176667          499.933333                 482.0 0.477086           0.441414       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score            5   5 996             300          0           0.000     0.000000          441.263333                 378.5 0.558897           0.513202       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score           10  10 996             300          1           0.100     0.003333          441.263333                 378.5 0.558897           0.513202       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score           20  20 996             300          2           0.100     0.006667          441.263333                 378.5 0.558897           0.513202       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score           50  50 996             300         14           0.280     0.046667          441.263333                 378.5 0.558897           0.513202       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score          100 100 996             300         39           0.390     0.130000          441.263333                 378.5 0.558897           0.513202       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score          200 200 996             300         81           0.405     0.270000          441.263333                 378.5 0.558897           0.513202       367 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power            5   5 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power           10  10 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power           20  20 996             300          3           0.150     0.010000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power           50  50 996             300         15           0.300     0.050000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power          100 100 996             300         45           0.450     0.150000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power          200 200 996             300         92           0.460     0.306667          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr            5   5 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr           10  10 996             300          0           0.000     0.000000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr           20  20 996             300          3           0.150     0.010000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr           50  50 996             300         15           0.300     0.050000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr          100 100 996             300         45           0.450     0.150000          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr          200 200 996             300         92           0.460     0.306667          401.236667                 387.5 0.641753           0.596865       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score            5   5 996             300          0           0.000     0.000000          488.966667                 472.0 0.542875           0.481508       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score           10  10 996             300          0           0.000     0.000000          488.966667                 472.0 0.542875           0.481508       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score           20  20 996             300          1           0.050     0.003333          488.966667                 472.0 0.542875           0.481508       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score           50  50 996             300          7           0.140     0.023333          488.966667                 472.0 0.542875           0.481508       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score          100 100 996             300         23           0.230     0.076667          488.966667                 472.0 0.542875           0.481508       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score          200 200 996             300         62           0.310     0.206667          488.966667                 472.0 0.542875           0.481508       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score            5   5 996             300          2           0.400     0.006667          516.790000                 521.0 0.421023           0.435616       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score           10  10 996             300          2           0.200     0.006667          516.790000                 521.0 0.421023           0.435616       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score           20  20 996             300          5           0.250     0.016667          516.790000                 521.0 0.421023           0.435616       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score           50  50 996             300          8           0.160     0.026667          516.790000                 521.0 0.421023           0.435616       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score          100 100 996             300         23           0.230     0.076667          516.790000                 521.0 0.421023           0.435616       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score          200 200 996             300         52           0.260     0.173333          516.790000                 521.0 0.421023           0.435616       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score            5   5 996             300          0           0.000     0.000000          502.273333                 485.0 0.483888           0.462409       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score           10  10 996             300          0           0.000     0.000000          502.273333                 485.0 0.483888           0.462409       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score           20  20 996             300          5           0.250     0.016667          502.273333                 485.0 0.483888           0.462409       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score           50  50 996             300         10           0.200     0.033333          502.273333                 485.0 0.483888           0.462409       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score          100 100 996             300         25           0.250     0.083333          502.273333                 485.0 0.483888           0.462409       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score          200 200 996             300         51           0.255     0.170000          502.273333                 485.0 0.483888           0.462409       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score            5   5 996             300          0           0.000     0.000000          439.436667                 392.5 0.562597           0.514575       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score           10  10 996             300          0           0.000     0.000000          439.436667                 392.5 0.562597           0.514575       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score           20  20 996             300          5           0.250     0.016667          439.436667                 392.5 0.562597           0.514575       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score           50  50 996             300         11           0.220     0.036667          439.436667                 392.5 0.562597           0.514575       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score          100 100 996             300         25           0.250     0.083333          439.436667                 392.5 0.562597           0.514575       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score          200 200 996             300         70           0.350     0.233333          439.436667                 392.5 0.562597           0.514575       367 Confirmed/known planets versus catalogue FP/FA only          NaN            all
```

## Sector Coverage
```
         label  sectors  targets
    background        1      354
    background        2      146
false_positive        1      103
false_positive        2       93
        planet        1      168
        planet        2      132
```

## Top Candidates
```
   tic_id  sector      label disposition  best_period  best_depth   depth_snr  ensemble_score  hybrid_score
 75969405      11 background  UNLABELLED     4.610691    0.300759 6721.170889        0.995977      0.999451
469979014       1 background  UNLABELLED     0.581241    0.127469 1345.099938        0.995977      0.997257
 22242383      10 background  UNLABELLED     0.678081    0.104720 2433.851859        0.988661      0.996891
277649549       1 background  UNLABELLED     4.832143    0.049776 3153.270770        0.987564      0.995245
387178621      10 background  UNLABELLED     8.189222    0.309717 1887.051296        0.987930      0.994879
```

## Interpretation limits
Sector coverage differs between reference groups. Taking each target's maximum score across sectors gives more observed sectors more opportunities for a high score; group comparisons are not controlled for this exposure difference. Catalogue periods outside the search interval cannot be recovered directly within that interval, although harmonics may occur. Independent evaluation with exposure and search coverage accounted for is needed before claiming generalisation or reduced inspection workload.
The primary experiment uses unsupervised anomaly detection; catalogue labels are used only for evaluation. The LOF novelty helper does not constitute an evaluated semi-supervised experiment. Physics-informed means astrophysically motivated feature engineering, not physical equations enforced during training. Stellar-catalogue-dependent radius and duration-consistency proxies are extracted where possible but excluded from default ML inputs because measurement availability differs between groups.
Interpretability analyses describe properties associated with high anomaly scores. They do not establish causation, provide formal per-object model attribution, or calibrate anomaly scores as statistical significance. The primary models fit and rank the same unlabelled sample. Reduced manual inspection workload and generalisation remain research questions requiring independent evaluation.
No held-out generalisation or causal improvement is established. Background objects are unlabelled. Precision@K measures catalogue-positive yield, not true planet purity. ROC-AUC and average precision exclude PC-only and background targets. BLS power and depth SNR are identical rankings under the default SNR objective. Catalogue-conditioned stellar-feature missingness can bias physics ablations. Non-parametric p-values are exploratory and uncorrected for multiple comparisons.