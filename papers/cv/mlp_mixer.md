---
title: MLP-Mixer - An all-MLP Architecture for Vision.
venue: CoRR
volume: abs/2105.01601
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2105-01601
ee: https://arxiv.org/abs/2105.01601
url: https://dblp.org/rec/journals/corr/abs-2105-01601
authors: ["Ilya O. Tolstikhin", "Neil Houlsby", "Alexander Kolesnikov 0003", "Lucas Beyer", "Xiaohua Zhai", "Thomas Unterthiner", "Jessica Yung", "Andreas Steiner", "Daniel Keysers", "Jakob Uszkoreit", "Mario Lucic", "Alexey Dosovitskiy"]
sync_version: 0
---

# MLP Mixer: An all-MLP architecture for Vision

While convolutions and attention are suffient for good performance, neither are necessary.

MLP-Mixer: Based exclusively on MLPs. Apply the MLPs to image patches (mixing the per-location features) and then apply the MLPS across patches (mixing spatial information).

![[mlp_mixer_architecture.png]]

Basically, flatten into patches, indepdently process with MLPs (so process each patche's channels), transpose back into channels of W x H, do layer norm, and do MLPs there with a skip connection.

So the first MLP mixes across channels, the second MLP mixes between channels and across spatial units.

The architecture is equivalent to a CNN which uses 1x1 convolution for channel mixing and a single dpeth-wise convolutions of a full receptive field and parameter sharing for token mixing.

Typically CNNs mix features at a given spatial location and between different spatial locations both at the same time. Mixer separates these two steps.

Parameter sharing: The same channel-mixing MLP is applied to every column of X, which ameks sense since you want positional invariance. However, you don't want channel invariance, so processing spatial information between channels independently does *NOT* involve parameter sharing.

The complexity of the network is linear in the number of image patches.

Utilizes skip-connections and layer-norm, but no position embeddings since the token-mixing MLPs are sensitive to the order of the input tokens already.

## Experiments

The point is not to show a SOTA but rather just to show that an all-MLP architecture is competitive and patches may be all that you need.

They test quite a range of different configurations, different depths, patch sizes etc. Patch sizes go from 14, 16 and 32.  Smaller patches means bigger sequence length.

### How to do fine-tuning?

If you want to fine-tune on higher resolutions, you need some way of adjusting the number of weights since the patch size does not change.

To do this, multiply the input by a weight matrix $W_1 \in R^{D_S \times S}$. This has to be adjusted by when changing the input dimension.

Assume that the image resolution increases by a factor $K$. So then the token sequence increases by $K^2$. How do you initialize the parameters? Split the input spequence into $K^2$ equal parts.

Replace $W_1 \in R^{D_S \times S}$ with a larger matrix $W'_1 \in R^{(K^2D_S) \times (K^2D_S)}$. Initialize $W'_1$ with a block-diagonal matrix with copies of $W_1$ on its main diagonal.

## Results

When the size of the upstream dataset increases, Mixer's performance improves significantly. Also runs 2.5 times faster than ViTH/14 and twice as fast as BiT.

 (but this seems in contradiction with the other paper that claimed ViT was was faster than BiT. Anyway).

 ## Invariance to input permtuations

  - Shuffling the order
	  - Invariant to order of patches
  - Permutting pixels within a patch
	  - Invariant to order of pixels within a patch.


But note that this is when you train from scratch and keep the same permutation. So it makes sense that if you scramble an image to garbage and feed it to ResNet that it will not perform well.