---
title: Language modeling via stochastic processes.
venue: CoRR
volume: abs/2203.11370
year: 2022
type: Informal Publications
access: open
key: journals/corr/abs-2203-11370
doi: 10.48550/ARXIV.2203.11370
ee: https://doi.org/10.48550/arXiv.2203.11370
url: https://dblp.org/rec/journals/corr/abs-2203-11370
authors: ["Rose E. Wang", "Esin Durmus", "Noah D. Goodman", "Tatsunori Hashimoto"]
sync_version: 3
cite_key: journals/corr/abs-2203-11370/Wang/2022
---

## Encoder
Contrastive loss with metrics induced by Brownian bridge dynamics (conditioned brownian motion).

Distribution of the t'th sentence embedding $z_t$ conditioned on $z_0$ and $z_T$

$$
p(z_t|z_0, z_T) = \mathcal{N}((1 - \frac{1}{T}z_0) + \frac{t}{T} z_t, \frac{t(T - t)}{T})
$$

The point of this is that you're most uncertain in the middle of the trajectory and most certain towards the two ends.

You can get a contrastive loss out of this, which is basically triplet NCE loss, where you minimize the expected distance of the middle point.

Sample three sentences from each document - use the middle sentence as a positive example and other sentences as negative examples.

We draw a line between $f(x_0)$ and $f(x_T)$ and we select a point on that line which is proportional to $t$. The distance is weighted by the distance.

We want a random process to stay in the space of coherent possibilities of where the dialogue is going to go for example.

## Generation

Time control generates text conditioned on a latent plan.

Pick the density model for the first phrase and the last phrase and then sample from that.

But when you want to produce something you don't know what the last sentence is.

## Experiments

### Order prediction task
Order prediction task: Given two sentences from the same document, can different models predict their original order?

Feed latents in order or out of order to a linear classifier and train classifier to predict if order is correct or swapped.

### Global Text Dynamics Task

In structured text - is the length of the various generated sections in line with the training distribution.
