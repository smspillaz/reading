---
title: Understanding Dataset Difficulty with V-Usable Information.
venue: ICML
pages: 5988-6008
year: 2022
type: Conference and Workshop Papers
access: open
key: conf/icml/EthayarajhCS22
ee: https://proceedings.mlr.press/v162/ethayarajh22a.html
url: https://dblp.org/rec/conf/icml/EthayarajhCS22
authors: ["Kawin Ethayarajh", "Yejin Choi", "Swabha Swayamdipta"]
sync_version: 3
cite_key: conf/icml/EthayarajhCS22
---

Proposes the idea of $\mathcal{V}$-usable information with respect to a model $\mathcal{V}$ for a more instructive metric of how difficult a dataset is.

The simple answer to how difficult a problem is, is to look at the mutual information between the data $X$ and the labels $Y$. High mutual information means that $X$ tells you a lot about $Y$, low mutual information means that knowing $X$ still means that $Y$ is noise.

However this doesn't say anything about the *form* of $X$. Eg, if $X$ is encrypted, the mutual information will actually stay the same because all that happened to $X$ is that it is was permuted in some way. But it might still be difficult for a model to understand because existing inductive biases sort of stop working.

What can PVI do in practice?
 - Find mislabelled instances
 - Find instances that are likely to be mispredicted ($\text{PVI} \ge 0.5$)

