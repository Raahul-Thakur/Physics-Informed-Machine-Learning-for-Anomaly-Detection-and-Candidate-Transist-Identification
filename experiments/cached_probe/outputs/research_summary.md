# Research summary

These are descriptive results on a selected reference sample. Anomalies are not planet discoveries; PC labels are not confirmations.

- Requested 9 targets; analysed 9 light curves from 9 unique targets.
- 0 requested targets produced no usable feature row.
- The analysed sample contains 3 planet targets.
- The analysed sample contains 3 false_positive targets.
- The analysed sample contains 3 background targets.
- depth_snr recovered 0/3 catalogue-positive targets (0.0%) in the top 1 targets.
- ensemble_score recovered 0/3 catalogue-positive targets (0.0%) in the top 1 targets.
- hybrid_score recovered 0/3 catalogue-positive targets (0.0%) in the top 1 targets.

## Ranking metrics
```
                method  requested_k  k  n  positive_total  recovered  precision_at_k  recall_at_k  mean_positive_rank  median_positive_rank  roc_auc  average_precision  binary_n                                         metric_note  recall_note
         bls_max_power            1  1  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power            2  2  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power            5  5  9               3          1        0.200000     0.333333            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power           10  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power           20  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr            1  1  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr            2  2  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr            5  5  9               3          1        0.200000     0.333333            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr           10  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr           20  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score            1  1  9               3          1        1.000000     0.333333            5.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score            2  2  9               3          1        0.500000     0.333333            5.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score            5  5  9               3          1        0.200000     0.333333            5.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score           10  9  9               3          3        0.333333     1.000000            5.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score           20  9  9               3          3        0.333333     1.000000            5.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score            1  1  9               3          0        0.000000     0.000000            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score            2  2  9               3          0        0.000000     0.000000            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score            5  5  9               3          2        0.400000     0.666667            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score           10  9  9               3          3        0.333333     1.000000            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score           20  9  9               3          3        0.333333     1.000000            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score            1  1  9               3          0        0.000000     0.000000            5.666667                   6.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score            2  2  9               3          0        0.000000     0.000000            5.666667                   6.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score            5  5  9               3          1        0.200000     0.333333            5.666667                   6.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score           10  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score           20  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score            1  1  9               3          0        0.000000     0.000000            6.000000                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score            2  2  9               3          1        0.500000     0.333333            6.000000                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score            5  5  9               3          1        0.200000     0.333333            6.000000                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score           10  9  9               3          3        0.333333     1.000000            6.000000                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score           20  9  9               3          3        0.333333     1.000000            6.000000                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN
```

## Correlations
```
               feature                  score  n  spearman_rho  p_value
         bls_max_power              depth_snr  9      1.000000 0.000000
         bls_max_power isolation_forest_score  9      0.600000 0.087623
         bls_max_power              lof_score  9     -0.803354 0.009106
         bls_max_power         ensemble_score  9     -0.225943 0.558846
         bls_max_power           hybrid_score  9      0.577411 0.103507
             depth_snr          bls_max_power  9      1.000000 0.000000
             depth_snr isolation_forest_score  9      0.600000 0.087623
             depth_snr              lof_score  9     -0.803354 0.009106
             depth_snr         ensemble_score  9     -0.225943 0.558846
             depth_snr           hybrid_score  9      0.577411 0.103507
isolation_forest_score          bls_max_power  9      0.600000 0.087623
isolation_forest_score              depth_snr  9      0.600000 0.087623
isolation_forest_score              lof_score  9     -0.627621 0.070365
isolation_forest_score         ensemble_score  9      0.485360 0.185354
isolation_forest_score           hybrid_score  9      0.878669 0.001816
             lof_score          bls_max_power  9     -0.803354 0.009106
             lof_score              depth_snr  9     -0.803354 0.009106
             lof_score isolation_forest_score  9     -0.627621 0.070365
             lof_score         ensemble_score  9      0.369748 0.327379
             lof_score           hybrid_score  9     -0.323529 0.395727
        ensemble_score          bls_max_power  9     -0.225943 0.558846
        ensemble_score              depth_snr  9     -0.225943 0.558846
        ensemble_score isolation_forest_score  9      0.485360 0.185354
        ensemble_score              lof_score  9      0.369748 0.327379
        ensemble_score           hybrid_score  9      0.655462 0.055296
          hybrid_score          bls_max_power  9      0.577411 0.103507
          hybrid_score              depth_snr  9      0.577411 0.103507
          hybrid_score isolation_forest_score  9      0.878669 0.001816
          hybrid_score              lof_score  9     -0.323529 0.395727
          hybrid_score         ensemble_score  9      0.655462 0.055296
```

## Group Statistics
```
                method          label  n    median       q25       q75  mann_whitney_p_vs_rest
         bls_max_power     background  3 14.624300 10.215611 17.043073                1.000000
         bls_max_power false_positive  3 10.940263  8.815815 16.121958                0.714286
         bls_max_power         planet  3  7.596905  6.996021 13.011203                0.714286
             depth_snr     background  3 14.624300 10.215611 17.043073                1.000000
             depth_snr false_positive  3 10.940263  8.815815 16.121958                0.714286
             depth_snr         planet  3  7.596905  6.996021 13.011203                0.714286
isolation_forest_score     background  3  0.458152  0.448902  0.467633                0.380952
isolation_forest_score false_positive  3  0.450749  0.421760  0.453018                0.547619
isolation_forest_score         planet  3  0.433243  0.425556  0.567582                0.904762
             lof_score     background  3  0.999767  0.999746  1.000250                1.000000
             lof_score false_positive  3  0.999775  0.999685  1.000280                0.795418
             lof_score         planet  3  0.999768  0.999681  1.000013                0.795418
        ensemble_score     background  3  0.666667  0.611111  0.666667                0.243305
        ensemble_score false_positive  3  0.416667  0.402778  0.597222                0.516853
        ensemble_score         planet  3  0.500000  0.472222  0.541667                0.697334
          hybrid_score     background  3  0.611111  0.541667  0.736111                0.436661
          hybrid_score false_positive  3  0.611111  0.472222  0.638889                1.000000
          hybrid_score         planet  3  0.444444  0.361111  0.583333                0.516853
```

## Ablation Results
```
                method  requested_k  k  n  positive_total  recovered  precision_at_k  recall_at_k  mean_positive_rank  median_positive_rank  roc_auc  average_precision  binary_n                                         metric_note  recall_note feature_family
         bls_max_power            1  1  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power            2  2  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power            5  5  9               3          1        0.200000     0.333333            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power           10  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power           20  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr            1  1  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr            2  2  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr            5  5  9               3          1        0.200000     0.333333            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr           10  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr           20  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score            1  1  9               3          1        1.000000     0.333333            4.000000                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score            2  2  9               3          1        0.500000     0.333333            4.000000                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score            5  5  9               3          2        0.400000     0.666667            4.000000                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score           10  9  9               3          3        0.333333     1.000000            4.000000                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score           20  9  9               3          3        0.333333     1.000000            4.000000                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score            1  1  9               3          0        0.000000     0.000000            5.333333                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score            2  2  9               3          0        0.000000     0.000000            5.333333                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score            5  5  9               3          2        0.400000     0.666667            5.333333                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score           10  9  9               3          3        0.333333     1.000000            5.333333                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score           20  9  9               3          3        0.333333     1.000000            5.333333                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score            1  1  9               3          0        0.000000     0.000000            4.000000                   4.0 0.833333           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score            2  2  9               3          0        0.000000     0.000000            4.000000                   4.0 0.833333           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score            5  5  9               3          3        0.600000     1.000000            4.000000                   4.0 0.833333           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score           10  9  9               3          3        0.333333     1.000000            4.000000                   4.0 0.833333           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score           20  9  9               3          3        0.333333     1.000000            4.000000                   4.0 0.833333           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score            1  1  9               3          0        0.000000     0.000000            4.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score            2  2  9               3          1        0.500000     0.333333            4.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score            5  5  9               3          2        0.400000     0.666667            4.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score           10  9  9               3          3        0.333333     1.000000            4.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score           20  9  9               3          3        0.333333     1.000000            4.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power            1  1  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power            2  2  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power            5  5  9               3          1        0.200000     0.333333            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power           10  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power           20  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr            1  1  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr            2  2  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr            5  5  9               3          1        0.200000     0.333333            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr           10  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr           20  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score            1  1  9               3          1        1.000000     0.333333            6.000000                   8.0 0.000000           0.250000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score            2  2  9               3          1        0.500000     0.333333            6.000000                   8.0 0.000000           0.250000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score            5  5  9               3          1        0.200000     0.333333            6.000000                   8.0 0.000000           0.250000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score           10  9  9               3          3        0.333333     1.000000            6.000000                   8.0 0.000000           0.250000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score           20  9  9               3          3        0.333333     1.000000            6.000000                   8.0 0.000000           0.250000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score            1  1  9               3          0        0.000000     0.000000            4.666667                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score            2  2  9               3          1        0.500000     0.333333            4.666667                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score            5  5  9               3          2        0.400000     0.666667            4.666667                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score           10  9  9               3          3        0.333333     1.000000            4.666667                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score           20  9  9               3          3        0.333333     1.000000            4.666667                   4.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score            1  1  9               3          0        0.000000     0.000000            5.666667                   5.0 0.500000           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score            2  2  9               3          0        0.000000     0.000000            5.666667                   5.0 0.500000           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score            5  5  9               3          2        0.400000     0.666667            5.666667                   5.0 0.500000           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score           10  9  9               3          3        0.333333     1.000000            5.666667                   5.0 0.500000           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score           20  9  9               3          3        0.333333     1.000000            5.666667                   5.0 0.500000           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score            1  1  9               3          1        1.000000     0.333333            5.333333                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score            2  2  9               3          1        0.500000     0.333333            5.333333                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score            5  5  9               3          1        0.200000     0.333333            5.333333                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score           10  9  9               3          3        0.333333     1.000000            5.333333                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score           20  9  9               3          3        0.333333     1.000000            5.333333                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power            1  1  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power            2  2  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power            5  5  9               3          1        0.200000     0.333333            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power           10  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power           20  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr            1  1  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr            2  2  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr            5  5  9               3          1        0.200000     0.333333            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr           10  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr           20  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score            1  1  9               3          1        1.000000     0.333333            4.333333                   3.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score            2  2  9               3          1        0.500000     0.333333            4.333333                   3.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score            5  5  9               3          2        0.400000     0.666667            4.333333                   3.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score           10  9  9               3          3        0.333333     1.000000            4.333333                   3.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score           20  9  9               3          3        0.333333     1.000000            4.333333                   3.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score            1  1  9               3          0        0.000000     0.000000            7.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score            2  2  9               3          0        0.000000     0.000000            7.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score            5  5  9               3          0        0.000000     0.000000            7.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score           10  9  9               3          3        0.333333     1.000000            7.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score           20  9  9               3          3        0.333333     1.000000            7.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score            1  1  9               3          0        0.000000     0.000000            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score            2  2  9               3          1        0.500000     0.333333            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score            5  5  9               3          2        0.400000     0.666667            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score           10  9  9               3          3        0.333333     1.000000            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score           20  9  9               3          3        0.333333     1.000000            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score            1  1  9               3          0        0.000000     0.000000            6.333333                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score            2  2  9               3          0        0.000000     0.000000            6.333333                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score            5  5  9               3          1        0.200000     0.333333            6.333333                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score           10  9  9               3          3        0.333333     1.000000            6.333333                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score           20  9  9               3          3        0.333333     1.000000            6.333333                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power            1  1  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power            2  2  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power            5  5  9               3          1        0.200000     0.333333            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power           10  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power           20  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr            1  1  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr            2  2  9               3          0        0.000000     0.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr            5  5  9               3          1        0.200000     0.333333            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr           10  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr           20  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score            1  1  9               3          1        1.000000     0.333333            5.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score            2  2  9               3          1        0.500000     0.333333            5.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score            5  5  9               3          1        0.200000     0.333333            5.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score           10  9  9               3          3        0.333333     1.000000            5.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score           20  9  9               3          3        0.333333     1.000000            5.333333                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score            1  1  9               3          0        0.000000     0.000000            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score            2  2  9               3          0        0.000000     0.000000            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score            5  5  9               3          2        0.400000     0.666667            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score           10  9  9               3          3        0.333333     1.000000            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score           20  9  9               3          3        0.333333     1.000000            5.333333                   5.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score            1  1  9               3          0        0.000000     0.000000            5.666667                   6.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score            2  2  9               3          0        0.000000     0.000000            5.666667                   6.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score            5  5  9               3          1        0.200000     0.333333            5.666667                   6.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score           10  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score           20  9  9               3          3        0.333333     1.000000            5.666667                   6.0 0.666667           0.500000         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score            1  1  9               3          0        0.000000     0.000000            6.000000                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score            2  2  9               3          1        0.500000     0.333333            6.000000                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score            5  5  9               3          1        0.200000     0.333333            6.000000                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score           10  9  9               3          3        0.333333     1.000000            6.000000                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score           20  9  9               3          3        0.333333     1.000000            6.000000                   7.0 0.333333           0.333333         4 Confirmed/known planets versus catalogue FP/FA only          NaN            all
```

## Top Candidates
```
   tic_id  sector disposition  best_period  best_depth  depth_snr  ensemble_score  hybrid_score
144596911       4  UNLABELLED     2.044517    0.000227  19.461847        0.666667      0.861111
```

## Interpretation limits
No held-out generalisation or causal improvement is established. Background objects are unlabelled. Precision@K measures catalogue-positive yield, not true planet purity. ROC-AUC and average precision exclude PC-only and background targets. BLS power and depth SNR are identical rankings under the default SNR objective. Catalogue-conditioned stellar-feature missingness can bias physics ablations. Non-parametric p-values are exploratory and uncorrected for multiple comparisons.