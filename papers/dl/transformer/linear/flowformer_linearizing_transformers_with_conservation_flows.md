---
title: Flowformer: Linearizing Transformers with Conservation Flows.
venue: ICML
pages: 24226-24242
year: 2022
type: Conference and Workshop Papers
access: open
key: conf/icml/WuWXWL22
ee: https://proceedings.mlr.press/v162/wu22m.html
url: https://dblp.org/rec/conf/icml/WuWXWL22
authors: ["Haixu Wu", "Jialong Wu", "Jiehui Xu", "Jianmin Wang", "Mingsheng Long"]
sync_version: 3
cite_key: conf/icml/WuWXWL22
---

Attention has quadtratic complexity, previous methods rely on similarity decomposition and associativity of matrix multiplication to deivse a linear time attention. The problem with decomposition is that you're not able to take the softmax anymore, so this can result in degenerate attention. The point of the softmax is to introduce competition amongst the tokens, eg, enforcing higher attenton only to essential tokens and avoiding near-uniform attention weights. But this is inherently a quadratic operaton.

In this paper, they linearize transformers free from specific inductive biases based on flow network theory. They cast attention as information flow from sources to sinks through learned flow capacities.

Apply the property of flow-conservation. Flowformer does wel on long sequences, time series, vision, NLP and RL.

Recall that with linear transformers, we can decompose as follows:

$$
S(Q_i, K_j) = \phi(Q_i) \phi(K_j^T)
$$

Then we can abuse this to reduce the complexity via associativity:

$$
R_i = \sum^m_{j = 1} = \frac{\phi(Q_i) \phi(K_j^T)}{\sum^m_{j' = 1} \phi(Q_i) \phi(K_{j'}^T)} V_j
$$

$$
R_i = \phi(Q_i) \sum^m_{j = 1} = \frac{\phi(K_j^T) V_j}{\phi(Q_i) \sum^m_{j' = 1} \phi(K_{j'}^T)}
$$

Once you do this the complexity is quadratic in feature size and not sequence lenghth size. The problem is specifying what $\phi$ is. Approximating softmax as an inner product space is hard.

Other related work:
 - [[reformer]]
 - [[performer]]
 - [[linformer]]
 - cos-former

If you look at this from a flow-network viewpoint, you have $R$ (or in other words, $A$) which is a "sink" and $V$ which is the source. Then $S(Q, K)$ is a matrix $QK^T$ which defines the flow capacity.