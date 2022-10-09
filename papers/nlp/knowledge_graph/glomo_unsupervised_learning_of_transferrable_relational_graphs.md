---
title: "GLoMo: Unsupervised Learning of Transferable Relational Graphs."
venue: "NeurIPS"
pages: "8964-8975"
year: 2018
type: "Conference and Workshop Papers"
access: "open"
key: "conf/nips/YangZDHCSL18"
ee: "https://proceedings.neurips.cc/paper/2018/hash/5dbc8390f17e019d300d5a162c3ce3bc-Abstract.html"
url: "https://dblp.org/rec/conf/nips/YangZDHCSL18"
authors: ["Zhilin Yang", "Junbo Jake Zhao", "Bhuwan Dhingra", "Kaiming He", "William W. Cohen", "Ruslan Salakhutdinov", "Yann LeCun"]
sync_version: 3
cite_key: "conf/nips/YangZDHCSL18"
---
# GLoMo: Unsupervised Learning of Transferrable Relational Graphs

Basic idea: given some input sequence (eg, a sentence, something else),
predict an NxN affinity matrix indicating potential relationships between
tokens, then conditionally generate features using the affinity matrix.

## Graph Predictor

Two multi-layer CNNs, query and key.

Key produces sequence of convolutional features and query produces
similarity outputs.

$$
G_{ij}^l = \frac{(\text{relu}(k^{lT}_i q^l_j + b)^2}{\sum_{i'}(relu(k^{lT}_{i'} q^l_j + b))^2}}
$$