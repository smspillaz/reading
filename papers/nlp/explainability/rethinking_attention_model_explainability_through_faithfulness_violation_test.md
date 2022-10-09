---
title: "Rethinking Attention-Model Explainability through Faithfulness Violation Test."
venue: "ICML"
pages: "13807-13824"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/LiuLGKL022"
ee: "https://proceedings.mlr.press/v162/liu22i.html"
url: "https://dblp.org/rec/conf/icml/LiuLGKL022"
authors: ["Yibing Liu", "Haoliang Li", "Yangyang Guo", "Chenqi Kong", "Jing Li", "Shiqi Wang"]
sync_version: 3
cite_key: "conf/icml/LiuLGKL022"
---

Attention produces probability distributions over the input which are deemed as "feature importance indicators". However there is one critical limitation with this, which is the weakness in identifying the polarity of feature impact. Eg, features with higher weights might actually be *suppressing* as opposed to *contributing* to the final outcome.

Proposes a diagnostic methodology called the "faithfulness violation test" to measure consistency between explanation weights and impact on polarity. The study shows that most attention-based explanation methods are hindered by faithfulness violation, especially raw attention.

This is illustrated by a figure which shows a VQA model with attention weights on the image for a given question. On the $y$-axis, you have the change in confidence of the predicted label once the top 10% of attention weights are removed. Red regions show predictions where the top 10% of attention weights are actually negative polarity, eg, they are suppressing the model prediction.

A faithful explanation should at least possess two properties:
 - importance correlation: magnitude of explanation weights which precisely reflect the importance of the inputs (1)
 - polarity consistency: sign of the weights should correctly indicate the policy of model impact. (2)

Most explanation methods do (1) very well, but don't really deal with (2), and this can result in misleading explanations, eg, you see large weights on a certain part of the image and are misled into believing that this part of the image matters for the prediction, but its actually suppressing some prediction, eg, there's a large *negative* correlation between what is in the image and the predicted label.

Faithfulness violation test is defined as: $$\triangle C(x, x^*) = f(x)_{\hat{y}} - f(x \setminus x^*)_{\hat{y}}$$

where $x^* = \arg \max_{x_i \in \mathbf{x}} ||w(x_i)||$, eg, the most influential feature in a data point $\mathbf{x}$. Usually this means that for sequences, this is the most influential token.

In other words, $\triangle C$ measures how much a prediction for the ground-truth label changes if you remove the  most influential feature. The intuition is that if you remove the most important feature according to $w(x_i)$, then $\triangle C$ should be *positive* because $f(x)_{\hat{y}} > f(x \setminus x^*)_{\hat{y}}$. But if $\triangle C$ is negative, then that is a *faithfulness violation*, because the confidence actually becomes *stronger* once you remove the most important feature according to the weights.

In the paper they test lots of different explanation methods, for example taking the attention weights, attention rollout, integrated gradients etc over lots of different model types with different types of attention.

The factors that affect faithfulness violation are  mainly the depth of the network.