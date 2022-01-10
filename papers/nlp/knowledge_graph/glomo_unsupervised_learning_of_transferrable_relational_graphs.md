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


