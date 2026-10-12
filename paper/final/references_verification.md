# Literature and reference verification

Editorial review date: 17 September 2026. This is a focused review of literature relevant to the implemented experiment, not a systematic review of every transit-search publication. The manuscript contains 14 research/software references plus directly linked archive and implementation documentation.

| Reference | Primary or official verification source | Supported use in this manuscript |
| --- | --- | --- |
| Ricker et al. (2015) | [Author manuscript](https://oar.princeton.edu/bitstream/88435/pr1871j/1/014003_1.pdf), [arXiv record](https://arxiv.org/abs/1406.0151) | TESS mission context. Journal issue year is 2015; the preprint and online publication appeared in 2014. |
| Kovács, Zucker and Mazeh (2002) | [Author record](https://arxiv.org/abs/astro-ph/0206099) and [A&A paper](https://www.aanda.org/articles/aa/pdf/2002/31/aa2422.pdf) | BLS as the periodic box-shaped transit-search baseline. No transfer of the original paper's performance thresholds to this experiment. |
| Shallue and Vanderburg (2018) | [Author manuscript and journal DOI](https://arxiv.org/abs/1712.05044) | Supervised Kepler candidate classification. The preprint is dated 2017; the journal citation uses 2018. |
| Yu et al. (2019) | [Author manuscript and journal DOI](https://arxiv.org/abs/1904.02726) | TESS supervised triage and vetting, distinguished from our host-ranking outcome. |
| Crake and Martínez-Galarza (2023) | [Author preprint](https://arxiv.org/abs/2301.10264) | Earlier unsupervised TESS anomaly analysis; dependence on the parent population. Cited as a preprint because the consulted record does not establish a journal publication. |
| Dasgupta (2025) | [Author preprint, version 4](https://arxiv.org/abs/2508.04722v4) | Related TESS transit work using synthetic-guided Unsupervised Random Forests and morphology. Preprint status is explicit; its detection rates are not compared numerically with ours. |
| Liu, Ting and Zhou (2008) | [Author paper](https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf), [author institution record](https://research.monash.edu/en/publications/isolation-forest/) | Isolation Forest, ICDM, pages 413–422. |
| Breunig et al. (2000) | [scikit-learn reference and algorithm documentation](https://scikit-learn.org/stable/modules/outlier_detection.html), [ELKI reference metadata](https://elki-project.github.io/releases/current/javadoc/elki/outlier/lof/LOF.html) | Local density scoring and original authors/title/year; ELKI confirms the proceedings DOI. The old author PDF redirects and the ACM page was inaccessible during verification, so no claim of a newly completed full-text review is made. |
| Hippke et al. (2019) | [Author manuscript and journal DOI](https://arxiv.org/abs/1906.00966) | Detrending and transit preservation. Our two-method pilot does not reproduce Wōtan or establish survey completeness. |
| Savitzky and Golay (1964) | [ACS publication record](https://doi.org/10.1021/ac60214a047) | Origin of the smoothing procedure; not evidence that our chosen window is optimal. |
| Lightkurve Collaboration (2018) | [Official citation instructions](https://lightkurve.github.io/lightkurve/about/citing.html) | Software acknowledgement, ASCL 1812.013. |
| Ginsburg et al. (2019) | [Author manuscript and journal DOI](https://arxiv.org/abs/1901.04520) | astroquery archive-query dependency. |
| Astropy Collaboration (2022) | [Official citation instructions](https://www.astropy.org/acknowledging.html), [author paper](https://arxiv.org/abs/2206.14220), installed package `__citation__` | Software acknowledgement. Package citation confirms ApJ 935, 167 and the DOI. |
| Pedregosa et al. (2011) | [JMLR publisher record](https://jmlr.org/papers/v12/pedregosa11a.html) | scikit-learn software acknowledgement, volume 12, pages 2825–2830. |

The official [MAST TESS page](https://archive.stsci.edu/missions-and-data/tess) verifies the public observation archive. The [NASA Exoplanet Archive TOI definitions](https://exoplanetarchive.ipac.caltech.edu/docs/API_TOI_columns.html) verify CP/KP/PC/FP/FA terminology. The local independent catalogue records identify the NASA Exoplanet Archive TAP service as their source. [Astropy BLS documentation](https://docs.astropy.org/en/stable/timeseries/bls.html) and [scikit-learn documentation](https://scikit-learn.org/stable/modules/outlier_detection.html) support the implementation descriptions; installed versions remain those recorded in the frozen package.

Some publisher endpoints restrict automated access. Where available, author manuscripts and official software citation records were used instead. Journal DOIs are retained as bibliographic identifiers even when their landing pages were inaccessible; such a restriction is not treated as a failed or nonexistent reference. Preprints are not represented as peer-reviewed publications. No performance claim is inferred solely from a paper title, and no external performance percentage is used to substantiate this experiment's results.

## Proofreading and scientific consistency

The revision expands abbreviations, identifies the 95% interval in the abstract, distinguishes successful processing of injections from successful signal recovery, and corrects the distinction between invalid non-positive raw flux and retained downward relative-flux deviations. It preserves the host-level outcome, label-informed development selection, unsupervised fitting, conditional bootstrap scope, incomplete labels and absence of demonstrated workload reduction.

The main comparison and uncertainty limits were checked against `tables/paired_primary_uncertainty.csv`; injection recovery and depth bias were checked against `tables/injection_trials.csv`. Numerical tables, figures, source, frozen models and the historical scientific archive are unchanged. Current editorial hashes and verification results are recorded in `editorial_revision_2026-09-17.json`.

The availability statement reflects the current local state: MIT-licensed code, public MAST observations and public catalogue services, but no assigned public repository URL or study-release DOI. A public release and author/affiliation and venue-specific formatting remain separate submission tasks. The manuscript does not invent an access link, deposition, author identity or promise of access on request.
