---
title: "An Empirical Study of Low Precision Quantization for TinyML."
venue: "CoRR"
volume: "abs/2203.05492"
year: "2022"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2203-05492"
doi: "10.48550/ARXIV.2203.05492"
ee: "https://doi.org/10.48550/arXiv.2203.05492"
url: "https://dblp.org/rec/journals/corr/abs-2203-05492"
authors: ["Shaojie Zhuo", "Hongyu Chen", "Ramchalam Kinattinkara Ramakrishnan", "Tommy Chen", "Chen Feng", "Yicheng Lin", "Parker Zhang", "Liang Shen"]
sync_version: 3
cite_key: "journals/corr/abs-2203-05492/Zhuo/2022"
---


-   FP model preprocessing: Cross-layer range equalization and outlier channel splitting, to rebalance tensor distributions.
-   Find clipping range and zero point
-   Optimization of the quantization function, eg, there can be errors introduced, so you want the right tradeoff. One way to do this is to go layer-by-layer, minimizing the divergence by optimizing scale and zero-point (trainable parameters) using the calibration data.