---
title: Learning from Demonstration with Weakly Supervised Disentanglement.
venue: ICLR
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/iclr/HristovR21
ee: https://openreview.net/forum?id=Ldau9eHU-qO
url: https://dblp.org/rec/conf/iclr/HristovR21
authors: ["Yordan Hristov", "Subramanian Ramamoorthy"]
sync_version: 3
cite_key: conf/iclr/HristovR21
---
# Learning from Demonstration with Weakly Supervised Disentanglement

https://iclr.cc/virtual/2021/poster/3178

We treat the task of interpretable learning from demonstration as an optimisation problem over a probabilistic generative model.

 We show that such alignment is best achieved through the use of labels from the end user, in an appropriately restricted vocabulary, in contrast to the conventional approach of the designer picking a prior over the latent variables.


 How can we bridge high-level notions to low-level perceptive that controls use.

 We aim to model the distribution of robot arm trajectories.

 Use a conditional latent variable model to represent the distribution of demonstrated trajectories $x$ and discrete user labels $y$ given an image $i$.

 The latent variables $c$ represent the abstract spatial, forceful and speed notions of "where" and "how

 Each demonstration associated with discrete weak labels.

 Start with an RGB image and a time-series trajectory.

 Compress all modalities to a common bottleneck layer.

 Do temporal convolutions to reconstruct the sequence.

 A portion of the latent variables is unaligned but is used for reconstruction.

Because we use weak supervision to disentangle the latents - you can sample trajectories consistent with the meaning of the latent.

Sample trajectories are consistent with the meaning with the latent.