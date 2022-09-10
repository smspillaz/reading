---
title: Weakly-Supervised Disentanglement Without Compromises.
venue: ICML
pages: 6348-6359
year: 2020
type: Conference and Workshop Papers
access: open
key: conf/icml/LocatelloPRSBT20
ee: http://proceedings.mlr.press/v119/locatello20a.html
url: https://dblp.org/rec/conf/icml/LocatelloPRSBT20
authors: ["Francesco Locatello", "Ben Poole", "Gunnar R\u00e4tsch", "Bernhard Sch\u00f6lkopf", "Olivier Bachem", "Michael Tschannen"]
sync_version: 3
cite_key: conf/icml/LocatelloPRSBT20
---

The theory here is that if we only know *how many* factors have changed, but not which ones, then this is sufficient to learn a disentangled representation.

The idea is basically that under a generative model of the world, you can change N covariates in the image by changing N covariates in the latents and holding the rest fixed.

The way it works is that you take paired observations, for which you know some, but not all factors, have changed.  Typically you would hold $k$ constant.

The generative model looks like:

$$
p(z) = \prod^d p(z_i)
$$

$$
p(\bar{z}) = \prod^k p(\bar{z})
$$

where $x_1 = g^*(z)$ and $x_2  = g^*(f(z, \bar{z}, S))$

What this is saying is that our generative process generates $x_1$ from $z$ and $x_2$ by some function of $z, \bar{z},$ and $S$.

You sample the subset $S$ from all of the indices, where $S$ has size $k$. Then you require that:

$$
f(z, \bar{z}, S)_S = z_S
$$
and 
$$
f(z, \bar{z}, S)_{\bar{S}} = \bar{z}
$$


What does this mean? It means that if you take $z$  and substitute in the "correct" factors $S$ from $\bar{z}$, you should get $x_2$. 

How do you pick $S$? You can make every combination of $S$ of size $k$ from $d$, then pick the one with the smallest KL.

How do you ensure that this works at inference time? You train the model such that the indices with the smallest KL end up minimizing their KL, eg, for any two given images that share $k$ factors, they will have $k$ indices that are the same. You don't specify *which* indices, just the number.