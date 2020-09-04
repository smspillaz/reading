# GraphStar

Non-spectral methods conduct local convolutions, but to capture global state you need to
increase depth, which may result in over-smothing.

Graph Attention Networks: Use multi-head attention, but this does not allow for deep neighbourhood representation.
Star Transformer: Virtual message passing relay, reducing number of connections from quadratic to linear.

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
 - Node representation is attention-weighted concatenation of added node-to-star, node-to-self, node-to-neighbourhood relations)

Star Update:
 - 
