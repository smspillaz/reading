---
title: Meta-Learning to Compositionally Generalize.
venue: ACL/IJCNLP
pages: 3322-3335
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/acl/ConklinWST20
doi: 10.18653/V1/2021.ACL-LONG.258
ee: https://doi.org/10.18653/v1/2021.acl-long.258
url: https://dblp.org/rec/conf/acl/ConklinWST20
authors: ["Henry Conklin", "Bailin Wang", "Kenny Smith", "Ivan Titov"]
sync_version: 3
cite_key: conf/acl/ConklinWST20
---

In this paper, they optimize a meta-learnign augmented version of supervised-learning, where the objective directly optimizes for OOD.

Construct pairs of tasks for meta-learning by sub-sampling existing training data. Each pair of tasks is constructed to contain relevant examples, as determined by some similarity metric.

They implement MAML but for OOD. Create pairs of tasks for each batch (meta-train and meta-test) by subsampling training data. Meta-train should look like training and meta-test should look like testing. Steps taken on meta-training should benefit meta-testing.

They say that [[geca_good_enough_compositional_data_augmentation]] doesn't try to solve compositional generalization but instead just makes the task easier.

How does it work?

 - In meta-training, you do one step of SGD, then eval on the accompanying meta-test task. In mathematical terms, $\mathcal{L}_{\beta_t}(\theta) + \mathcal{L}_{\beta_g}(\theta')$ where $\theta'$ is the updated parameters from meta-training and $t$ is the train loss and $g$ is the test loss.
 - Note that this is *different* from $\mathcal{L}_{\beta_t}(\theta) + \mathcal{L}_{\beta_g}(\theta)$, because you're not constraining *how* the parameters get updated. The constraint says that you can't make $\beta_{t}$ better at the expense of $\beta_g$ . The latter still allows you for you to get better at $\beta_t$ and get worse at $\beta_g$.


We should also try to structure the virtual tasks such that they are distinct from each other. They use kernel density estimation to define a relevance distribution for each example.

A couple of different similarity metrics:

 - Levenshtein Distance
 - String-kernel similarity (number of common subsequences)
 - Tree-kernel similarity (Tree convolution kernel)


The idea is that you sample for meta-test based on similarity.

### Experiments

- SCAN / COGS

Baselines:
 - LSTM Seq2seq
 - Transformer Seq2seq
 - GECA

How do we do? Lev-MAML can improve performance a lot on SCAN MCD1 and MCD2, at least when using LSTM. It doesn't help a lot when using a Transformer. GECA + LSTM can make things even better. 

On COGS, Tree-MAML can boost performance by about 8 points on the Gen set. So not bad.

One tip for "not being able to see the OOD set". They never do any validation on the whole generalization set. Instead take a subset of the generalization set, and ensure that when you test on the real generalization set that you use a different seed.

They also say that the [[compositional_generalization_through_meta_seq2seq]] paper is perhaps not so interesting because it only solves SCAN and not other problems.
