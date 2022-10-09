---
title: "Staged Training for Transformer Language Models."
venue: "ICML"
pages: "19893-19908"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/ShenWKDPB22"
ee: "https://proceedings.mlr.press/v162/shen22f.html"
url: "https://dblp.org/rec/conf/icml/ShenWKDPB22"
authors: ["Sheng Shen", "Pete Walsh", "Kurt Keutzer", "Jesse Dodge", "Matthew E. Peters", "Iz Beltagy"]
sync_version: 3
cite_key: "conf/icml/ShenWKDPB22"
---

Right now when we compare language models, we're comparing model sizes from different random initializations. The initializations have to be different because you have a different number of weights.

As an alternative, you could start with a smaller "seed" model with the same initialization, then "grow" it to other models by applying a growth operator. They preserve both the loss and the training dynamics after applying the operator.

Loss preservation has a fairly straightforward definition.

To preserve training dynamics, define $\phi_k$ as the model at step $k$ and $\phi_{k + 1}$ as the model after one step of gradient descent.

We want:

$$
\frac{\partial}{\partial C} \mathcal{L}(\phi, C) = E_{D}[\frac{l(\phi_k, \mathcal{D}) - l(\phi_{k + 1}, \mathcal{D})}{C_k}]
$$

### Growth Operators

Double the hidden dimension of the entire model.

For layer norm terms, just duplicate the weights and biases.

For linear layers, you do the growth operator like:
$$
\begin{pmatrix} W & 0 \\ 0 & W \end{pmatrix}
$$
This growth operator is loss-preserving. However it is not dynamics preserving.

In order to do that you have to match the learning rate schedule.