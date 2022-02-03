# Provable guarantees for self-supervised deep learning with Spectral Contrastive Loss

https://neurips.cc/virtual/2021/oral/28346

 Our work analyzes contrastive learning without assuming conditional independence of positive pairs using a novel concept of the augmentation graph on data. Edges in this graph connect augmentations of the same data, and ground-truth classes naturally form connected sub-graphs. We propose a loss that performs spectral decomposition on the population augmentation graph and can be succinctly written as a contrastive learning objective on neural net representations. Minimizing this objective leads to features with provable accuracy guarantees under linear probe evaluation. By standard generalization bounds, these accuracy guarantees also hold when minimizing the training contrastive loss.
 
 - Learning representations from large unlabelled dataset - especially in computer vsiion
	 - Pull embeddings of augmentations of the same image closer
	 - Push embeddings of views of different images far apart
 - Put a linear classifier on top, you get pretty good downstream performance



Theoretical justifications?
 - Assume positive pairs are independent conditioned on the true label or hidden variable
 - Assumption not realistic because only when conditioned on the image


Information theoretic analysis:
 - Do not show wy the representaitons can be used in a linear way


This work proves that contrastive learning learns a linearly separable space.


Motivation:
 - Clustering population data in augmentation graph
 - Nodes: all augmented image. Edge between two nodes that are from the same image but are augmented.
 - Same augmented image can come from the two different natural images if they are already close.
 - Two augmented images are connected in the graph if they are augmentations from the same image. So it is not just a bunch of stars, each augmented image is also connected to augmentations of the same image.
 - Each connected manifold is one class
 - Intuitions:
	 - Very few edges between different lasses, almost disconnected!
	 - x is an augmentation of a dog
	 - x' is an augmentation of a cat
	 - unliely that both x and x' are augmentations of the same image $\bar x$.
	 - Two augmented dog images connected via a sequence of interpolating dog images. So basically we can't go directly from an augmented image of a dog to an original of another dog, but we can traverse an interpolation that eventually gets you there.
	 - Augmentations from the same class are connected to each other via interpolating data.
 - To recover the class structure we just need to find a nice partition of the graph


Community detection via eigendecomposition.

Throwing away small eigenvectors will do that.

Spectral clustering.

this algorithm returns a partiton that approximates a partition with some good theoretical guarantees.

## Contrastive learning as contrastive learning

The learned representation should be equivalent to the eigenvectors of the adjacency matrix.

Design a poluation loss function:

$$
\min_F L(F) = ||(I - L) - FF^T||^2_F = \sum_{i, j} (\frac{w_{x_i, x_j}}{\sqrt{w_{x_i}} \sqrt{w_{x_j}}} - f_{\theta}(x_i)^Tf_{\theta}(x_j))^2
$$

Minimizing $F$ contains eigenvectors of $L$ as columns.

Rewrite the loss by expanding the square:

$$
c - 2 \sum_{ij} (\frac{w_{x_i, x_j}}{\sqrt{w_{x_i}} \sqrt{w_{x_j}}} f_{\theta}(x_i)^Tf_{\theta}(x_j) + \sum_{ij} (f_{\theta}(x_i)^Tf_{\theta}(x_j))^2
$$

The firsrt term is positive pairs, the second term is for negative pairs.

Ignore the scaling term $\sqrt{w_x}$ and constant which doesnt affect the linear probes:

$$
- 2 \sum_{ij} (f_{\theta}(x_i)^Tf_{\theta}(x_j) + \sum_{ij} (f_{\theta}(x_i)^Tf_{\theta}(x_j))^2
$$

where $i$ is the negative and $j$ is the positive.

## Theoretical Guarantees
Labels can be recovered from the augmentations with error $\alpha$

Augmentations from the same class are connected to each other.

Conductance: total edges out of S divided by total edges connecting to $S$. When conductance is small, the set $S$ has a small set of connections to the rest of the graph.

If a representation function has $2k$ dimensions, there exists a linear classifier such that you get error at most $\bar O(\alpha/ \rho^2_k)$. If $\rho^2_k$ is large, you will do well.