# Mining and Learning with Graphs at Scale

Pre-computing the nearest neighbours is important.

Similarity graphs: edge relationship is based on some measure of similarity/disatnce.

Graphs - computation on abstract concepts, computation on different data types. Multi-modal
datasets.


Applications of graph neural networks:
 - Label propagation - start from some known bad actors, look at nearby negihbours,
   use graph structure to identify nearby neighborus that may also be suspicious.
 - Anomaly detection via density clustering: things that are statistically unlikely.

Improving other ML models: relational discovery. Related images.

Feature instruction: generated graph signals are usefl as training signals for ML models.

Resource efficiency: communication overhead.


## Modelling COVID with GNNs

Intuition - depends on time and space.
 - number of cases that you have tomorrow depends on what you had yesterday
   and also what your neighbours had - also based on air lines.

 - mobility data: has very rich mobility data through GPS analysis.

 - each node represents a time at a place
   - 150 slices, each slice represents a day
   - between slices, temporal edges, inversely weighted by time

Prediction of next day cahnge was much bettter than other methods. The information
helps.

## Graph Mining and Privacy

FLoC - FLoC aims to replace third party cookie with shared cookie.

Cluster must represent some minimum size constraint.

Affinity hierarhical graph clustering algorithm - cosine similarity
measure.

Can you do a recommendation system?

 - There is a public graph $G$ and in addition every node has access
   to a local grpah $G_u$.

 - Solve some specific machine learning problems like clustering
   - don't share private data to the recommender system
   - this is possible for a variety of problems.
   - send sketches of the public data to the individual uses (personalized).
   - users exchnage between their private contacts their own private sketches.
   - cloud will not be aware of the contacts.

## Causality

 - How clustering can be applied to Causal inference.

 - Branch of statistics that looks at establishing cause and effect.
 - Randomized trials, assigns units of interest to a treatment or control condition.

Clustering comes into it if the randomized trial suffers from interference - eg, if
treating one unit can affect some other unit.

Assign treated and control units based on the cluster that you're in.

Vaccination trial: vaccination status of one unit can affect the response of other neighbours.
In some cases vaccination trials have looked vaccinating whole households rather than individuals.

In some cases the social network is not explicit. Need to do a balanced partition.


## Grale - Learning Graphs

toy example - partially labelled set of nodes and a graph indicating some similarity. Spread
information from the labelled nodes to the unlabelled nodes.

In the real world, we usually have many different relationships that we could pick from. How
do we actually build the graph?

If we make a bad choice, we would make bad predictions.

Given a multi-modal feature sapce $X$ each with a distance measure $k$.
 - A partial labelling on this feature sapce
 - A learning algoprithm which is a function of some grpah $G$ having vertex
   set equal to $X$.

How do we select the right graph?

 - Label propagation
 - Assume that the nodes have a bunch of features associated with them.
 - Learn some sort of edge-weighting that is a function of all the different
   relationships.
 - Weight edges based on decisions of a classifier that decides whether or not
   two nodes are the same.


Grale:
 - Step 1: generate candidate pairs via LSH
 - Step 2: within each bucket, train a pairwise model to predict same-class membership
   or apply model to infer similarity on pairs.


If points are close in the feature space they're likely to have similar representaitons.


Model Structure:

 - In practice use one of two different models
 - One is a neural network, or use a tree model.
 - Neural network: embed each of the nodes, combine via hadamard product

Grale for Youtube:

 - Use it to detect malicious actors
 - Separate abuse from nona-buse

 - by Aadding Grale to the system we increase recall by 90%.

## Similarity Ranking on Graphs

Given a graph, how do we understand similarities based exclusuvely on the structure in hte grpah.


 - Single hop:
   - Common neighbours
   - Jaccard coefficient
   - Weight nodes in terms of log degree

 - Multi-hop:
   - Katz score
   - Personalized PageRank (PPR)

Given a node v and a probability, unique stationary distribution that
assigns a score to all nodes in the graph.

 - PPR can be used on very large graphs
 - Efficient GNNs
 - Efficient graph embeddings
 - Graph ranking
 - Suggestions in social networks

Ranking:

 - On one side, users, other side items
 - How do you define a similarity score that takes into account different types of items.


 - Problematic cases: Ego node part of many communities.
    - Two well separated communities
    - Should we recommend B to node A if they're in separate communities.
    - Should cluster the ego-networks.
    - Common neighbours will say that these two nodes are related.
    - Experiment: 1.4% decrease in number of rejected suggestions.


Hierarchical Clustering
 - Seeks to build a hierarhcy of clusters.

Many sequential algorithms.

Affinity hierarchical clustering:
  - Keep heaviest edge above a threhsold incident to each node. Each
    node is trying to connect to the heaviest edge.
  - Form clusters by the heavy edge connections.
  - Iterate and recluster.
  - Compute graphs between clusters.


Balanced Partioning
 - Try to partition the grah into $k$ pieces and minimize the cut.
 - Best approximations are based on linear programming, does not escale.

Outline of Algorithm:
 - Initial ordering (1D embedding)
 - Space-filling curves, hierarchical clustering (affinity hierarchical clustering).
   - Use the order of leaves in the tree to get the initial ordering.
 - Semi-local moves: min-linear arrangement, optimize by random swaps.
 - Introduce imbalance:
   - dynamic programming
   - linear boundary adjustment
   - min-cut boundary optimization

 - You can get a fully balanced solution

Randomized composable core-sets:
 - divide the graph into pieces, compute the solution on coresets, then combine into a solution.
 - Distributed metric clsutering: Divide the data into pieces, solve clsutering on each piece
 - This gives us a good set of centers for things like k-medians.


Coverage maximization:
 - Find k-nodes to cover the maximum number of neighbours
 - Basically set cover but hyarder.

Given a family of subsets, choose $k$ subsets.
 - Sketching + CoreSets 
 - Generate random numbers f or items
 - Keep O(n) edges with minimum hash value but no more than O(n/k) per items.


Dynamic Distributed Clustering:

 - Online Hierarchical Agglomerative Clustering
   - When a new pointa rrives, run a split-merge procedure
   - Eg, break the hierarchy into a forest, run HAC on the forest.


## Community Detection

 - Find communities in a social network.
 - Cluster nodes into densely connected sets.
 - Ideally we should detect the number of clusters, specify the desired cluster density.


Modularity:
 - Similar to what was covered in complex networks.
 - start with each node in its own cluster, then improve things
 - Little theoretical guarantees.

Conductance:
 - Number of edges leaving C over total degrees of nodes in C.

Normalized Cut:
 - Sum of cluster conductances.

Coconductance:
 - Takes a $p > 0$ parameter - coconductance of clsutering is sum_C (1 - conductance(C))^p
 - When $p$ is zero, the optimal soluition is maximum matching
 - When $p$ is inf, optimal soliution is connected components.


 - Theoretical algorithm: constant factor approximation of the optimal soliution in linear time.
 - Nice empirical performance.

## Label Propagation with limited data

SSL - to label the unlabelled instances use the context
 - use similarity relationships between points.
 - SSL using Gaussian Fields and Harmonic Functions (2003)
 - Propagate labels along graph edges.

Instead of using matrix calculations, approximate it.

Eg, MNIST. Some are labelled 4s, some are 9s.
 - Define edges by similarity score.

Spread the labels from the seeds outwards along the edges

 - But if you keep propagating, some nodes end up with labels for each tyope

 - By holding out some of the labels, we can run label propagating and measure how
   well the learned labels match the ground truth.

Label propagation can be used for a downstream task. Pick nodes where we have the most confidence.

Applications to text and video classification. Can be used to clean noisy labels - eg, guesses
for the labels.

System Properties:
 - Nodes and edges can be different types, just must be that similar nodes connected by an edge have similar labels.
 - Binary multi-class and multi-label problems.
 - You don't have to keep all labels at each node, keep the top $k$ labels. Useful when you have a
   large label set.

Loss Function:
 - Label loss (eg, nodes that have a ground truth, compute loss)
 - Neighbour loss: agree with your neighbours
 - Prior loss: If you have some prior label, eg, uniform distribution, or
   if certain labels are more likely than others.

Learned label update funciton: train a model to exploit node features.

 - Do a short label propagation run to get neighbouring labels.
 - Compare when we're trying that model we use the seed label as the target label to train against.

"Semi-Supervised Learning with graphs".


# Graph Neural Networks

## Graph Embeddings

Primitive - high-dimensional float vector representation of information,
generated by the inner layer of a deep neural network.

The information is the same but the representaiton is different.

A graph embedding is just a representation of a graph that preserves the
properties of the graph.

Initial work: random walks, DeepWalk. Generate a skip-gram and then model that.
Latent representations you learn are the embeddings that you use.

Extensions for:
 - Directed grpahs
 - Hierarchical Structure (HARP): Hierarhical Representation learning for Networks
 - Graph Attention Mdoels: "Learning nodee embeddings via graph attention."

Graphs as a modality:
 - one of the power of graph embeddings is that you're able to encode them and mix
   the relational representations with another model to add a graph component to it.

## Graph Convolutions

Inspired by convolutional networks - incorporate context. Nontrivial to do scaleably.
In graphs you can have an arbitrary number of edges. You have to handle an arbitrarily large number
of nearby neighbours.

Adjacency Matrix:
 - Every node has a row and column corresponding to it.
 - Graph convolution looks at the immediate neighbours
 - n-hop neighbourhoods
 - Learn a new vector for the seed node until you've projected into a new space.
 - Pooling

GCN: Uses the frequency domain of a graph to do "convolutions".
 - Requires normalization.

Message Passing Neural Networks:
 - Naturally incorporate heterogeneous nodes.
 - Generalize the idea of a GCN to use arbitrary control of how messages are passed.
 - Learn how a message can be generated.
 - Read out the final state as a "read out".

Common elements in graph models: "Machine Learning on Graphs: A model and comprehensive taxonomy"

Challenges of Graph Neural Networks:
 - (1) Representation Complexity: Multiple aggregation process creates
       a weakness, adding extra layers after the second doesn't improve the
       classification performance.
       - Happens because local neighbour features are much more important
       - Over-averaging reduces locality
       - Over-smoothing
       - Eg, prediction task, you can only really learn your opposite labels.

       N-GCN: Mixture of experts: Feed several GCNs increasingly dense grap[hs.
       MixHop: Expanding contextual horizons: As the graph has less and less correlation,
               improve performance substantiually over the baseline.

 - (2) Speed
 - (3) Baises
 - (4) Complex Interactions


## Scaling GNNs

Scaling Graph Neural Networks with Approximate PageRank

Adjacency matrix is NxN

Most popular approach: Sample pathces of the graph. This approximation doesn't impact
accuracy all that much.,

Recursive message passing: - relies on recursive message passing.

Assumption: All neighbouring nodes are useful for the final computation. GCN picks up 
the most important nodes by defaults.

### PPRGo

 - Calculating aggregations at riuntime is slow
 - But there might be mechanisms to separate the aggregation beforehand.

 - Weight nodes by their importance
 - There should be a dial that allows you to grab the top n nodes.

Personalized PageRank:
 - For every node calculate stationary distribution of random walk. Nodes that
   appear frequently are weighted higher. "Infinite hop attention vector".
 - ACL's algorithm.
 - Power iteration. We only need PPR vector once, makes sense to fall back to this,
   but we only need a few iterations to get a reasonably effective PPR vector.


(1) Calculate PPR vectrors offline
(2) Train an MLP model that ingests the node features
(3) Aggregate those logits using attention wieghts of PPR vector
(4) Inference: Use power iteration to approximate the PPR vector
(5) Feed approximated PPR with node features to produce final prediction.

PPRGo aggregates the most important nodes in the N hop neighbourhood using only 1 hop of computation.

Tradeoff between accuracy and scaleability:
 - PPRGo shows comparable accuracy.
 - Reddit: PPRGo is the only method that still stays fast.
 - MAG: Scholar Citation Dataset - 12M nodes and 173M edges.

Conclusions:
 - GCNs use a scattershot method.
 - Doing multiple hops is slow.
 - PPRGo gives the benefit of large neighbourhood learning with the speed of a single hope GCN

"Scaling Graph Neural Networks with Approximate Pagernak".

## Debiasing GNNs

Learn node embeddings that are invariatnt to sensitive metadata
 - eg, gender/age/income

Approch (1): Adversarial debiasing. Predict the sensitive metadata, backprop inverse loss

Approach (2): Make random walks conditionally independent of metadata

Approach (3): Learn embedding of metadata itself, project graph embeddings to be orthogonal to metadata. (MONET)

 - Learn a transformation of the raw metadata and concatenate it with the graph embedding
 - if we can encode the metadata in the concatenated representation space, then debias the topology space
   by just removing it
 - Meta-Data leakage - metadata is still captured by topology embeddings.

 - Orthogonalize the topology embeddings away from the metadata. Project the topology embeddings into
   the null space which results in exact linear debiasing.
 - Input: topology embedding, metadata embedding
     - $P_z = I - Q_z Q_z^T$
     - forward pass: Compute Z left-singular vectors $Q_z$ and projection $Q_zQ_z^T$
                     Compute orthogonal topology embedding $W^{\orth} = P_z W$
                     return debiased graph representation $W_^{\orth}, Z$


 - After applying, completely debiased.
 - Only solves linear debiasing.

## Learning Multiple Embeddings

A node have multiple meanings or senses, just like words.

Why is this important?
 - Random walks will cross the community boundaries very often.
 - Each node has many roles and belongs to many communities that the random walk will explore partially.
 - A random walk starting from a node will cross boundaries of communities easily
 - Look at the node-centric structure of the graph: ego networks. We can disentangle these communities.

Ego-network:
 - For each node like the center node, the ego network is defined as the neighbours of the node
   and all the connections between them.
 - when communities overlap, usually there is a single context in which two neighbours interact.

Persona Grpah:
 - Based on the ego-net
 - Process one graph into another where the communities are separated
 - once we identify that a node is part of two communities, duplicate the node and
   connect each node to each separate community, disconnect the communities through
   that node.

Splitter framework:
 - Create ego-net of each node
 - Partition each ego-net with any non-overlapping clustering algorithm, 
 - Create the persona graph
 - analyze the persona graph
 - Map the results of the persona graph to the original graph

Where does this get you to multiple embeddings? 
 - If a node is part of more than one community, it gets multiple embeddings
   as part of a learned embedding within its community
 - Reguarlize by original embedding - don't stray too far.

 - Improves over previous results for things like link prediction.
 - Use simple max-aggregation of dot products for similarity.
