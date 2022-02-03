---
title: An Image is Worth 16x16 Words - Transformers for Image Recognition at Scale.
venue: ICLR
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/iclr/DosovitskiyB0WZ21
ee: https://openreview.net/forum?id=YicbFdNTTy
url: https://dblp.org/rec/conf/iclr/DosovitskiyB0WZ21
authors: ["Alexey Dosovitskiy", "Lucas Beyer", "Alexander Kolesnikov", "Dirk Weissenborn", "Xiaohua Zhai", "Thomas Unterthiner", "Mostafa Dehghani", "Matthias Minderer", "Georg Heigold", "Sylvain Gelly", "Jakob Uszkoreit", "Neil Houlsby"]
sync_version: 3
cite_key: conf/iclr/DosovitskiyB0WZ21
---

# An image is worth 16x16 Words: Transformers for Image Recognition at Scale

https://iclr.cc/virtual/2021/poster/3013


 => In vision, attention is either applied in conjunction with convolutional networks, or used to replace certain components of convolutional networks while keeping their overall structure in place.
 => We show that this reliance on CNNs is not necessary and a pure transformer applied directly to sequences of image patches can perform very well on image classification tasks

Typically attention applied in conjunction with convnets. But this reliance on CNNs is not really necessary and a pure transformer applied directly to image patches can do well.

 Can we make use of the pure transformer network for images?

The main problem with all-attentional models so far is that they use specialized attention patterns and therefore don't scale up well to modern hardware accelerators.

How to apply the transformer to images?
 - Split an image into patches and provide a sequence of linear embeddings of those patches as inputs to a transformer.
 - Does slightly worse than ResNet, but that's mainly because Transformers lack some of the inductive biases of ResNets such as translation equivaraince.
 - But we do better if we're training on larger datasets, so large scale training trumps inductive bas.


 Transfer learning benefits from scale. When you increase the size of the pre-training data, performance improves a little it. Increasing the model size also helps.

 In this paper, explore the use of a pure transformer for vision, ViT, focussing on transfer learning usecase. Study as well the scaling properties, what does the model learn.

 ## Vision transformer

 Split image into patches.

 Linear projection of flattened patches. The order is lost, so we add some positional embeddings.

 Then feed it into an encoder with a dummy token that can attend to everything else. Attach the classification head to the representation for the dummy.

 Base model: 12 layers, hidden size 768, MLP size 3072, 12 heads, 86M params.

 - 2x2 patches, reshaped into 2x2xC, projected into D dimensions.
 - Full self-attention.
 - Prepend a learnable embedding to the sequence of embedded patches.
 - Learnable 1D position embeddings. 2D position embeddings don't seem to help much.

 Also experiment with a hybrid CNN, instead of passing patches, pass the linearized feature maps.

 Scaling the transformer architecture is enough to make the CNN features unnecessary.

 ViT-Huge beats SOTA while being 4x cheaper to pre-train.

 ViT-Large/16 is 14x cheaper to train and matches CNN SOTA.

 ViT speed scales mostly linearly in number of patches =.

 ### Position Embeddings

 Visualize the cosine similarity of learned position embeddings. Different small images use different query patches. Deviates from locality in interesting ways.


 ### Receptive Field Size

 For each attention head, plot the average distance between query patch and the patch it attends to.

 Finding: Early layers, some attention heads are local, some are globals, then later on attention becomes much more global. Idea of "building up local features".


## Can attention replace convolutions?

Yes.

Think about what convolutions are doing. Its the dot product of the filter weights along the local neighbourhood. Transformers with a local attention pattern are equivalent.

Scaling is a problem:
 - Sparse transformers
 - Apply it in different sized blocks
 - Apply it along individual axes


Contributions of this work:

 - Large-scale pretraniing helps a lot.


## Pre-training

 -The ViT can handle arbitrary sequence lengths up to memory constraints, but the pre-trained positional embeddings may no longer be meaningful. So do 2D interpolation of the pre-trained embeddings according to location in original image
 - This is basically the way to handle images which are larger than what was in the training data.


## Training
 -  Batch size of 4096, weight decay of 0.1.
 -  Linear learning rate warmup and decay.
 -  Fine-tuning: SGD with momentum, batch size 512.


## Model configs

ViT-L/16: "Large" variant with 16x16 input patch size, D: 1024, 16 heads, 24 layers
ViT-H/14: "Huge" variant with 14x14 input patch size, D: 1280, 16 heads, 32 layers.

## Results

Transformer models pre-trained on JFT-300M outperforms resnet baseline on all datasets while taking less resources to pre-train.

Fine-tuning accuracy.

Few-shot accuracies: solve regularized LSQ problem which maps the forzen representation of a subset of training images to -1, 1 target vectors.

Takes 2.5k TPU-core-days. Nice.

Comparison: BiTL (ResNet152x4, which takes 9.9k tpu-core-days and gets 1% lower on ImageNet).

All in all the results are incrementally better, but it does seem to take less time on a TPU. That's probably just because you can parallelize attention more easily.

## How important is the size of the pre-training dataset?

Apparently they "shine" when pre-trained on larger datasets. That's not so clear from the plots. If anything I would say that you're doing marginally better.

On the fewshot case, ViT seems to be able to better make use of pre-training.

## Analysis of internal representations

Examine the "attention distance" which is analogous to the receptive filed size in the CNNs.

To get the "attention maps" - use "Attention Flow" (Quantifying attention flow in transformers)

## Future work

 - Using ViT for detection and segmentation
 - Self-supervised pretrinaing methods (like SimCLR)