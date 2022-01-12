# On Disentangled Representations Learned from Correlated Data

The focus of disentanglement approaches has been on identifying independent factors of variation in data. However, the causal variables underlying real-world observations are often not statistically independent. In this work, we bridge the gap to real-world scenarios by analyzing the behavior of the most prominent disentanglement approaches on correlated data in a large-scale empirical study (including 4260 models). *We show and quantify that systematically induced correlations in the dataset are being learned and reflected in the latent representations, which has implications for downstream applications of disentanglement such as fairness.* We also demonstrate how to resolve these latent correlations, either using weak supervision during training or by post-hoc correcting a pre-trained model with a small number of labels.

https://icml.cc/virtual/2021/oral/9352

[[trauble_on_disentangled_representations_learned_from_correlated_data.pdf]]

[[trauble_on_disentangled_representations_learned_from_correlated_data]]

Question: What about extremely correlated data? Authors only tested $\sigma = 0.2$ as the most extreme correlation case?