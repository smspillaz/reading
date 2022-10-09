---
title: "Epistemic Neural Networks."
venue: "CoRR"
volume: "abs/2107.08924"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2107-08924"
ee: "https://arxiv.org/abs/2107.08924"
url: "https://dblp.org/rec/journals/corr/abs-2107-08924"
authors: ["Ian Osband", "Zheng Wen", "Mohammad Asghari", "Morteza Ibrahimi", "Xiyuan Lu", "Benjamin Van Roy"]
sync_version: 3
cite_key: "journals/corr/abs-2107-08924/Osband/2021"
---

Bayesian Neural Networks are a special case of ENNs.

This can be used as a replacement to ensemble methods to measure type-2 error.

Motivating example:
 - Say you have  duck/rabbit classifer. A typical neural network gives you p(duck|input) and p(rabbit|input).
 - These predictions don't distinguish genuine ambiguity from insufficiency of data.
 - What if you make a joint prediction across two identical inputs? In this case, treat your model as a population of learners, where each time you route the task of prediction to a different person. Eg in a joint prediction you predict whether you have rabbit-rabbit, duck-duck, rabbit-duck or duck-rabbit.
 - If this table is one where you have predictions on the diagonal, then the issue epistemic uncertainty, eg, you just don't know enough about the problem. But if the table is one where the image is ambiguous, you'd have probabilty distributed everywhere.

Why do we care? Because we want to know if the uncertainty will get resolved with more data.

What this does in practice: ENNs can help with joint-log-loss, because you're more likely to be conservative in your estimates when you are uncertain about the problem. In joint-log-loss you get a batch of images and see how you do jointly over them.

Joint probability gives you a probability for each class combination, which you can get by multiplying marginals.

## Difference between an NN and an ENN

ENN gets an input an an index. Index is a latent variable. Eg, a 10-dimensional gaussian. The network generates this and uses it while it makes predictions.

In a standard neural network, you have joint probability like:

$$
\prod^{\tau}_{t = 0} \text{softmax}(f(\theta, x_t))_{y_t}
$$
Eg,  to get the joint probability over all inputs in some sequence $x_0, ..., x_{\tau}$, you multiply over the softmax probability estimated by the network corresponding to each input's label.

In an epistemic neural networks, your joint probability looks like this:

$$
\int P_Z(dz) \prod^{\tau}_{t = 0} \text{softmax}(f(\theta, x_t, z))_{y_t}
$$

Eg, you integrate over your latent variable $z$ over its distribution.

When you make a joint prediction, you use the same $z$ across multiple predictions. Depending on this $z$, the joint prediction is not the same as the product of marginals. The integral over $z$ can couple the predictions.

## Epinet

![[epinet.png]]

An ENN that you add to the base network to make the combination an ENN.

Key idea is randomized prior functions. Sample something from prior and then add trainable function.

Test uncertainty depends on generalization.