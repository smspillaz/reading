---
title: "Graph neural induction of value iteration."
venue: "CoRR"
volume: "abs/2009.12604"
year: 2020
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2009-12604"
ee: "https://arxiv.org/abs/2009.12604"
url: "https://dblp.org/rec/journals/corr/abs-2009-12604"
authors: ["Andreea Deac", "Pierre-Luc Bacon", "Jian Tang"]
sync_version: 3
cite_key: "journals/corr/abs-2009-12604/Deac/2020"
---

Motivation: GVIN generalizes VIN to graphs ([[gvin_life_beyond_lattices]]) but doesn ot account ofr the correspondences between value iteration and the graph convolution operator, making use of graph kernels instead.

# Architecture
Message-passing neural networks represent hte most generic form of graphc convolution. Basically nodes trade messages with each other and then update their state using an MLP.

For each MDP we provide separate graphs $G_{a_i}$ for each action $a_i$ using $s$ as nodes and featureized as followed.

 - $x_s = (v(s), r(s, a_i))$ containing the previous value function estimate and reward model.
 - Edges: $e_{s, s'} = (\gamma, p(s'|s, a_i))$, which is the discount factor of the transition model.

Alignment between value iteration and MPNNs:
 - MPNN message function corresponds to taking product of edge features with value function estimate in the neighbours
 - Aggregation over neighbours corresponds to taking a sum over $s'$
 - MPNN readout function $U$ corresponds to summing the reward model
 - Maximization over actions is aligned with taking elementwise maz in computes $h_s^{(a_i)}$ within each $G_{a_i}$


The general idea here is to "teach" a GNN to do value iteration, rather than explicitly doing it. So you just create lots of random graphs with different reward functions and different node/edge distributions and test the hypothesis on unseen graph structures.

# Experiments
Train message passing networks on transition models following Erdos-Reny graphs with 20 states and 5 actions. Perform the traiing using teacher forcing and at test time perform rollouts of the RNN.