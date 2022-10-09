---
title: "Predicting Out-of-Domain Generalization with Local Manifold Smoothness."
venue: "CoRR"
volume: "abs/2207.02093"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2207-02093"
doi: "10.48550/ARXIV.2207.02093"
ee: "https://doi.org/10.48550/arXiv.2207.02093"
url: "https://dblp.org/rec/journals/corr/abs-2207-02093"
authors: ["Nathan Ng", "Neha Hulkund", "Kyunghyun Cho", "Marzyeh Ghassemi"]
sync_version: 3
cite_key: "journals/corr/abs-2207-02093/Ng/2022"
---

Novel complexity measure based on local manifold smoothness of a classifier.

This is the classifier's sensitivity to perturbations in its input around a test point.

Neighbourhood decision distribution:

$$
p_j(x) = \frac{|\{x' \in N_{\mathcal{M}} : f(x') = j\}|}{|N_{\mathcal{M}}|}
$$

Smoothness is given as $\mu(f, x) = \max p_j(x)_{j \in \mathcal{Y}}$

$N_{\mathcal{M}}$ is the "neighbourhood manifold", eg, the set of points that are at distance at most $r$ away from the $x$ as measured in the original input space.

$\mathcal{Y}$ is the output space with $k$ classes. So this basically says that smoothness