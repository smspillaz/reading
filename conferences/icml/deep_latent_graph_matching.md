# Deep Latent Graph Matching

Deep learning for graph matching (GM) has emerged as an important research topic due to its superior performance over traditional methods and insights it provides for solving other combinatorial problems on graph. While recent deep methods for GM extensively investigated effective node/edge feature learning or downstream GM solvers given such learned features, there is little existing work questioning if the fixed connectivity/topology typically constructed using heuristics (e.g., Delaunay or k-nearest) is indeed suitable for GM. From a learning perspective, we argue that the fixed topology may restrict the model capacity and thus potentially hinder the performance. To address this, we propose to learn the (distribution of) latent topology, which can better support the downstream GM task. We devise two latent graph generation procedures, one deterministic and one generative. Particularly, the generative procedure emphasizes the across-graph consistency and thus can be viewed as a matching-guided co-generative model. Our methods deliver superior performance over previous state-of-the-arts on public benchmarks, hence supporting our hypothesis.

[[yu_deep_latent_graph_matching.pdf]]

https://icml.cc/virtual/2021/spotlight/8836



## Introduction

 GM - finding node correspondence across graphs.
 
 Existing methods under pre-calculated topology of graphs.
 
 Contributions:
  - Novel method to learn the distributions of latent topology of downstream tasks
  - Flexible to be equipped into existing GM methods
  - SOTA performance


## Latent Topology

If we can generate topology then we can find the correspondence between node .

## Formulation:

GM Formulation: $max_z z^T Mz \text{st} Z \in \{0, 1\}^{n \tmes n}, Hz = 1$

Learning based GM: $\max_{\theta} \prod_k P_{\theta} (Z_k|G_k^s, G_k^t)$

 - We use some probability, we use the parameter theta and maximize the probabiity.

With a distribution of latent topology: $\max \prod_k \int_{A_k^s, A_k^t} P_{\theta} (Z_k, A_k^s, A_k^t, G_k^s, G_k^t)$

 - We incorporate the latent topology $A$.

ELBO: $\log P_{\theta(Z|G^s, G^t) \ge E_{Q_{\phi}(A^s, A^t|G^s. G^t)} [\log P_{\theta}(Z, A^s, A^t|G^s, G^t) - \log Q_{\phi}(A^s, A^t|G^s, G^t)]$

 - We can instead optimize the evidence lower bound.


## Matching loss functions

 - Matching loss: Hamming loss
 - Locality loss: Hamming loss  - we want local connections
 - Consistency loss: The graphs should be isomophisms of each other.


## Optimization

![[deep_latent_graph_matching_dlgm-d_algorithm.png]]

EM-like optimization:
 - E-step: obtain predicted matching $Z$ using fixed $P_{\theta}$ and update $Q_{\psi}$ using the locality and consistency loss functions
 - M-step: Obtain predicted graph topology $A^s$ and $A^t$ using the $Q_{\phi}$ function and update $P_{\theta}$ using the matching loss.

## Model Architecture

![[deep_latent_graph_matching_model.png]]

There's a singleton pipeline for each source and target. Concatenating together those features gives you an affinity and this can be passed to the GM solver for the matching loss.

The singleton pipeline itself extracts local and global features from an image,.

