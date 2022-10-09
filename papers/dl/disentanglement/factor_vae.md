---
title: "Disentangling by Factorising."
venue: "ICML"
pages: "2654-2663"
year: 2018
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/KimM18"
ee: "http://proceedings.mlr.press/v80/kim18b.html"
url: "https://dblp.org/rec/conf/icml/KimM18"
authors: ["Hyunjik Kim", "Andriy Mnih"]
sync_version: 3
cite_key: "conf/icml/KimM18"
tags: ["DeepMind"]
---
This paper aims to improve upon $\beta$-VAE by encouraging the distribution of representations to be factorial and hence independent.

$\beta$-VAE has a problem with reconstruction quality. Why does this happen? Look at the objective:

$$
\frac{1}{N} \sum^N [E_{q(z|x^{(i)})} [\log p(x^{(i)}|z)] - \beta \text{KL}(q(z|x^{(i)})||p(z))]
$$

The first time is re-construction error. But the KL term can be re-expressed as such:

$$
I(x;z) + \text{KL}(q(z)||p(z))
$$

If you increase $\beta$ too much, then what happens is that you also penalize $I(x;z)$, eg, at some point there will be no correlation between $x$ and $z$.

One thing we could do is penalize $\text{KL}(q(z)||\bar{q}(z))$, where $\bar{q}(z) = \prod^d q(z_j)$ .

## Algorithm

To sample $q(z)$ we can choose a datapoint $x$ and sample $q(z|x)$.

To sample $\bar{q}(z)$ its a bit trickier. But you can generate $d$ samples from $q(z)$ and permute across the batch for each latent. Eg:

$$
\begin{bmatrix}
q_{11} & q_{12} & q_{13} & q_{14} \\
q_{21} & q_{22} & q_{23} & q_{24} \\
q_{31} & q_{32} & q_{33} & q_{34} \\
q_{41} & q_{42} & q_{43} & q_{44} \\
\end{bmatrix}
$$

Say that the first dimension is the batch dimension and the second dimension is the latent dimension. One possible permutation is:

$$
\begin{bmatrix}
q_{41} & q_{32} & q_{23} & q_{14} \\
q_{21} & q_{22} & q_{43} & q_{44} \\
q_{11} & q_{42} & q_{33} & q_{24} \\
q_{31} & q_{12} & q_{13} & q_{34} \\
\end{bmatrix}
$$

As long as the batch is large enough, we hypothesize that this approximates $\bar{q}(z)$.

Then to minimize the KL divergence, use the *density-ratio* trick. Eg, train a discriminator to vote whether a given $z$ is from $q(z)$ or from $\bar{q}(z)$. Then train the encoder to generate samples such that $q(z)$ looks like $\bar{q}(z)$ to the discriminator, eg, the latents are independent of each other.

In this way the mutual information between $x$ and $z$ is still the same, but we penalize entanglement explicitly.