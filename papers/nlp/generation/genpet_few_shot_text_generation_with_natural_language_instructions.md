---
title: Few-Shot Text Generation with Natural Language Instructions.
venue: EMNLP
pages: 390-402
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/emnlp/SchickS21
doi: 10.18653/V1/2021.EMNLP-MAIN.32
ee: https://doi.org/10.18653/v1/2021.emnlp-main.32
url: https://dblp.org/rec/conf/emnlp/SchickS21
authors: ["Timo Schick", "Hinrich Sch\u00fctze"]
sync_version: 3
cite_key: conf/emnlp/SchickS21
---

"It is crucila to find task descriptions that are easy to understand for the pretrained model and ensure that it actually makes good use of them".

"Measures also have to be taken against overfitting".

Introduces GENPET, a method for tet generation based on pattern-explotiing training, a recent approach for combining textual instructions with supervised learning.

GENPET is based on PET. PET combines the idea of probing MLMs with gradient based learning for efficient few-shot text classification.

Contributions:
 - GENPET
 - Training with PEGASUS and GENPET outperforms standard finetuning across a broad set of tasks and training set sizes
 - Quantification

PEGASUS is a transformer encoder-decoder which is pretrained using gap-sentence generation.

Requires a set of documents with multiple sentences.

1. Pick a subset of the most informative sentences
2. Replace sentences with a mask
3. Concatenate the premoved sentences into a pseudo-summary.


# Pretraining and Fine-tuning

Pretraining large NNs with an LM objective and then fine-tuning has lead to some significant improvements.

Anotehr approach: Pretrain a large NN on a task that more closely matches the downstrea mtask and then fine-tune.

Fine-tuning still requires lots of data. What happens if you only have a small amount of data?

Reforumlating the downstream taks to make it more similar to the pretraining objective can yield good results.


# Pattern-Exploiting Training

It can be applied to problems where a text sequence $x \in \mathcal{X}$ must be mapped to a label from a finite set $\mathcal{Y}$. It converts the inputs into "cloze questions" which dramatically reduces the number of examples requires.

A cloze question is one where you have to fill in the blank with the label.

In GENPET, they extend this to fine-tuning language models for text generation. Three key challenges tackeld

1. How to provide an instruciton to an encoder-decoder model so that the model can make the best possible use of it
2. How can we ensure that the modle understands the instrucitons provided sufficiently well and how to deal with the fact that even minor modifications can have a big impact on performance
3. How to prevent overfitting

consider a model $p_M(y|z) = \prod^n p_M(y_i|z; y{1:i - 1})$ where $p_M(y_i|z; y{1:i - 1})$ comes from processing $z$ usin the enocder and $y_{1:i - 1}$ using the decoder.

If we hapen to know some prefix, then you can condition on that too: $p_M(y|z;y_{1:k - 1}) = \prod^n_{i = k} p_M(y_i|z; y{1:i - 1})$

![[pet_training.png]]

They found that tokens belonging to the decoder have a much stronger impct ona model's prediction than regualr input tokens.

So they supplement each pattern $P$ with a decoder prefix that is given to the model as part of the generated sequence rather than the observed input.

## How to combine instrucitons
Multi-pattern approach.

Given pairs of patterns and corresponding decoder prefixes, and a set of models, we aim to obtain a single model $M$ that contains the combined knowledge of all models.

We require a small set of unlabeled examples $\mathcal{U}$. Generate one output sequence per pattern-decoder prefix pair using greedy decoding. Then to assign a score, first compute the log-likelihood of $y$ for each pair, and the total score of $y$ is then simply the exponentiated average over the patterns.

## Preventing overfitting

### Unsupervised Scoring

Compute $s(y|x)$ but use an untrained model to compute $p_{(P_i, d_i)}(y|x)$ for all $i \in \{1, ..., k\}$.

The intuition is that if for a given input a trained model simply reproduces phrases from its training set, then the resulting pair of input and output texts should look strange. Use this idea to discard generated texts of poor quality.

### Joint Training

Assume the existence of an ensemble where each model was trained using a different instruction.

Also train a single model jointly on all instructions. Forcing a single model to work wel for all instructions can act as a regularizer to prevent overfitting.
