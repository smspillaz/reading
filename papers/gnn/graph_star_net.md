---
title: Graph Star Net for Generalized Multi-Task Learning.
venue: CoRR
volume: abs/1906.12330
year: 2019
type: Informal Publications
access: open
key: journals/corr/abs-1906-12330
ee: http://arxiv.org/abs/1906.12330
url: https://dblp.org/rec/journals/corr/abs-1906-12330
authors: ["Haonan Lu", "Seth H. Huang", "Tian Ye", "Xiuyan Guo"]
sync_version: 3
cite_key: journals/corr/abs-1906-12330/Lu/2019
---
# GraphStar

Non-spectral methods conduct local convolutions, but to capture global state you need to
increase depth, which may result in over-smothing.

Graph Attention Networks: Use multi-head attention, but this does not allow for deep neighbourhood representation.
Star Transformer: Virtual message passing relay, reducing number of connections from quadratic to linear. (https://arxiv.org/abs/1902.09113)
   * Hub-and-spokes model, with local connections between neighbours in a sequence
   * Two phase update process - satellite nodes and relay nodes
   * On the first phase, update the hidden state of each node as $\bold{C^t_i} = [h^{t - 1}_{i - 1}; h^{t - 1}_{i}; e^i s^_{t - 1}]$ and $h^t_i = $\text{Att}(h_{t - 1}_i, C^t_i)$
     * Eg, C is a sequence of vectors, we take attention *just* over the neighbours last hidden states, the current node's embedding and the hub node
   * On the second phase, update the star by taking attention between the star and everything else.


GraphStar:
 - Perform inductive tasks on previously unseen graphs
 - Aggregate both local and long range information
 - Hierarchical representation of graphs in the relays


Three steps:
 - Star initialization
 - Update real nodes
 - Update stars

Initial representation:
 - $a_i = \text{softmax}(W_q F_{\text{mean}} f)$ (attention)

Real Node Update:
 - Node representation is normalized attention-weighted concatenation of added node-to-neighbourhood, node-to-star, node-to-self relations)

Star Update:
 - Multi-head attention between each node and a corresponding star node

Does pretty well on various benchmarks. Not sure where you put the stars, but a natural choice is to just
have one star and have all nodes connected to that.