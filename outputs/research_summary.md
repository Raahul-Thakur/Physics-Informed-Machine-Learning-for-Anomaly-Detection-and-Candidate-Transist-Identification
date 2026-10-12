# Research summary

These are descriptive results on a selected reference sample. Anomalies are not planet discoveries; PC labels are not confirmations.

- Requested 110 targets; analysed 110 light curves from 110 unique targets.
- 0 requested targets produced no usable feature row.
- 11 of 30 hosts' representative catalogue periods lie outside the configured 0.5–12 day search interval; 1 have no usable representative period. Individual-sector baseline caps can restrict coverage further. This is not an all-planets completeness estimate.
- 0 of the top 5 hybrid-ranked inspection candidates are unlabelled backgrounds. These rankings do not validate planets.
- The analysed sample contains 30 planet targets.
- The analysed sample contains 30 false_positive targets.
- The analysed sample contains 50 background targets.
- depth_snr recovered 2/30 catalogue-positive targets (6.7%) in the top 11 targets.
- ensemble_score recovered 1/30 catalogue-positive targets (3.3%) in the top 11 targets.
- hybrid_score recovered 2/30 catalogue-positive targets (6.7%) in the top 11 targets.

## Ranking metrics
```
                method  requested_k  k   n  positive_total  recovered  precision_at_k  recall_at_k  mean_positive_rank  median_positive_rank  roc_auc  average_precision  binary_n                                         metric_note  recall_note
         bls_max_power            5  5 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power            6  6 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power           10 10 110              30          2        0.200000     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power           11 11 110              30          2        0.181818     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power           20 20 110              30          4        0.200000     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN
         bls_max_power           22 22 110              30          4        0.181818     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr            5  5 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr            6  6 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr           10 10 110              30          2        0.200000     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr           11 11 110              30          2        0.181818     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr           20 20 110              30          4        0.200000     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN
             depth_snr           22 22 110              30          4        0.181818     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score            5  5 110              30          2        0.400000     0.066667           62.766667                  66.5 0.413333           0.224451        40 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score            6  6 110              30          3        0.500000     0.100000           62.766667                  66.5 0.413333           0.224451        40 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score           10 10 110              30          3        0.300000     0.100000           62.766667                  66.5 0.413333           0.224451        40 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score           11 11 110              30          3        0.272727     0.100000           62.766667                  66.5 0.413333           0.224451        40 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score           20 20 110              30          5        0.250000     0.166667           62.766667                  66.5 0.413333           0.224451        40 Confirmed/known planets versus catalogue FP/FA only          NaN
isolation_forest_score           22 22 110              30          5        0.227273     0.166667           62.766667                  66.5 0.413333           0.224451        40 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score            5  5 110              30          1        0.200000     0.033333           61.333333                  62.5 0.450000           0.235739        40 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score            6  6 110              30          1        0.166667     0.033333           61.333333                  62.5 0.450000           0.235739        40 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score           10 10 110              30          1        0.100000     0.033333           61.333333                  62.5 0.450000           0.235739        40 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score           11 11 110              30          1        0.090909     0.033333           61.333333                  62.5 0.450000           0.235739        40 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score           20 20 110              30          3        0.150000     0.100000           61.333333                  62.5 0.450000           0.235739        40 Confirmed/known planets versus catalogue FP/FA only          NaN
             lof_score           22 22 110              30          4        0.181818     0.133333           61.333333                  62.5 0.450000           0.235739        40 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score            5  5 110              30          1        0.200000     0.033333           62.333333                  64.5 0.431667           0.227628        40 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score            6  6 110              30          1        0.166667     0.033333           62.333333                  64.5 0.431667           0.227628        40 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score           10 10 110              30          1        0.100000     0.033333           62.333333                  64.5 0.431667           0.227628        40 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score           11 11 110              30          1        0.090909     0.033333           62.333333                  64.5 0.431667           0.227628        40 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score           20 20 110              30          4        0.200000     0.133333           62.333333                  64.5 0.431667           0.227628        40 Confirmed/known planets versus catalogue FP/FA only          NaN
        ensemble_score           22 22 110              30          5        0.227273     0.166667           62.333333                  64.5 0.431667           0.227628        40 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score            5  5 110              30          0        0.000000     0.000000           54.466667                  55.5 0.481667           0.255137        40 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score            6  6 110              30          0        0.000000     0.000000           54.466667                  55.5 0.481667           0.255137        40 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score           10 10 110              30          2        0.200000     0.066667           54.466667                  55.5 0.481667           0.255137        40 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score           11 11 110              30          2        0.181818     0.066667           54.466667                  55.5 0.481667           0.255137        40 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score           20 20 110              30          5        0.250000     0.166667           54.466667                  55.5 0.481667           0.255137        40 Confirmed/known planets versus catalogue FP/FA only          NaN
          hybrid_score           22 22 110              30          5        0.227273     0.166667           54.466667                  55.5 0.481667           0.255137        40 Confirmed/known planets versus catalogue FP/FA only          NaN
```

## Correlations
```
               feature                  score   n  spearman_rho      p_value
         bls_max_power              depth_snr 110      1.000000 0.000000e+00
         bls_max_power isolation_forest_score 110      0.425016 3.690665e-06
         bls_max_power              lof_score 110      0.442562 1.291730e-06
         bls_max_power         ensemble_score 110      0.437942 1.712869e-06
         bls_max_power           hybrid_score 110      0.829446 4.461893e-29
             depth_snr          bls_max_power 110      1.000000 0.000000e+00
             depth_snr isolation_forest_score 110      0.425016 3.690665e-06
             depth_snr              lof_score 110      0.442562 1.291730e-06
             depth_snr         ensemble_score 110      0.437942 1.712869e-06
             depth_snr           hybrid_score 110      0.829446 4.461893e-29
isolation_forest_score          bls_max_power 110      0.425016 3.690665e-06
isolation_forest_score              depth_snr 110      0.425016 3.690665e-06
isolation_forest_score              lof_score 110      0.936839 4.357251e-51
isolation_forest_score         ensemble_score 110      0.984818 5.754039e-84
isolation_forest_score           hybrid_score 110      0.836542 5.496147e-30
             lof_score          bls_max_power 110      0.442562 1.291730e-06
             lof_score              depth_snr 110      0.442562 1.291730e-06
             lof_score isolation_forest_score 110      0.936839 4.357251e-51
             lof_score         ensemble_score 110      0.981382 3.196595e-79
             lof_score           hybrid_score 110      0.847709 1.648270e-31
        ensemble_score          bls_max_power 110      0.437942 1.712869e-06
        ensemble_score              depth_snr 110      0.437942 1.712869e-06
        ensemble_score isolation_forest_score 110      0.984818 5.754039e-84
        ensemble_score              lof_score 110      0.981382 3.196595e-79
        ensemble_score           hybrid_score 110      0.855017 1.421549e-32
          hybrid_score          bls_max_power 110      0.829446 4.461893e-29
          hybrid_score              depth_snr 110      0.829446 4.461893e-29
          hybrid_score isolation_forest_score 110      0.836542 5.496147e-30
          hybrid_score              lof_score 110      0.847709 1.648270e-31
          hybrid_score         ensemble_score 110      0.855017 1.421549e-32
```

## Group Statistics
```
                method          label  n    median      q25       q75  mann_whitney_p_vs_rest
         bls_max_power     background 50  5.730070 4.917540  9.603448                0.000035
         bls_max_power false_positive 30 10.608762 7.507530 29.273171                0.002137
         bls_max_power         planet 30  8.263769 6.695578 18.028275                0.120250
             depth_snr     background 50  5.730070 4.917540  9.603448                0.000035
             depth_snr false_positive 30 10.608762 7.507530 29.273171                0.002137
             depth_snr         planet 30  8.263769 6.695578 18.028275                0.120250
isolation_forest_score     background 50  0.392437 0.366891  0.425976                0.817225
isolation_forest_score false_positive 30  0.404782 0.368217  0.467460                0.230912
isolation_forest_score         planet 30  0.377548 0.367137  0.406732                0.144355
             lof_score     background 50  1.318507 1.019688  3.193643                0.831244
             lof_score false_positive 30  1.358602 1.025837  4.435698                0.352604
             lof_score         planet 30  1.183550 1.013377  1.553063                0.241532
        ensemble_score     background 50  0.522727 0.262500  0.730682                0.800933
        ensemble_score false_positive 30  0.584091 0.284091  0.832955                0.281364
        ensemble_score         planet 30  0.415909 0.247727  0.587500                0.173035
          hybrid_score     background 50  0.409091 0.249432  0.647727                0.020165
          hybrid_score false_positive 30  0.638636 0.396023  0.804545                0.016418
          hybrid_score         planet 30  0.452273 0.351705  0.692614                0.845672
```

## Ablation Results
```
                method  requested_k  k   n  positive_total  recovered  precision_at_k  recall_at_k  mean_positive_rank  median_positive_rank  roc_auc  average_precision  binary_n                                         metric_note  recall_note feature_family
         bls_max_power            5  5 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power            6  6 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power           10 10 110              30          2        0.200000     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power           11 11 110              30          2        0.181818     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power           20 20 110              30          4        0.200000     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power           22 22 110              30          4        0.181818     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr            5  5 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr            6  6 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr           10 10 110              30          2        0.200000     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr           11 11 110              30          2        0.181818     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr           20 20 110              30          4        0.200000     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             depth_snr           22 22 110              30          4        0.181818     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score            5  5 110              30          1        0.200000     0.033333           61.000000                  68.0 0.410000           0.226037        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score            6  6 110              30          2        0.333333     0.066667           61.000000                  68.0 0.410000           0.226037        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score           10 10 110              30          3        0.300000     0.100000           61.000000                  68.0 0.410000           0.226037        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score           11 11 110              30          3        0.272727     0.100000           61.000000                  68.0 0.410000           0.226037        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score           20 20 110              30          4        0.200000     0.133333           61.000000                  68.0 0.410000           0.226037        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
isolation_forest_score           22 22 110              30          5        0.227273     0.166667           61.000000                  68.0 0.410000           0.226037        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score            5  5 110              30          0        0.000000     0.000000           62.833333                  66.5 0.473333           0.245123        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score            6  6 110              30          0        0.000000     0.000000           62.833333                  66.5 0.473333           0.245123        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score           10 10 110              30          2        0.200000     0.066667           62.833333                  66.5 0.473333           0.245123        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score           11 11 110              30          2        0.181818     0.066667           62.833333                  66.5 0.473333           0.245123        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score           20 20 110              30          4        0.200000     0.133333           62.833333                  66.5 0.473333           0.245123        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
             lof_score           22 22 110              30          5        0.227273     0.166667           62.833333                  66.5 0.473333           0.245123        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score            5  5 110              30          1        0.200000     0.033333           62.333333                  63.0 0.420000           0.225149        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score            6  6 110              30          2        0.333333     0.066667           62.333333                  63.0 0.420000           0.225149        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score           10 10 110              30          3        0.300000     0.100000           62.333333                  63.0 0.420000           0.225149        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score           11 11 110              30          3        0.272727     0.100000           62.333333                  63.0 0.420000           0.225149        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score           20 20 110              30          4        0.200000     0.133333           62.333333                  63.0 0.420000           0.225149        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
        ensemble_score           22 22 110              30          5        0.227273     0.166667           62.333333                  63.0 0.420000           0.225149        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score            5  5 110              30          0        0.000000     0.000000           55.566667                  60.5 0.496667           0.261041        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score            6  6 110              30          0        0.000000     0.000000           55.566667                  60.5 0.496667           0.261041        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score           10 10 110              30          2        0.200000     0.066667           55.566667                  60.5 0.496667           0.261041        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score           11 11 110              30          3        0.272727     0.100000           55.566667                  60.5 0.496667           0.261041        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score           20 20 110              30          6        0.300000     0.200000           55.566667                  60.5 0.496667           0.261041        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
          hybrid_score           22 22 110              30          6        0.272727     0.200000           55.566667                  60.5 0.496667           0.261041        40 Confirmed/known planets versus catalogue FP/FA only          NaN        generic
         bls_max_power            5  5 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power            6  6 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power           10 10 110              30          2        0.200000     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power           11 11 110              30          2        0.181818     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power           20 20 110              30          4        0.200000     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power           22 22 110              30          4        0.181818     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr            5  5 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr            6  6 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr           10 10 110              30          2        0.200000     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr           11 11 110              30          2        0.181818     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr           20 20 110              30          4        0.200000     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             depth_snr           22 22 110              30          4        0.181818     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score            5  5 110              30          1        0.200000     0.033333           59.700000                  56.5 0.426667           0.238222        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score            6  6 110              30          2        0.333333     0.066667           59.700000                  56.5 0.426667           0.238222        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score           10 10 110              30          3        0.300000     0.100000           59.700000                  56.5 0.426667           0.238222        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score           11 11 110              30          3        0.272727     0.100000           59.700000                  56.5 0.426667           0.238222        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score           20 20 110              30          4        0.200000     0.133333           59.700000                  56.5 0.426667           0.238222        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
isolation_forest_score           22 22 110              30          5        0.227273     0.166667           59.700000                  56.5 0.426667           0.238222        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score            5  5 110              30          1        0.200000     0.033333           58.200000                  53.5 0.510000           0.274896        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score            6  6 110              30          1        0.166667     0.033333           58.200000                  53.5 0.510000           0.274896        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score           10 10 110              30          1        0.100000     0.033333           58.200000                  53.5 0.510000           0.274896        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score           11 11 110              30          1        0.090909     0.033333           58.200000                  53.5 0.510000           0.274896        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score           20 20 110              30          4        0.200000     0.133333           58.200000                  53.5 0.510000           0.274896        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
             lof_score           22 22 110              30          5        0.227273     0.166667           58.200000                  53.5 0.510000           0.274896        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score            5  5 110              30          1        0.200000     0.033333           58.933333                  59.0 0.468333           0.251661        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score            6  6 110              30          1        0.166667     0.033333           58.933333                  59.0 0.468333           0.251661        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score           10 10 110              30          2        0.200000     0.066667           58.933333                  59.0 0.468333           0.251661        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score           11 11 110              30          2        0.181818     0.066667           58.933333                  59.0 0.468333           0.251661        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score           20 20 110              30          5        0.250000     0.166667           58.933333                  59.0 0.468333           0.251661        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
        ensemble_score           22 22 110              30          6        0.272727     0.200000           58.933333                  59.0 0.468333           0.251661        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score            5  5 110              30          0        0.000000     0.000000           52.433333                  54.5 0.518333           0.279517        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score            6  6 110              30          0        0.000000     0.000000           52.433333                  54.5 0.518333           0.279517        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score           10 10 110              30          2        0.200000     0.066667           52.433333                  54.5 0.518333           0.279517        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score           11 11 110              30          2        0.181818     0.066667           52.433333                  54.5 0.518333           0.279517        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score           20 20 110              30          6        0.300000     0.200000           52.433333                  54.5 0.518333           0.279517        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
          hybrid_score           22 22 110              30          7        0.318182     0.233333           52.433333                  54.5 0.518333           0.279517        40 Confirmed/known planets versus catalogue FP/FA only          NaN            bls
         bls_max_power            5  5 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power            6  6 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power           10 10 110              30          2        0.200000     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power           11 11 110              30          2        0.181818     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power           20 20 110              30          4        0.200000     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power           22 22 110              30          4        0.181818     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr            5  5 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr            6  6 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr           10 10 110              30          2        0.200000     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr           11 11 110              30          2        0.181818     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr           20 20 110              30          4        0.200000     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             depth_snr           22 22 110              30          4        0.181818     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score            5  5 110              30          3        0.600000     0.100000           61.600000                  58.5 0.390000           0.233560        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score            6  6 110              30          3        0.500000     0.100000           61.600000                  58.5 0.390000           0.233560        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score           10 10 110              30          3        0.300000     0.100000           61.600000                  58.5 0.390000           0.233560        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score           11 11 110              30          3        0.272727     0.100000           61.600000                  58.5 0.390000           0.233560        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score           20 20 110              30          5        0.250000     0.166667           61.600000                  58.5 0.390000           0.233560        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
isolation_forest_score           22 22 110              30          5        0.227273     0.166667           61.600000                  58.5 0.390000           0.233560        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score            5  5 110              30          2        0.400000     0.066667           57.466667                  52.5 0.486667           0.257348        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score            6  6 110              30          2        0.333333     0.066667           57.466667                  52.5 0.486667           0.257348        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score           10 10 110              30          2        0.200000     0.066667           57.466667                  52.5 0.486667           0.257348        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score           11 11 110              30          3        0.272727     0.100000           57.466667                  52.5 0.486667           0.257348        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score           20 20 110              30          5        0.250000     0.166667           57.466667                  52.5 0.486667           0.257348        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
             lof_score           22 22 110              30          5        0.227273     0.166667           57.466667                  52.5 0.486667           0.257348        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score            5  5 110              30          2        0.400000     0.066667           59.800000                  57.0 0.441667           0.245232        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score            6  6 110              30          3        0.500000     0.100000           59.800000                  57.0 0.441667           0.245232        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score           10 10 110              30          3        0.300000     0.100000           59.800000                  57.0 0.441667           0.245232        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score           11 11 110              30          3        0.272727     0.100000           59.800000                  57.0 0.441667           0.245232        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score           20 20 110              30          5        0.250000     0.166667           59.800000                  57.0 0.441667           0.245232        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
        ensemble_score           22 22 110              30          5        0.227273     0.166667           59.800000                  57.0 0.441667           0.245232        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score            5  5 110              30          1        0.200000     0.033333           53.200000                  54.5 0.486667           0.275668        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score            6  6 110              30          2        0.333333     0.066667           53.200000                  54.5 0.486667           0.275668        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score           10 10 110              30          2        0.200000     0.066667           53.200000                  54.5 0.486667           0.275668        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score           11 11 110              30          2        0.181818     0.066667           53.200000                  54.5 0.486667           0.275668        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score           20 20 110              30          5        0.250000     0.166667           53.200000                  54.5 0.486667           0.275668        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
          hybrid_score           22 22 110              30          6        0.272727     0.200000           53.200000                  54.5 0.486667           0.275668        40 Confirmed/known planets versus catalogue FP/FA only          NaN        physics
         bls_max_power            5  5 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power            6  6 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power           10 10 110              30          2        0.200000     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power           11 11 110              30          2        0.181818     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power           20 20 110              30          4        0.200000     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
         bls_max_power           22 22 110              30          4        0.181818     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr            5  5 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr            6  6 110              30          0        0.000000     0.000000           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr           10 10 110              30          2        0.200000     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr           11 11 110              30          2        0.181818     0.066667           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr           20 20 110              30          4        0.200000     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             depth_snr           22 22 110              30          4        0.181818     0.133333           47.766667                  49.5 0.556667           0.291416        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score            5  5 110              30          2        0.400000     0.066667           62.766667                  66.5 0.413333           0.224451        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score            6  6 110              30          3        0.500000     0.100000           62.766667                  66.5 0.413333           0.224451        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score           10 10 110              30          3        0.300000     0.100000           62.766667                  66.5 0.413333           0.224451        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score           11 11 110              30          3        0.272727     0.100000           62.766667                  66.5 0.413333           0.224451        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score           20 20 110              30          5        0.250000     0.166667           62.766667                  66.5 0.413333           0.224451        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
isolation_forest_score           22 22 110              30          5        0.227273     0.166667           62.766667                  66.5 0.413333           0.224451        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score            5  5 110              30          1        0.200000     0.033333           61.333333                  62.5 0.450000           0.235739        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score            6  6 110              30          1        0.166667     0.033333           61.333333                  62.5 0.450000           0.235739        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score           10 10 110              30          1        0.100000     0.033333           61.333333                  62.5 0.450000           0.235739        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score           11 11 110              30          1        0.090909     0.033333           61.333333                  62.5 0.450000           0.235739        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score           20 20 110              30          3        0.150000     0.100000           61.333333                  62.5 0.450000           0.235739        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
             lof_score           22 22 110              30          4        0.181818     0.133333           61.333333                  62.5 0.450000           0.235739        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score            5  5 110              30          1        0.200000     0.033333           62.333333                  64.5 0.431667           0.227628        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score            6  6 110              30          1        0.166667     0.033333           62.333333                  64.5 0.431667           0.227628        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score           10 10 110              30          1        0.100000     0.033333           62.333333                  64.5 0.431667           0.227628        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score           11 11 110              30          1        0.090909     0.033333           62.333333                  64.5 0.431667           0.227628        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score           20 20 110              30          4        0.200000     0.133333           62.333333                  64.5 0.431667           0.227628        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
        ensemble_score           22 22 110              30          5        0.227273     0.166667           62.333333                  64.5 0.431667           0.227628        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score            5  5 110              30          0        0.000000     0.000000           54.466667                  55.5 0.481667           0.255137        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score            6  6 110              30          0        0.000000     0.000000           54.466667                  55.5 0.481667           0.255137        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score           10 10 110              30          2        0.200000     0.066667           54.466667                  55.5 0.481667           0.255137        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score           11 11 110              30          2        0.181818     0.066667           54.466667                  55.5 0.481667           0.255137        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score           20 20 110              30          5        0.250000     0.166667           54.466667                  55.5 0.481667           0.255137        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
          hybrid_score           22 22 110              30          5        0.227273     0.166667           54.466667                  55.5 0.481667           0.255137        40 Confirmed/known planets versus catalogue FP/FA only          NaN            all
```

## Sector Coverage
```
         label  sectors  targets
    background        1       50
false_positive        1       30
        planet        1       30
```

## Top Candidates
```
   tic_id  sector          label disposition  best_period  best_depth  depth_snr  ensemble_score  hybrid_score
183979262       1 false_positive          FP     3.431573    0.008811 443.716988        0.954545      0.984091
 38686737       5 false_positive          FP     2.247803    0.020509 102.902019        0.954545      0.961364
 49899799       4 false_positive          FP     7.011261    0.006630 303.733006        0.900000      0.950000
  9804616       4 false_positive          FP     0.516991    0.017259  38.308962        0.950000      0.913636
325680697       4 false_positive          FP     1.824892    0.004851 138.102817        0.850000      0.913636
```

## Interpretation limits
Sector coverage differs between reference groups. Taking each target's maximum score across sectors gives more observed sectors more opportunities for a high score; group comparisons are not controlled for this exposure difference. Catalogue periods outside the search interval cannot be recovered directly within that interval, although harmonics may occur. Independent evaluation with exposure and search coverage accounted for is needed before claiming generalisation or reduced inspection workload.
The primary experiment uses unsupervised anomaly detection; catalogue labels are used only for evaluation. The LOF novelty helper does not constitute an evaluated semi-supervised experiment. Physics-informed means astrophysically motivated feature engineering, not physical equations enforced during training. Stellar-catalogue-dependent radius and duration-consistency proxies are extracted where possible but excluded from default ML inputs because measurement availability differs between groups.
Interpretability analyses describe properties associated with high anomaly scores. They do not establish causation, provide formal per-object model attribution, or calibrate anomaly scores as statistical significance. The primary models fit and rank the same unlabelled sample. Reduced manual inspection workload and generalisation remain research questions requiring independent evaluation.
No held-out generalisation or causal improvement is established. Background objects are unlabelled. Precision@K measures catalogue-positive yield, not true planet purity. ROC-AUC and average precision exclude PC-only and background targets. BLS power and depth SNR are identical rankings under the default SNR objective. Catalogue-conditioned stellar-feature missingness can bias physics ablations. Non-parametric p-values are exploratory and uncorrected for multiple comparisons.