---
title: "The Dual Form of Neural Networks Revisited: Connecting Test Time Predictions to Training Patterns via Spotlights of Attention."
venue: "ICML"
pages: "9639-9659"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/IrieCS22"
ee: "https://proceedings.mlr.press/v162/irie22a.html"
url: "https://dblp.org/rec/conf/icml/IrieCS22"
authors: ["Kazuki Irie", "R\u00f3bert Csord\u00e1s", "J\u00fcrgen Schmidhuber"]
sync_version: 3
cite_key: "conf/icml/IrieCS22"
---

Linear layers in neural networks trained by gradient descent are essentially a key-value system that memorizes the training data and initial weights, producing unnormalized dot product attention over the entire training experience.

If you look at neural networks in this way (the "dual" form), you can visualize how an NN makes use of training patterns at test time by examining the attention weights.

How is it possible for DALL-E 2 to generalize

Why is there a duality?

Linear layer: $W = \sum^T v_t \otimes k_t, y = Wx$

Attention: $y = (\sum^T v_t \otimes k_t) x$

Eg, we just can see $W$ as being broken down into a kind of outer product between keys and values.

A linear layer trained by gradient descent also has this duality. Eg, the weight matrix is given by:

$$
W = W_0 + \sum^T e_t \otimes x_t
$$
where $W_0$ is the initialization and $e_t$ is the error signal and $x_t$ is the input. Then we say that the model is $y = Wx$

This can also be seen as a layer storing $T$ key-value pairs $(x_1, e_1) ... (x_t, e_t)$, eg:

$$
W = W_0 + XE^T
$$

Or in other words:  $W = W_0 + \sum^T x_t \otimes e_t$

Of course the computational complexity of this depends on $|T|$.

### Some Experiments
The way that they confirm this in the experiments is to train an NN by backpropagation, but also keep a record of all the data points and error signals seen during training.

After training, you can compute the attention weights between all training samples and any test example by putting the test data through the model to get the input to each layer, then computing the corresponding dot product with the stored inputs.

#### Single Task

Two layer feedforward NN on MNIST.

In figure 4, they take some test example from class 6 and then compute the dot product between it and every other example seen during training, partitioning by class and sorting by dot product value on the y axis. Training examples in class 6 have the highest attention score, followed by examples in class 1 and class 8.