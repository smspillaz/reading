---
title: "Disentanglement of Correlated Factors via Hausdorff Factorized Support."
venue: "CoRR"
volume: "abs/2210.07347"
year: "2022"
type: "Informal and Other Publications"
access: "open"
key: "journals/corr/abs-2210-07347"
doi: "10.48550/ARXIV.2210.07347"
ee: "https://doi.org/10.48550/arXiv.2210.07347"
url: "https://dblp.org/rec/journals/corr/abs-2210-07347"
authors: ["Karsten Roth", "Mark Ibrahim", "Zeynep Akata", "Pascal Vincent", "Diane Bouchacourt"]
sync_version: 3
cite_key: "journals/corr/abs-2210-07347/Roth/2022"
---

What's the problem?

Traditional disentanglement assumes that:

$$
p(\mathbf{z}) = \prod p(z_i)
$$

eg, that the probability of a particular combination is the probability of the marginal components.

But this isn't true for most data.

What's a relaxiation on this?

Assume that the *support* of the distribution factorizes. Eg,$\mathcal{S}(p(\mathbf{z}))$ is the *support* of $p$. It is the set $\{\mathbf{z} \in \mathcal{Z}|p(\mathcal{z}) > 0)\}$

We say that $\mathcal{S}$ is factorized if it equals the cartesian product of supports over individual dimension marginals:

$$
\mathcal{S}(p(\mathbf{z})) = \prod \mathcal{S}(p(z)) \implies \mathcal{S}^{\times}(p(\mathcal{z}))
$$

Note that factorized support does not imply independence, but independence does imply factorized support.

All factorized support is saying is that for any given combination, that is at least *possible*, even if it isn't *probable*.

Reminder: Hausdorff Distance is:

$$
d_h(\mathcal{S}, \mathcal{S}^{\times}) = \max (\sup_{z \in \mathcal{S}^{\times}} [\inf_{z' \in \mathcal{S}} d(z, z')], \sup_{z \in \mathcal{S}}[\inf_{z' \in \mathcal{S}^{\times}} d(z, z')]) = \sup_{z \in S^{\times}}[\inf_{z ' \in \mathcal{S}} d(z, z')]
$$

Eg, for each $z$ in $\mathcal{S}^{\times}$, you find point $z'$ in $\mathcal{S}$ with the smallest distance, then you take the biggest distance out of all of those smallest distances.

How does that help in our case? Recall that $\mathcal{S}(p(z))$  is the *support* of the distribution (eg, any $z$ where $p(z) > 0$) and $\mathcal{S}^{\times}(p(z))$ is the *cartestian product of the support*, eg, if we were to take the components of $z$, we have the supports for $z_1$ ($\mathcal{S}(p(z_1)))$, the supports for $z_2$ and so on, then we take all the combinations of those things.

To give a concrete example, say that we have latents where the components correspond to different properties of a thing

| Color | Size | Shape |
|-----|-----|-----|
| Red, Blue, Yellow | Big, Small | Square, Circle |

Now lets say that we have the following observations

| Observation | Attribute | Value |
| ------------| ---------| ------|
| (1) Red Big Square | Color | Red |
| (1) Red Big Square | Size | Big |
| (1) Red Big Square | Shape | Square |
| (2) Small Blue Circle | Color | Blue |
| (2) Small Blue Circle | Size | Small |
| (2) Small Blue Circle | Shape | Square |
| (3) Big Yellow Square | Color | Yellow |
| (3) Big Yellow Square | Size | Big |
| (3) Big Yellow Square | Shape | Square |

We would have the following supports for $\mathcal{S}(p(z))$

 - Red Big Square
 - Small Blue Circle
 - Big Yellow Circle

We would have the following supports for $\mathcal{S}(p(z_1))$

 - Red
 - Blue
 - Yellow

We would have the following supports for $\mathcal{S}(p(z_2))$

 - Big
 - Small

We would have the following supports for $\mathcal{S}(p(z_3))$

 - Circle
 - Square

Then we would have the following cartesian product supports $\mathcal{S}^{\times}{p(z)}$

 - Red Big Square
 - Red Big Circle
 - Red Small Square
 - Red Small Circle
 - Blue Big Square
 - Blue Big Circle
 - Blue Small Square
 - Blue Small Circle
 - Yellow Big Square
 - Yellow Big Circle
 - Yellow Small Square
 - Yellow Small Circle

How do we measure the distance between these? Note that $d(\mathbf{z}, \mathbf{z}')$ is a distance metric between *any two latents*. It can be euclidean distance or cosine distance.

So, what the paper says is that for the *product of all possible combinations of latent codes where each component has some probability* and the *set of latent codes which have some probability*, we want to minimize the hausdorff distance, which is the largest smallest distance between any two pairs of codes in both sets. This means that you minimize cases where things exist in the product set but don't exist in the set of observed latent codes with *some* probability.