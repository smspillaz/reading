---
title: Generalized Value Iteration Networks - Life Beyond Lattices.
venue: AAAI
pages: 6246-6253
year: 2018
type: Conference and Workshop Papers
access: open
key: conf/aaai/NiuCGTSK18
ee: https://www.aaai.org/ocs/index.php/AAAI/AAAI18/paper/view/16552
url: https://dblp.org/rec/conf/aaai/NiuCGTSK18
authors: ["Sufeng Niu", "Siheng Chen", "Hanyu Guo", "Colin Targonski", "Melissa C. Smith", "Jelena Kovacevic"]
sync_version: 3
cite_key: conf/aaai/NiuCGTSK18
---
# Generalized Value Iteration Networks

tl;dr:
 - VIN applied to a graph, using a graph kernel for graph convolution.
 - Directional / spatial kernel
 - Episodic Q learning: Update trainable weights after each episode, instaed of after n steps.


## VIN Framework

![[gvin_framework.png]]

- Basically: graph with starting nodes and goal nodes
	- $r = f_R(g;w_r)$ ($w_r$ is weights for reward func)
	- $P^{(a)} = f_P(G; w_P^{(a)})$ ($w_P^{(a)}$ - graph convolution weight in $a$th channel)
	- $q^{(a)}_{n + 1} = P^{(a)} (r + \gamma v_n)$
	- $v_{n + 1} = \max_a q^{(a)}_{n + 1}$
- Instead of extracting action values from the neighbours, instead have a pseudo action of moving to one of your neighbours ($q_s = \max_{s' \in N(s)}$)
- 2D spatial kernel function $K(\cdot, \cdot)$
	- $P_{i, j} = A_{i, j} \cdot K_{w_{o}} (X_i, X_j)$
		- $i$ and $j$ are node indices
		- $X_i$ and $X_j$ are the embeddings of each node
		- $A$ is the adjacency matrix
		- Basic idea: Multiply adjacency matrix with graph dot product kernel. Result is a sparse matrix where each row corresponds to a node's neighbouring values. Taking max along the row gives you the max value.
- OK, but how to define $K_{w_P}(\cdot, \cdot)$?
	- Directional Kernel: $\sum^L w_l K_d^{t, \theta_t}(\theta) = (\frac{1 + \cos(\theta + \theta_l)}{2})^t$
		- Where the parameter $\theta$ is $\theta_{ij}$ - the direction of the edge connecting the $i$th and $j$th node. For example, $\theta_{ij} = X_i^TX_j$
		- $t$: Directional resolution
		- $w_l$: the weight with respect to reference direction $l$.
		- $\theta_l$ the trainable reference direction parameter
	- Spatial Kernel:
		- $\sum^L w_l K_s^{(d_t, t, \theta_t)}K(d, \theta) = I_{|d - d_{\epsilon}| \le \epislon} (\frac{1 + \cos(\theta - \theta^l)}{2})^2$
		- Basically the same as the directional kernel, but with a distance threshold.
	- Embedding
		- $P_{ij} = \frac{(I_{i = j} A_{ij})}{\sqrt{\sum_k (1 + A_{kj})\sum_k(1 + A_{ik})}} \text{MLP(X_i - X_j)}$
		- Basically normalized learned function based on embedding L1 norm distance.