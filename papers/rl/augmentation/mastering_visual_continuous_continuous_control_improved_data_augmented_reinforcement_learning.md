---
title: "Mastering Visual Continuous Control - Improved Data-Augmented Reinforcement Learning."
venue: "CoRR"
volume: "abs/2107.09645"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2107-09645"
ee: "https://arxiv.org/abs/2107.09645"
url: "https://dblp.org/rec/journals/corr/abs-2107-09645"
authors: ["Denis Yarats", "Rob Fergus", "Alessandro Lazaric", "Lerrel Pinto"]
sync_version: 3
cite_key: "journals/corr/abs-2107-09645/Yarats/2021"
tags: ["DeepMind"]
---
DrQ-v2: Solve Humanoid Walk from Images.

Off-policy actor-critic approach the learns directly from pixels.

Multiple improvements over DrQ resulting SOTA on DMCS.

Conceptually very simple and easy to implement.

SAC-AE: Stack observations, conv encoder to get some features which we feed into the policy network. Then we have a reconstruction task.

DrQ: Data-regularized Q

 - Image Augmentation is all you need (ICLR2021)
- Key Idea: iamge encoders are crucial but they are overfitted. If we do image augmentation we use the capacity much better.
- Pad each image and random crop, generate N image samples and compute both the Q function target and Q function estimate using the averages.
- No reconstruction or world model loss needed. We can even ditch the decoder.

Change base LR algorithm from SAC to DDPG.

![[drq_v2.png]]