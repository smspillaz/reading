---
title: Patches are all you need?
---

# Patches are all you need?

Is the performance of ViTs due to the transformer or due to the patches? We only used patches because of quadratic runtime of self-attention.

Paper proposes ConvMixer.

Similar to ViT and the even-more-basic MLP mixer. Maintain equal size and resolution throughout the network.

ConvMixer only uses convolutions to achieve the mixing steps.

Uses a tensor-layout patch embedding to preserve locality and then applies $d$ copies of fully-convolutional block consisting of a "large kernel" depthwise convolution.

Eg, conv2d wher ethe kernel size is the patch size, the stride is the patch size, and you go $d \to d$, with groups = $d$ on the first step (spatial mixing) and groups = 1 on the second step with a 1x1 conv (channel mixing).

Its equivalent to the MLP-mixer in a sense - the activations are shared. 