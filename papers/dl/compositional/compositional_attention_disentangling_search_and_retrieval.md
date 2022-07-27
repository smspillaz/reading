---
title: Compositional Attention - Disentangling Search and Retrieval.
venue: CoRR
volume: abs/2110.09419
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2110-09419
ee: https://arxiv.org/abs/2110.09419
url: https://dblp.org/rec/journals/corr/abs-2110-09419
authors: ["Sarthak Mittal", "Sharath Chandra Raparthy", "Irina Rish", "Yoshua Bengio", "Guillaume Lajoie"]
sync_version: 3
cite_key: journals/corr/abs-2110-09419/Mittal/2021
---

MH Key-value attention does two operations, search and retrieval.

This static pairing can lead to learning of redundant parameters and hinder generalization.

Proposes "Compositional Attention". Disentangles search and retrieval and composes them in a "dynamic, flexible and context-dependent manner" through an additional soft-compeittion stage. This can work well on out-of-distribution inputs.

![[compositional_attention_motivation.png]]

The example here is that in traditional MHA, you learn both a search and retrieval program, and both of those are coupled for each head. So for example, you might learn to search according to color and then retrieve according to shape. This means that you need at least 9 heads (shape/shape, shape/color, shape/location, color/shape, color/color, color/location, location/shape, location/color, location/location). This means that you learn "searching" 3 times over for each attribute type and "retrieval" 3 times over for each attribute type.

In contrast when they're disentangled, you only need to learn to search by color, or search by shape etc once, then learn to retrieve by shape or location once.

The way to do this is that you figure out which value sub-head to use for each head. Presumably that means that there is parameter sharing between heads as well.

![[compositional_attention_goyal_architecture.png]]

## Architecture in more detail

Define $S$ parallel search mechanisms:

$$
S_i = \text{softmax}(Q_iK_i^T)
$$

Then define $R$ different retrieval mechanisms

$$
R_{ij} = S_i V_j
$$

This gives you all the hypothetical retrievals per-search. You then do attention over the "retrieval queries" and "retrieval keys"

$$
\bar Q_i = X \bar W_q, \bar K_{ij} = R_{ij} \bar W_k
$$
# Experiments

At least for the SCAN dataset you can outperform the baseline at larger cutoff lengths.

On Sort-of-CLEVER, compositional transformer is doing marginally better.

Contextual Retrieval: Construct an OOD version of the dataset only showing certain ground truth search-retrieval combinations. Can the model recombine the search and retrieval heads for the OOD data?