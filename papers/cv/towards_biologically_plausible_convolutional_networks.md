---
title: "Towards Biologically Plausible Convolutional Networks."
venue: "CoRR"
volume: "abs/2106.13031"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2106-13031"
ee: "https://arxiv.org/abs/2106.13031"
url: "https://dblp.org/rec/journals/corr/abs-2106-13031"
authors: ["Roman Pogodin", "Yash Mehta", "Timothy P. Lillicrap", "Peter E. Latham"]
sync_version: 3
cite_key: "journals/corr/abs-2106-13031/Pogodin/2021"
tags: ["DeepMind"]
---

Main idea behind this paper: Human vision does not use weight sharing, so convolution cannot be biologically plausible. Local connections are possible, weight sharing is not possible.

However, locally connected but nonconvolutional networks can underperform convolutional ones.

What is a plausible alternative to weight sharing that uses the same regularization principle, eg, each neuron in the pool should react similarly to identical inputs?

Proposes to add lateral connectivity to a locally connected network, allowing learning via Hebbian plasticity. Pause occassionally for a "weight sharing phase". This gets you "nearly convolutional" performance.

In the "dynamic weight sharing scheme", you don't get perfect convolutional connectivity because in each channel only subgroups of neurons share weights.

## Related Work

**Vision Transformers / Transformers without SA**: All of these need weight sharing - at each block the input is reshaed into patches and the same weight is used for all patches.

## Regularization in locally connected networks

Convolutional nets implemented by depending on a difference in indices and sharing weigths.

Locally connect is just that, but without weight sharing. Eg, each output pixel has its own set of corresponding weights, but those weights are sparse and apply only to a subset of the inputs.

#### How to do this?

Can you develop *approximately convolutional weights*?  So, eg, $w_{ij} \approx w_{i - j}$?

One straightforward way to do it is just augmenting the data to provide multiple translations of the image. That way, you will see the image from many perspectives.

Another way is to modify the network so that during learning, weights become approximately convolutional. Add lateral connections and a "sleep phase", eg, the weghts relax to their mean over output neurons. So the mean idea is that you let the weights diverge and then "correct" them periodically using a kind of student-teacher architecture.

However, need to take care that the initial weights are not overwritten during hebbian learning.

Consider the following rule:

$$
\triangle w_i \propto -(z_i - \frac{1}{N} \sum^N_j z_j - \gamma (w_i - w_i^{\text{init}}))
$$

If we present the network with $M$ different inputs and denote the covariance $C = \frac{1}{M} \sum_m X_m x_m^T$ then the weight converges to:

$$
w_i^{*} = (C + \gamma I)^{-1} (C \frac{1}{N} \sum^N w^{\text{init}}_j + \gamma w_i^{\text{init}})
$$
(this is a well known consequence of L2 regularization), we are just adding $\frac{1}{\gamma}$ to the eigenvalues of the covariance.

For all kernel sizes, the weights converge to a nearly convolutional solution within a few hundred iterations.

### Dynamic Weight Sharing in Multiple Locally connected Layers

When you have $k$ dimensional inputs, then $x$ repeats every $k$ neurons.

## Realistic model that implements the update rule


In a realistic circuit, you update with excitatory neurons and an inhibitory neuron:

$$
\tau r_i = -r_i + w^T_i x = \alpha r_{\text{inh}} + b
$$
$$
\tau r_{\text{inh}} = -r_{\text{inh}} + \frac{1}{N} \sum r_j - b
$$

Then the equation converges to a fixed point:

$$
b + w^T_i  = \frac{1}{N} \sum_j w_j^T x
$$

For strong inhibition (eg, a large alpha), you can use an anti-hebbian term.


## Results

### Metric

$$
\text{SNR}w = \frac{1}{k^2} \sum_j \frac{(\frac{1}{N}) \sum_i (w_i)_j)^2}{\frac{1}{N} \sum_i((w_i)_j - \frac{1}{N}\sum_{i'} (w_{i'})_j)^2}
$$

### Datasets

 * CIFAR 10
 * CIFAR 100
 * TinyImageNet
 * ImageNet

A locally connected network on its own has only 29.6\% Top-1 accuracy on TinyImageNet compared to a convolutional architecture of the same number of layers/dimensions.

Data augmentatino can improve the situation somewhat, but weight sharing can help a lot, the more you do it the better. Obviously if you do weight sharing every batch then that's basically just a convolutional network.

### Brain-Score Metric

How well representations built by the network correspond to the ventral stream data in primates.

Brain-score correlates with imagenet performance, so the worse brain-score performance of astandard locally connected network can be related to the poor image net performance.