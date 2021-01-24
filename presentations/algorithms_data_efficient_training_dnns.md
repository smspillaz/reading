# Algorithms for Efficient Training of Deep Neural Networks

Why has there been a resurgence?

 - Better training algorithms (pre-training, batch norm, dropout, resnets, transformers)
 - Flexibility in architecture
 - Capacity

Huge capacity requires lots of labelled data! Gathering labelled data is time consuming
and costly.

Design data-efficient methods for training deep neural networks.

Many paradigms:

 - Fully supervised learning
 - SSL
 - Unsupervised
 - Transfer
 - Multi-task
 - Active learning
 - Few-short

Contributions:

 - Fully supervised learning with explicit constraints 
 - SSL
 - Unsupervised learning (mixup resynthesis)
 - InfoGrpah

## Manifold Mixup

 - Better features by interpolating hidden states (ICML 2019)
 - Learn a decision boundary - needs to be smooth, not close to the samples,
   too confident on the samples.
 - Apply some constraints on the hidden states. Should concentrate hidden states from low volume.

 - Take two images, extract certain hidden states, mix them, forward propagate, get a mixed label
   compute the loss. Results in better accuracy. Can help against weak adversarial attacks.
 - Helps a lot of hte test samples have novel composition of semantic concepts.

## On aversarial mixup resynthesis

 - Fool the discriminator

## Interpolation consistency training for SSL

 - Hard to do a linear decision boundary
 - Want the decision boundary to fall into the low density region

 - Consistency regularization:
   - Interpolation consistency - perturbation in the direction of other random samples

 - Follow-up: MixMatch, ReMixMatch

## InfoGraph

 - Unsupervised and semi-supervised graph-level representation learning via mutual information maximization
 - Learn the features in an unsupervised way
   - Pass graphs A and B through a graph encoder network
   - Readout function: Graph-level featues. Maximize mutual information between graph-level and node-level features.
   - One network trained with labelled samples and one network trained with unlabelled samples
   - Maximize mutual information of representations for nodes with similar features.



