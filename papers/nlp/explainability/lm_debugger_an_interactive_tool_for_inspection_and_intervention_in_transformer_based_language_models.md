---
title: "LM-Debugger: An Interactive Tool for Inspection and Intervention in Transformer-Based Language Models."
tags: ["ai2"]
venue: "CoRR"
volume: "abs/2204.12130"
year: "2022"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2204-12130"
doi: "10.48550/ARXIV.2204.12130"
ee: "https://doi.org/10.48550/arXiv.2204.12130"
url: "https://dblp.org/rec/journals/corr/abs-2204-12130"
authors: ["Mor Geva", "Avi Caciularu", "Guy Dar", "Paul Roit", "Shoval Sadde", "Micah Shlain", "Bar Tamir", "Yoav Goldberg"]
sync_version: 3
cite_key: "journals/corr/abs-2204-12130/Geva/2022"
---

Code at this [link](https://github.com/mega002/)

Current interpretation methods mostly focus on probing the model from the outside, eg, executing behavioural tests, analyzing salience from input features. Not much in terms of internal prediction construction process.

![[lm_debugger_sample.png]]

Introduces `LM-Debugger`, interactive debugging tool for transformer based LMs.

Updates by the FFN can be decomposed into a weighted collection of sub-updates, each induced by an FFN parameter vector.

LM-debugger has three main capabilities:
 1. For a given input, interpret predictions at each layer in the network. Project the token representations before and after the FNN update.
 2. Intervene in predictions by changing the weights of specific sub-updates.
 3. Learns a search index over all the parameter vectors across the network and relates them to tokens that they promote.

## Interpretation Method

A transformer has some L layers and an embedding matrix over some vocabular.

If we let $x^l_{i}$ be the hidden representation of some token $i$ at layer $l$, we can define it as $x^l_i = x^{l - 1}_i + \text{FFN}(\text{MHSA}(x^{l - 1}_i))$

We can project this to the vocabulary space by taking the outer product with the embeddings, eg $p^l_i = \text{softmax}(Ex^{l}_i)$

Now, each FFN is given by $\text{FFN}^l(x^l) = \sum^{d_m} f(x^l \cdot k^l_i) v^l_i = \sum^{d_m}_{i = 1} m^l v^l_i$

Eg, if we consider that we have the parameter matrix $K$ and $V$ (not to be confused with the keys and values of attentions), we have essentially a sum over the features of the intermediate dimension of $x^l$ dot $k_i$ for feature $i$, then through activation $f$, the dot of $f(x^l \cdot k_i) \cdot v_i$. Eg, feature $i$ comes from $f(x^l \cdot k_i) k_i$

Now, with $L$ layers, there are $L \times d_m$ "value vectors" and therefore $L \times d_m$ sub-updates.

## So how does LM-Debugger work?

You can run inputs through the model to generate text in an autoregressive manner and apply interventions.

The prediction trace: user enters an input for which a detailed trace of the predition across the network is provided. Then you show the top tokens in the output distribution and the 10 most dominant FFN sub-updates.

You can also do interventions - eg, set the coefficient of any vector values and induce your own sub-updates.

Value vectros can be interpreted by the top tokens that they promote. So by considering these sets of tokens as textual documents, LM-Debugger allows for search for concepts encoded in value vectors across layers.

You can also trace FFN updates, eg, by looking at the sub-updates on each layer.

You can also use it for controlled language generation.