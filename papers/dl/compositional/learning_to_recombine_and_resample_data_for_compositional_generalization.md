---
title: "Learning to Recombine and Resample Data for Compositional Generalization."
venue: "CoRR"
volume: "abs/2010.03706"
year: 2020
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2010-03706"
ee: "https://arxiv.org/abs/2010.03706"
url: "https://dblp.org/rec/journals/corr/abs-2010-03706"
authors: ["Ekin Aky\u00fcrek", "Afra Feyza Aky\u00fcrek", "Jacob Andreas"]
sync_version: 3
cite_key: "journals/corr/abs-2010-03706/Akyurek/2020"
---

Train a generative model to reconstruct trianing pairs by constructing them from other trianing pairs.

Then do data augmentation by sampling from the reconstruction model.

The approach is called R&R.

What would a learned data augmentation process look like? It should automatically identify valid ways of transforming and combining examples without pre-committing to a fixed-set of transformations.

For example, prototype models:

$$
d \sim p_{\text{rewrite}}(\cdot|d';\theta), d; \sim \text{Uniform}(\mathcal{D})
$$
We do $p(d) = \frac{1}{|\mathcal{D}|} \sum_{d' \in \mathcal{D}} p_{\text{rewrite}}(d|d';\theta)$ , eg each data point must be explainable by at least one other example and a parametric rewriting operation.

Obviously if the dataset is big, then this is not tractable. However you can optimize the lower bound with respect to a neighbourhood of training samples around each $d$.

You need a set of "compatible prototypes", $\Omega \in \mathcal{D}^n$ .

How to get teh neigbhourhood?

 - 1-prototype neighbourhood: Use the jaccard distance, eg, the neighbourhood is given by given by data examples where the levensteihn distance is less than some $\delta$.
 - 2-prototype-neigbhourhood: We want each data example in the neighbourhood to collectively contain enough information to reconstruct $d$.
	 - Long-short strategy: Choose some $d_1$ that is similar to $d$, then choose some $d_2$ which has $\text{dist}(d_1, d) = \text{dist}(d_2, d), d_1 \ne d_2$.
	 - Long-long recombination: Choose many supports which are similar to $d$ and collectively contain all the tokens which are contained in $d$.