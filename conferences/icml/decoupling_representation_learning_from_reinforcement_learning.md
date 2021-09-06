# Decoupling Representation Learning from Reinforcement Learning

In an effort to overcome limitations of reward-driven feature learning in deep reinforcement learning (RL) from images, we propose decoupling representation learning from policy learning. To this end, we introduce a new unsupervised learning (UL) task, called *Augmented Temporal Contrast (ATC),* which trains a convolutional encoder to *associate pairs of observations separated by a short time difference, under image augmentations and using a contrastive loss.* In online RL experiments, we show that *training the encoder exclusively using ATC matches or outperforms end-to-end RL in most environments.* Additionally, we benchmark several leading UL algorithms by pre-training encoders on expert demonstrations and using them, with weights frozen, in RL agents; we find that agents using ATC-trained encoders outperform all others. We also train multi-task encoders on data from multiple environments and show generalization to different downstream RL tasks. Finally, we ablate components of ATC, and introduce a new data augmentation to enable replay of (compressed) latent images from pre-trained encoders when RL requires augmentation. Our experiments span visually diverse RL benchmarks in DeepMind Control, DeepMind Lab, and Atari, and our complete code is available at https://github.com/astooke/rlpyt/tree/master/rlpyt/ul.

https://icml.cc/virtual/2021/spotlight/10142

[[stooke_decoupling_representation_learning_from_rl.pdf]]

## Motivation
Typically we learn the visual representation E2E with the policy. This can be a disadvantage:

1. Often a bottleneck (several years of aux tasks)
2. Requires task-specific training

Self-supervised method are powerful enough to learn visual representation without theu se ofrewards.

## Augmented temporal contrast
![[augmented_temporal_contrast.png]]

Basically take an anchor image and a positive image. Augment them.

Momentum encoder: $\bar \theta \rightarrow (1-  \tau)\bar \theta + \tau \theta$

Logis: $l_{i, j+} = p_i W \bar c_{j+}$

This forms logits which go into the noise contrastive loss function:

$$
\mathbf{L}^{\text{ATC}} = -\mathbb{E}_{\mathbf{O}} [\log \frac{\exp l_{i, i+}}{\sum_{o_j \in \mathbf{O}} \exp l_{i, j+}}]
$$

(reminder: InfoNCE loss wants a large log-ratio between a logit and all other logits. In this case it means that the logits for two known samples should be small compared to the sum of distances between that sample and other samples that are supposed to be "unrelated").

We require the network to associate the anchor image with the correct positive image compared to all the negative examples.

## How well does this work compared to training end-to-end?

In ATC reward training we don't backprop into the CNN layers. Representation learning is decoupled from the task rewards. Blue curves are equal to or better than end-to-end RL and better in the sparse reward case.

## New capabilities

Mutli-task vision encoders - single convolution encoder trained on 4 tasks, frozen, then succeeds in four new tasks/domains.

