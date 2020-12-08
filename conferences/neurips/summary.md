# Mining and Learning Graphs at Scale

## Label Propagation

 - Can be cast as a semi-supervised learning problem
 - Some nodes have labels, other nodes do not have labels
 - Induce a network by some learning some unsupervised distance function (contrastive loss, etc)
 - Propagate labels from labelled examples to unlabelled examples
   weighted by the edge weights.

## Personalized PageRank (PPR)

 - PageRank: Stationary distribution of visit probability by a random surfer
 - Personalized PageRank: "Egocentric" PageRank - per node stationary distribution
   - Can be leveraged for things like community detection
 - Ego centric label propagation: Use PPR vector like a kind of attention. Which nodes
   are actually important for a given node.
 - Learn multiple embeddings: A node can be part of many communities. Use Personalized PageRank
   to partition the graph, create copies of the node (personas) for each community that
   it is in, learn embeddings for each node in the context of each community.

# Equivariant Networks

## Symmetries

 - In many domains there are equivariances and symmetries, eg,
   if you transform the input space in some way, it may look
   the same in some representations but not others.
 - Eg, if I rotate an equilateral triangle 2pi/3 times - it
   is still the same triangle, even if the co-ordinates have shifted.
 - Knowledge about symmetries can help with learning, map things
   that look different but are actually the same to the same representation
 - Being invariant to symmetry-preserving transformations is often not
   enough. Piccasso problem example - the distances between parts matter, for instance.
 - Data Augmentation is not enough to preserve equivariance. Equivariance puts
   the constraint on transformations everywhere. Data Augmentation puts it
   only on the network outputs within a specific domain.


## Steerable CNNs
 - Take each filter, rotate it 4 times, now you have 4 different filters
   all detecting the same thing, but on rotated versions of the images
   (to clarify, not learning 4 different sets of weights - you share parameters
    for all 4 rotations, but each filter gets to see the image in all rotations)
 - On the next layer, you have activations - one of those filters in
   the relevant channel will get the right activations
 - Now you have a problem where depending on the rotation of the image,
   the activations will be in a different channel - need to shuffle the channels to
   compensate.
 - With a standard CNN, not rotation invariant, backrotating the image will show
   unstable activations depending on the rotation of the image.


# Uncertainty Estimation

## Uncertianty estimation models

 - Models often assign high uncertainty to OOD inputs
   - Example: Two moons - introduce a third class - what happens?
     - We're uncertain only around the decision boundary, but not outside
       of it - we classify the third unseen class as the first class
 - Types of uncertainty:
   - Type 1: Epistemic - which model best describest this phenomena - many possible models
   - Type 2: Aleatoric - noise in the data, noise in the label set

 - Measure uncertainty by calibration error (|predicted uncertainty - accuracy|)
   - Being wrong here means that you were either underconfident or overconfident

## Robustness

 - Bayesian Neural Networks - distribution over the parameters.
 - Ensemble learning - effective in practice for uncertainty estimates
   - In practice often works better than bootstrap method
   - Ensemble of different random seeds, different hyperparameters, etc
 - Tricks to make a normal model more robust:
   - Recalibration: fit temperature parameter to adjust confidence on a validation set
   - Monte-Carlo Dropout
   - Deep Ensembles: Re-run SGD but with different random seeds
   - SWAG + Laplace: Fit a simple distribution to the mode centered around the SGD solution

 - Some recent advances
   - BatchEnsemble:
     - Having an ensemble of models is expensive, duplicating the model N times
     - Start with the idea that in an ensemble, for each weight matrix $W$, we have
       some ofther matrix $F_i$ for the $i$th ensemble
     - Express $F_i$ as $q_is_i^t$ - outer product of two vectors
     - Now you just need to learn the two vectors as opposed to entire matrices
     - Intuition - have one model, but *modulate it*. Simialr to FiLM


## Prior Selection for Bayesian Neural Networks

 - Standard normal distribution prior $N(0, 1)$ is often the default, but this may not be the best choice
   - Has bad statistical properties: does not leverage information about the network structure
     including inherent self-correlations, assumes that all hidden units contribute infinitisemally to each input
   - Had bad optimization properties: sensitive to parameterization, too strong a regularizer
 - Think about the whole input/output relationship

## Data Augmentation

 - Data Augmentation can improve calibration error quite a lot
 - Critically, a mix of augmentations is important here
 - ImageNet-C test set to test your model on OOD data.

## Distance Awareness
 - As you train on a manifold, you want your uncertainty to go up as you move away from that manifold
 - Spectral Normalized Neural Gaussian Processes
   - Replace Output layer with Gaussian Process layer
   - Apply spectral normalization to preserve distances within each layer
   - GPs allow you to capture similarity. Uncertainty is correlated to distance
     from the rest of the training examples.

