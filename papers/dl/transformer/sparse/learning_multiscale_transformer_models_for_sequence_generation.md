---
title: "Learning Multiscale Transformer Models for Sequence Generation."
venue: "ICML"
pages: "13225-13241"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/LiZJJXZ22"
ee: "https://proceedings.mlr.press/v162/li22ac.html"
url: "https://dblp.org/rec/conf/icml/LiZJJXZ22"
authors: ["Bei Li", "Tong Zheng", "Yi Jing", "Chengbo Jiao", "Tong Xiao", "Jingbo Zhu"]
sync_version: 3
cite_key: "conf/icml/LiZJJXZ22"
---

Contributions:
 - Re-define the concept of "scale" for NLP, including sub-word scale, word scale and phrase scale. Use word boundaries and phrase-level piror to compensate for sub-word features
 - Universal Multiscale Transformer: Extracting features from different scales, flexible with the opportunity to incorporate other prior knowledge.

The following relations exist:
 - Inter-individual relations: Between input tokens, eg subwords
 - Intra-group relations: sub-words can obtain word boundary information
 - Inter-group relation: relationship across groups.

To do this define an adjacency matrix for each of these groups on the input sentence, then use this as the edges for a graph neural network which you put in the transformer layers.