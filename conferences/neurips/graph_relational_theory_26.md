# Graph / Relational / Theory

## Graph Cross networks and Vertex Infomax Pooling

### Background

Graph Neural Networks - applications to: 
 - Vertex classification, link prediction, graph classification, community detection, net evolution, matching etc
 - Most GNNs only deal with single-scale information, but neglect multi-scale information
 - Skips long-range features


Other methods:
 - Encoder/decoder
 - Graph u-net
 - Readout

Existing trainable graph pooling methods:
 - Vertex-selection based
 - Graph coarsening based

Spectral perspective and vertex perspective

Basic idea behind Graph Cross Network (GXN): Interchange of intermediate features across scales

### VIPool

Select the most informative set of vertices based on neural estimation of mutual information between
vertex features and neighbourhood features. Vertex is "informative" if it reflects the neighbourhood
information.

The idea is that this preserves the original graph structures after downscaling.

DiffPool: Existing methods average neighbourhoods into a single node. Breaks the vertex-vertex association

SAGPool: Daamages the graph structure

Vertex Infomax Pooling:

 (1) Mutual information neural estimation

  - MI: = $D_f(P_{v, n}||Pv \times P_n)$
  - Consider features of vertex and neighbourhood as a positive sample,
    features of other picked vertex and neighbourhood as a negative sample
  - Neighbourhood representation picked via r-hop graph convolutions
  - Parameterize a function of log-sigmoids to estimate the mutual information.
    and optimize to differentiate far away neighbourhoods from close ones.

 (2) Solution for vertex selection

  - Select top-K vertices that have the highest estimated mutual information with their neighbourhoods

 (3) Graph pooling and unpooling

  - Compute affinity score between each vertex and its neighbourhoods
  - Pooling

### GXN

 - First step: Use VIPool to pool the graph into multiple scales (recursive application)
 - Then construct branches in parallel. Use graph convolution networks across consecutive scales
 - Each layers carriers multi-scale information for embedding
 - Use graph pooling to aggregate the multiscale representation

### Feature crossing layers

 - Enhance the flow of multi-scale information

# Erdos goes Neural: Unsupervised learning framework for combinatorial optimization on graph

Combinatorial optimization problems on graphs - optimize a cost function given a graph

 - Eg, find a subset of nodes that minimize a problem subject ot some constraint
 - Eg, Graph partitioning, maximum clique.
 - Problems like this are NP-hard, but we can produce high quality solutions for a given data distribution

Learning paradigm:

 - Unsupervised learning - more stable training, don't need labels.
 - Don't need to compute labels.
 - Hard to guarantee the feasibility of solutions that you produce.


How do do unsupervised learning that ensures the feasibility of the discrete solution.

Steps:

 (1) Construct a GNN that produces a probibility that a node belongs to a solution
 (2) Derive a special loss function for the problem
   - Optimizes probability that a discrete local feasible solution exists
 (3) Recover such a discrete feasible solution from the probabilities

Approach differs from other approaches: - guarantee the feasibility of the solutions
using probabilistic methods.

Probabilistic method:
 - Prove the existence of a set of nodes $S$ with desired properties:
   - Define a probability distribution over space of all possible sets $S$
     - Learn it by the GNN
     - Optimize P by minimizing derived loss function
   - Show that probability is positive
   - Desired objective must exist!

Derived loss function:
 - Probabilistic penalty approach
   - Differentiable loss on the GNN output distribution $D$
   - $\text{loss}(D, G) = E[f(S; G)] + P(S \not \in \Omega) \beta$
    - $D$ is the output distribution of GNN over graph nodes.
    - Expected cost plus probability of constraint violation
    - Hyperparameter $\beta$ controls sensitivity of probability of constraint violation
   - Let $f$ be non-negative. Then there exist a set $S* \sim D$ that satisfies $f(S*; G) < \text{loss(D; G)}, S* \in \Omega$ with $P > 0$
   - Take-away: by minimizing the loss, the GNN provides us with the certificate of the existence of a low-cost feasible solution
   - But how to find it?
 - Linear box constraints

Method of conditional expectation:
 - One way is to just sample: But the probability of the desired object may be low
 - Key idea: visit all nodes of the graph sequentially and add them to the solution if they improve the expected cost
   - Condition on all the decisions we made on the previous step

Case studies:

 - max-clique:
   - find clique of largest weight:
   - $\min_{S \subset V) \sim w(s)$ st $S \in \Omega_{\text{clique}}$
   - $l_{\text{clique}}(D, G) = \gamma - (\beta + 1) \sum_{(u, v) \in E} w_{ij}p_ip_j + \frac{\beta}{2} \sum_{v_i \ne u} p_i p_j$
   - reported approximation ratios: we can outperform neural baselines and other heuristics.
 - graph partitioning (min-cut)

nice things about this approach:
 - scales nicely
 - decent approximation ratios where you're not OOD
 - greedy is currently the best approach, but promising research direction.


Some problems seem to be better suited for GNNs than others eg clustering.

## Graph Random Neural Networks for SSL on Graphs

In practice GNNs have many issues. Each node is highly dependent on its neighbourhoods, making it non-robust to noisy neighbours.

 - GNN is very susceptible to adversarial inputs
 - GNN is basically laplacian smoothing, stacking them just makes the embeddings more blurry
 - SSL: standard training method can over-fit to scare label information information

### Data Augmentation for SSL on Graphcs

CNNs improve learning the distribution by data augmentation.

 - Random Propagation
  - DropNode: Drop entire features of selected nodes
    - Row-vectors of $X$
  - Decouple feature propagation from feature transformation

### Graph-Random Neural Network (GRAND)

 - Consistency Regularized Training
   - Generate S data augmentations of graph
   - Optimize consistency, minimize prediction discrepancy

 - We do random propagation multiple times, then optimize consistency of multiple augmentations
 - Take average of node distributions, sharpening the distribution to compute label
 - Consistency loss in training

 - Algorithm: Basically apply DropNode, perform propagation, predict class distribution S times
   - Then compute consistency regularization loss via eq. 6

 - This data augmentation helps quite a lot!


### Pointer Graph Networks

We're trying to re-use concepts within classical algorithms within neural networks.

GNNs typically applied to static graphs that you know upfront

 - what about when you don't know the graph? sometimes you have to infer a "latent" graph
 - introduces "Pointer Graph Networks"

Basic Idea:

 - Augment sets or graphs with inferred edges
   - dynamic pointers
 - Learn poiner-based data structures

Algorithmic inputs:

 - Commonly they are graphs
 - Are input grpah edges most relevant
 - Incremental connectivity task: edges connected one at a time, eg, "query: 'are nodes i and j connected'"

Connectivity within disjoint-set-unions
 - We can answer connectivity queries sublinearly

Try to learn an auxilary graph for GNNs to use
 - We let each vertex learn one pointer to another vertex
 - You can already generalize this to trees

PGNN:
 - Given some latent space, an operation embedding and some pointers
  - compute new latent, masks, pointers at timestep t, outputs y

 - How to compute the pointers?
  - Transformers - compute the attention coefficients on the vertex
  - Pick the biggest ones as the new pointers, forming "pointer adjacency matrix"
  - Use this pointer adjacency matrix to form neighbourhoods in the GNN
  - Optimize by cross-entropy loss to ground-truth data structure state.

 - What makes data structures efficient is the fact that they only update a subset a subset
  - Use the "masking" inductive bias
    - figure out which vertex pointer should get updated by computing a mask
    - this step is critical for scaling!
  - Need teacher forcing because applying pointers and masking is non-differentiable

 - Pointer accuracies - seems to have learned the data structure effectively
 - Longer-term impact:
   - Learned executors can reason like algorithms
   - Plug an executor into a related problem and then freeze it.
   - Replace the algorithm with a "learned" algorithm executor.
   - Directly operate on the data without having to do FE for the algorithm
   - Differentiable algorithm!

## Convergence and Stability of GCNs on large random graphs

 - Theoretical properties of GNNs on large graphs
 - Pick two large graphs that look the same, but are actually totally random
   - Train a GNN to separate communities on left graph
    - It performs well on the right graph, even though both are random graphs!

 - can GNNs distinguish graph isomorphisms? k-WL test
 - large graphs highly likely to be isomorphic.


 - stability to input change:
   - if two graphs are roughly the same, the outputs should be roughly the same
   - CNN: translation invariant
   - GNN: stability to discrete graph metrics
     - what is "deformation" on a graph?

 - Random graph models
  - Latent-position models (W-random models, kernel random model):
    - adjacency matrid drawn from a bernoulli distribution parameterized by a kernel.
    - parameter: sparsity level $\alpha$ - you can obtain dense or sparse graphs.
  - Erdos-Renyi
  - Stochastic Block Models
  - Gaussian Kernel

 - Spectral vs Continuous Graph Neural Networks - instead of propagating a signal over the nodes,
   propagate a function over the latent space.
   - Deviation between discrete and continuous GNN is bounded

 - Deviation of cGNN is bounded by the jacobian for a translation-invariant graph generation kernel.

## Fourier features let networks learn high-frequency functions in low-dimensional domains

https://arxiv.org/abs/2006.10739

Context: MLP can represent 3D objects or scenes.

 - Train an MLP to take an input co-ordinate and output an RGB pixel
 - instead of just inputting the low-dimensional co-ordinate, pass them
   through a fourier feature mapping. Control the frequencies that
   you can represent in practice. With this technique you can
   learn the high frequency details.

Context: kernel regression: - nonparametric function estimation

 - High level: Add up a set of kernel functions, one centered each input data
   point each with its own weight. Gaussian blob
 - Adding them up produces the continuous estimate function.
 - Its important to pick the right kernel width. If you're too wide
   you underfit, if you're too skinny you overfit.

Context: Training kernel regression is like kernel regression:

 - The behaviour of networks under training under certain limits
 - Training a sufficiently wide NN is basically like fitting a kernel
 - Fourier feature mapping gives you many widths

How does fourier mapping work:
 - Pass the co-ordinates through many sin and cosines at different
   frequencies to get its position in different frequencies.
 - Stack them in the channel dimension.
 - If you change the standard deviation of your random matrix
   that generates your kernel
