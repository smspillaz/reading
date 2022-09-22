---
title: Grokking - Generalization Beyond Overfitting on Small Algorithmic Datasets.
venue: Mathematical Reasoning in General Artificial Intelligence Workshop, ICLR 2021
volume: 1
year: 2022
type: Informal Publications
access: open
key: journals/corr/abs-2201-02177
ee: https://arxiv.org/abs/2201.02177
url: https://dblp.org/rec/journals/corr/abs-2201-02177
authors: ["Alethea Power", "Yuri Burda", "Harrison Edwards", "Igor Babuschkin", "Vedant Misra"]
sync_version: 3
cite_key: journals/corr/abs-2201-02177/Power/2022
---

In this study, they look at a few things:

 1. Transformers can generalize past the point of fitting the dataset
 2. Generalization as a function of dataset size: smaller datasets require more optimization

First figures: You need 1000 steps to fit the training data, but then 1,000,000 steps to fit the unseen combinations. They also did a study to see how "steps until generalization" varies with the fraction of the training set - if you have most of the training set, this number is small, but if you have a small fraction this number is large. Eventually it becomes impossible.

The funny thing is that during the optimization, validation set performance seems to be flat until suddenly it isn't.

They mainly experiment on binary operations. Eg, a op b = c.

Anyway, their contributions are:
1. NNs are capable of generalizing to empty slots in a variety of binary op tables
2. Long after overfitting, validation accurracy suddenly increases
3. Data efficiency curves
4. Amount of optimization required for generalization increases as dataset size decreases
5. Optimization details to improve data efficiency. Weight decay helps.
6. If you visualize the symbol embeddings, something clearly interesting is happening.


In Figure 2 they show different datasets and their "percent of data / time required to generalize" tradeoffs.

Symmetric operations (x + y, x * y etc) tend to require less data for generalization than non-symmetric ones (x - y, x / y). For a transformer you can just learn a symmetric function by ignoring the positional embeddings.

## Effect of regularization

In figure 2 they look at different optimization techniques and how this affects "grokking". The thing that helps the most is AdamW and high weight decay, eg, 1.

## Visualizing the embeddings

Figure 3: T-sne plots of row vectors of the output layer for modular addition. You can seen clear reflections of the structure of the underlying mathematical objects. Structure more apparent when you use weight decay.