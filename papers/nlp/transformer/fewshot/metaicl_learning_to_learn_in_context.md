---
title: "MetaICL: Learning to Learn In Context."
tags: ["ai2"]
venue: "NAACL-HLT"
pages: "2791-2809"
year: "2022"
type: "Conference and Workshop Papers"
access: "open"
key: "conf/naacl/MinLZH22"
doi: "10.18653/V1/2022.NAACL-MAIN.201"
ee: "https://doi.org/10.18653/v1/2022.naacl-main.201"
url: "https://dblp.org/rec/conf/naacl/MinLZH22"
authors: ["Sewon Min", "Mike Lewis", "Luke Zettlemoyer", "Hannaneh Hajishirzi"]
sync_version: 3
cite_key: "conf/naacl/MinLZH22"
---

Pre-trained language model is tuned to do in-context learning on a large set of training tasks. esult is that it enables the model to learn a new task in context at test time.

The setup is pretty straightforward. You get $k$ meta-training examples, then one more support example that you have to predict the output sequence for.

Related work: In-context learning with LM achieves poor performance when target task is too different from language modeling in nature or if LM is not large enough.

## Channel MetaICL

Reparameterize $P(y|x)$ as $\frac{P(x|y)P(y)}{P(x)}$ using Bayes Rule. Do $P(y) = \frac{1}{\mathcal{|C|}}$

At meta-training time, you give the model the concatenation of $y_1, x_1 ..., y_{k}, x_k, y_{t + 1}$ and you have to predict $x_{k + 1}$.

## Experiments

Comparing:
 - Zero-shot LM
 - In-context LM
 - PMI 0-shot, PMI in-context (domain-conditional pointwise mutual information)
 - Channel 0-shot, Channel in-context
 - Finetuning


The biggest gains are in the HR -> LR, non-NLI -> NLI and non-Paraphrase -> Paraphrase settings.

HR -> LR is "high resource" to "low resource".

non-NLI to NLI -> is where the meta-training tasks do not overlap with the target tasks in task format and required capabilities.

The gains are mostly on unseen domains.

MetaICL can do about as well as fine-tuning can.

How many meta-training tasks do you need? More is better, but there is diminishing returns. More meta-training tasks in general means less variance and can boost mean performance by about 5 points.
