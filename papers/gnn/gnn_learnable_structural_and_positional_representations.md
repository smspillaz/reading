---
title: Graph Neural Networks with Learnable Structural and Positional Representations.
venue: CoRR
volume: abs/2110.07875
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2110-07875
ee: https://arxiv.org/abs/2110.07875
url: https://dblp.org/rec/journals/corr/abs-2110-07875
authors: ["Vijay Prakash Dwivedi", "Anh Tuan Luu", "Thomas Laurent 0001", "Yoshua Bengio", "Xavier Bresson"]
sync_version: 0
---

Problem: GNNs are designed to aggregate local neighbourhoods, so if an isomorphism exists between two non-intersecting N-balls then those two nodes get the same representation within the graph. See also the WL-test.

How to allieviate this problem?

 - Stack layers (N + 1 layers to deal with the N-ball problem)
	 - Can be deficient for long-distances due to over-squashing
 - Apply higher-order GNNs
	 - Higher order node-tuple agregations (WL-based GNNs), expensive
 - Conisdering positional encodings of nodes and edges
	 - Assign nodes a global position (eg, observed location)
	 - Requires this information

Contribution:
 - Learn positional representations that can be combined with structural GNNs.
 - Overcome lack of canonical positioning
 - Learn both position embeddigns and structural embeddigns at the same time.

Prior work on positional encoding:
 - Assign each node on the graph in the training data a position index. Requires n! possible permutations or sampling.
 - Laplacian Eigenvectors, but there is sign ambiguity in this case, so there are $2^k$ possible sign values when selecting the $k$ eigenvectors to learn.
 - Random anchor sets

## Architecture

* Decouple structural and positional representations
* Node update: $f_h(\begin{bmatrix}h^l_i \\ p^l_i \end{bmatrix}, \begin{bmatrix}h^l_j \\ p^l_j \end{bmatrix}_{j \in N_i}, e^l_{ij})$
* Edge update: $f_e(h^l_i, h^l_j, e^l_{ij})$
* Position update: $f_p(p^l_i, \{p^l_j\}_{j \in N^i}, e^l_{ij})$

The main difference here is that you concatenate the positional features to the node representations on each layer. (Note, there's a different position representation at each layer, eg $p^l$!). To update the positional information for the next layer, its a function of the positional information and edge information.

## Initial Positional Encodings

 - Laplacian PE (LapPE)
 - Random Walk PE (RWPE)

LapPE has sign ambiguity. RWPE is similar to PageRank, where you set $AD^{-1}$ as the random walk operator (eg, the transition probabilities are adjacency times inverse-degree)

RWPE provides a unique node representation on the condition that each node has a unique $k$-hop topological neighbourhood at a sufficiently large $k$.

 - Obviously this does not work for cycles or other such similar graphs where there are isomorphisms

"Precisely we use a k-dim vector that encodes the landing probabilities of a node i to itself in 1 to k steps""

There's some extra information on how this works provided in supplementary A.1

## Positional Loss

Laplacian Eigenvector Loss: $\mathcal{L}(p) = \frac{1}{k} \text{tr}(p^T \triangle p) + \frac{\lambda}{k} ||p^Tp - I_k||^2_F$

Add an $\alpha$ weighted eigenvector loss term to the task loss.

## Gated GCN-LSPE

In this case $p^{l + 1}_i = p^l_i + \text{tanh}(C^l_1 p^l_i) + \sum_{j \in N_i} \eta^l_{ij} \cdot C_2^l p_j^l$

($C_1$ and $C_2$ are matrix-valued parameters).


## Experiments

 * ZINC
 * OGBG-MOLTOX21
 * OGBG-MOLPCBA (437.9K graphs)

Results show that PE helps in pretty much all cases (eg, where there are different architectures)


## Ablations

 * Learning PE at every layer gives you the best performance
 * Choice of $k$ steps to initialize RWPE. Needs to be quite large. Need to do some big steps to get a unique representation.