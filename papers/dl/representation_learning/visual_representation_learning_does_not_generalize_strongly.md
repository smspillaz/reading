---
title: "Visual Representation Learning Does Not Generalize Strongly Within the Same Domain."
venue: "CoRR"
volume: "abs/2107.08221"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2107-08221"
ee: "https://arxiv.org/abs/2107.08221"
url: "https://dblp.org/rec/journals/corr/abs-2107-08221"
authors: ["Lukas Schott", "Julius von K\u00fcgelgen", "Frederik Tr\u00e4uble", "Peter V. Gehler", "Chris Russell", "Matthias Bethge", "Bernhard Sch\u00f6lkopf", "Francesco Locatello", "Wieland Brendel"]
sync_version: 3
cite_key: "journals/corr/abs-2107-08221/Schott/2021"
---

# Visual Representation Learning does not Generalize Strongly within the same domain

 - Recompose, interpolate or extrapolate only existing factors of variation from the training data.
 - Hypothesis: Models that learn the correct mechanism should be able to genearlize to this benchmark
 - Result: They fail to do so


Split the training and test data such that the models that learned the underlying mechanisms should be able to generalize to the test data

Several splits:
 - Composition: train: small hearts, large squares, test: large hearts, small squares
 - Interpolation: train: small hearts, large hearts, test: medium hearts
 - Extrapolation: train: small hearts, medium hearts, test: large hearts


Result: As soon as you go OOD, model predicts something that's ID.

Also introduces CelebGlow, which is a more "natural" dataset than the artificial ones introduced in dSprites, Shapes3D, MPI3D etc. Generated based on latent traversals.

## Problem

Assume that you render each observation using a computer graphic model - takes a set of independently controllable factors.

In the OOD setting you generate the test data differently than the way the training data was generated. The prior $p_{\text{test}}(y)$ is different. Each point can only have non-zero probability mass in either $p_{\text{train}}(y)$ or $p_{\text{test}}(y)$.

$g(\cdot)$ maps between independently controllable factors and $y$.

We want to learn $f$ such that ideally $f = g^{-1}$. But we only observe data from $p_{\text{train}}(y)$

## Objective

What inductive biases help on these OOD settings?

How best to leverage training data to learn representations that generalize?

### Bias 1: Representational Format

Postulate that there are latent variables, try to infer those in an unsupervised fashion.

Idea behind ICA and disentanglement.

Consider $\beta-\text{VAE}$, Ada-GVAE, Slow-VAE and PCL. Learn a representation, freeze the encoder and train an MLP to learn $y$ from $z$.

### Bias 2: Architectural - Supervised Learning

eg, CNN

### Bias 3: Transfer Learning

Eg, ResNet-50, ResNet-101 pretrained on ImageNet-21k.

## Splits

 - Composition
 - Interpolation
 - Extrapolation
 - Random

## Evaluation

 - Coefficient of determination, $R^2$
 - $R^2 = 1 - \frac{E_{(x, y) \in D_{\text{test}}}[(y_j - f_j(x))^2]}{\sigma^2_i}$
 - 1 means perfect regression, 0 means random guessing, since MSE is identical to variance per fecator.

## Results

Weakly supervised/unsupervised representation learning models garbage at composition. Fully supervised models are OK.

Mixed results on interpolation, but transfer learning methods do better.

Almost all models except transfer learning are garbage at extrapolation