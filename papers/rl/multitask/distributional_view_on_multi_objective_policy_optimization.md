---
title: "A distributional view on multi-objective policy optimization."
venue: "ICML"
pages: "11-22"
year: 2020
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/AbdolmalekiHNS20"
ee: "http://proceedings.mlr.press/v119/abdolmaleki20a.html"
url: "https://dblp.org/rec/conf/icml/AbdolmalekiHNS20"
authors: ["Abbas Abdolmaleki", "Sandy H. Huang", "Leonard Hasenclever", "Michael Neunert", "H. Francis Song", "Martina Zambelli", "Murilo F. Martins", "Nicolas Heess", "Raia Hadsell", "Martin A. Riedmiller"]
sync_version: 3
cite_key: "conf/icml/AbdolmalekiHNS20"
---
# A Distributional View on Multi-Objective Policy Optimization

Multi-objective policy optimization: We have multiple objectives that
we want to optimize for - say we get some reward for exploration, some
reward for finding the goal, some reward for staying within certain bounds
etc.

Typically you'd do this by weighting the rewards with some sort of
linear combination. This is difficult to do unless you know what the
scale of the rewards are, and it isn't scale invariant.

Basic idea behind this paper: Take a distributional approach
to policy optimization. You start out with a Q function and
a policy which maximizes your total return, but then since
you have multiple objectives 1, ..., k, you can make another
action distribution q_k(a|s) which maximizes Q_k (eg, the
Q only for that objective).

Then to combine the policies, you don't optimize the main
policy directly. Instead what you do is you optimize
each of the $q_k(a|s)$ distributions, subject to some
KL divergence between the $\pi_{\theta}^{\text{old}}$ and
$q_k(a|s)$ being less than $\epsilon_k$ (step (1)). Here $\epsilon_k$
is encoding a *preference*, eg, the larger the $\epsilon_k$, the
more $q_k$ is allowed to diverge from the old policy.

Then you update the $\pi_{theta}$ based on
the KL divergence between each $q_k$ and $\pi_{theta}$ (plus
some regularization based on KL divergence between the old policy
and the new one).

## Choosing $\epsilon_k$

The authors say here that when you choose $\epsilon_k$, you're
more invariant to the scale of the reward (which is true, you don't
depend on the reward at all, only the optimal distribution of actions
for each $q_k$, which sums to 1.

*however*, you should be careful not to set $\epsilon_k$ too high
since this functions a bit like a learning rate - setting it
too high causes you to trust each individual Q function more,
which might not be a good idea when you have a limited number
of samples.