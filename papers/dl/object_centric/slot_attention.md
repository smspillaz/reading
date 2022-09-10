---
title: Object-Centric Learning with Slot Attention.
venue: NeurIPS
year: 2020
type: Conference and Workshop Papers
access: open
key: conf/nips/LocatelloWUMHUD20
ee: https://proceedings.neurips.cc/paper/2020/hash/8511df98c02ab60aea1b2356c013bc0f-Abstract.html
url: https://dblp.org/rec/conf/nips/LocatelloWUMHUD20
authors: ["Francesco Locatello", "Dirk Weissenborn", "Thomas Unterthiner", "Aravindh Mahendran", "Georg Heigold", "Jakob Uszkoreit", "Alexey Dosovitskiy", "Thomas Kipf"]
sync_version: 3
cite_key: conf/nips/LocatelloWUMHUD20
---
# Object-Centric Learning with Slot Attention

Most deep learning approaches for image processing captures texture information but not really
object information. Can we learn object representations in an unsupervised way which we can later
use for some task (knowing only about the objects and not the pixels themselves?).

Summary: Produce output vectors corresponding to an object in the input, where the vector is the properties of the object.

## Slot Attention Module

Map from N input features to K output vectors.

Algorithm:
 - for iterations 0 to T
   - Compute attention over keys computed from inputs and queries computed from slots
   - Compute weighted mean over inputs using attention weights
   - Assign to slots based on previous state and newly attended to inputs with RNN (GRU)
   - Residual MLP

## How can we use this for object discovery?

Create an autoencoder with the following architecture:
 - Encoder: CNN with positional embeddings -> Slot Attention
 - Decoder: Spatial Broadcast Decoder using position embeddings. Decode using CNN of W x H x 4

Idea: Slots act as a representational bottleneck that cause only parts of the image to be decoded.

## Set Prediction

Motivation: Point cloud prediction, classifying multiple objects, generation of molecules.

Given an image and a set of things in that image. K! permutations of the set, slots should not be biased towards
any one of them.

Encoder:
 - CNN + positional embeddings -> slot attention
 - MLP from each slot to a label. Parameters shared for each slot. Match predictions and labels using hungarian algorithm.

## How does this relate to other things in the filed?
 - IODINE: Uses variational inference
 - MONet, GENESIS: Multiple encoder / decode step

## How does this relate to NNs for sets?
 - NB: Slot attention handles the problem of mapping from one set to another set of
   different cardinality while respecting permutation symmetry.
 - Prior work (DSPN) learns an ordered representation of the output set with per-element initialization.

## How does this relate to iterative routing?
 - Similar to CapsNet

## Soft Clustering
 - Kind of like soft k-means clustering: Dot product similarity with learned linear projections.


# Limitations

(1) Background slot
(2) Positional encoding is absolute, so no translation equivariance
(3) Slot attention "does not know about objects per-se", segmentation largely driven by downstream task.
  - > Does not actually detect objects, but relies on downstream task to do this.

# Ablation Study

- Position embeddings matter if you want to retain positional information.
- Slot Attention: If we just attend to the input axis and not the slot axis, we lose information required to force competition between slots
- GRU update: Marignally helps (10% AP improvement)

How to pick the number of training slots?
 - Too many slots slightly harms object discovery
 - But with more slots, property prediction is a bit easier.
 - Upper bound: NUmber of objects in the dataset

# Proof that slot attention is permutation invariance