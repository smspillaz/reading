---
title: Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer.
venue: J. Mach. Learn. Res.
volume: 21
pages: 140:1-140:67
year: 2020
type: Journal Articles
access: open
key: journals/jmlr/RaffelSRLNMZLL20
ee: http://jmlr.org/papers/v21/20-074.html
url: https://dblp.org/rec/journals/jmlr/RaffelSRLNMZLL20
authors: ["Colin Raffel", "Noam Shazeer", "Adam Roberts", "Katherine Lee", "Sharan Narang", "Michael Matena", "Yanqi Zhou", "Wei Li 0133", "Peter J. Liu"]
sync_version: 3
cite_key: journals/jmlr/RaffelSRLNMZLL20
---

This paper studies transfer learning and the limits of transfer learning.

Studies pre-training objectives, architectures and unlabelled datasets, transfer approaches and other factors.

Dataset: Colossal Clean Crawled Corpus"

The rapid rate of progress and diversity of techniques in this burgeoning ield can make it difficult to compare different algorithms, tease apart the effect of new contributions and understand the sapce of existing methods for transfer learning.

Leverage a unified approach to transfer learning that allows the systematic study of different approaches and push the limits of the current field.

Basic idea behind this work: Every text processing problem is text-to-text. Take some text as input, produce some text as output. Eg, all text problems are question answering, language modelling or span extraction. This means that you can apply the same objective, traing procedure and decodoing process to every task.

## Model
One big transformer. Map input sequence tokens to embeddings, then encode them with a transformer encoder.

Main difference: Use layernorm where no bias is added.

Relative positional encodings. How do they work?

 - a different learned embedding according to the offset between the key and query being compared.
 - Each position embedding is a scalar added to the corresponding logit.
 - Position encodings are also shared between layers.
 - Only 32 position offset embeddings, covering logarithmic step sizes for ranges.
 - One layer is not sensitive to relative positions beyond 128 tokens, but the receptive field increases as the number of layers increase, so this is fine.


## Dataset: Collosal Clean Crawled Corpus

Start with Common Crawl. Most of it is not natural language though, its mostly gibberish or boilerplate like menu text.

So filter as follows:

 - Retain lines that end in a punctuation mark (period, !, ?, or ")
 - Discard any page with < 5 sentences
 - Removed any page that contained any word on the "list of dirty, naughty, obscene or otherwise bad words"
 - Removed any line with the word "Javascript"
 - Lorem ipsum
 - Code (anything with a curly bracket)
 - Any three-sentence-span occurring more than once

Filter out anything non-Englihs wiht langdetect.

## Downstream tasks

1. GLUE
	1. Sentence acceptability judgment
	2. Sentiment analysis
	3. Paraphrasing
	4. NLI
	5. Coreference resolution
	6. Sentence completion
	7. Word Sense Disambiguation
	8. Question Answering
2. SuperGLUE
	1. CNN/Daily Mail abstractive summarization
	2. SQuAD question answering
	3. WMT English to German, French and Romanian
3. Definitive Pronoun Resolution


## Input / Output Format

For translation text-to-text is obvious

For classification, use a word as the target (eg "true", "false")

Follows previous work such as Natural Language Decathlon, which uses a consistent Q-A format for a suite of ten different tasks.

Use short-task prefixes instead of an explicit question answer format. Eg, "tl;dr:" for summarization.

Winograd tasks: Highlight the ambiguous pronoun in the text passage and predict which noun it refers to. Eg, "the city councilmen refused the demonstrators a permit because *they* feard violence", and the prediction should be "The city councilmen".

## Experiments

Try to compare a variety of different approaches on a set of tasks while keeping many factors fixed as possible. In this sense, not all approaches can be replicated exactly.

For example, we cannot use BERT since BERT is encoder-only.

### Baseline

Standard encoder-decoder transformer. Encoder and decoder the same size as BERT base.

Train using standard maximum likelihood using teacher forcing and cross-entropy loss. Use greedy decoding.

Inverse square root learning schedule.

### Vocabulary

SentencePiece to encode text as WordPiece tokens. Vocabulary size of 32000 wordpieces.

### Unsupervised Objective

Denoising objective (masked language modelling), predicting missing or otherwise corrupted language tokens.

Randomly sample and drop 15% of tokens, replacing spans by a single sentinel token. Target corresponds to all dropped-out spans.

# Comparing Architectural Variants

1. Encoder/Decoder (fully visible in encoder, causal in decoder)
2. Language Model (causal mask throughout)
3. Prefix-LM (Fully-visible on the input, same arch as language model)


One drawback of the language model framework in the text-to-text setting is that causl masking forces the model's representation of the $i$th input to depend only on entries up to $i$. This is a problem when you're trying to determine the meaning of words in the prefix stament, because you cannot look at words ahead of it.

On a Transformer based LM you can just use fully-visible masking for the prefix. Problem solved.

## How to compare different model structures

More parameters equals better performance usually, so you need some mechansim to compare these LLMs. Not quite as simple as the number of parameters, the number of connections also matters.

Use M to refer to number of FLOPs required for an L + L layer encoder-decoder or an L-layer decoder-only model:

 * Encoder-decoder with L layers in encoder and L layers in decoder, this has 2P parameters
 * Equivalent model but with parameters shared across encoder and decoder resulting in P parameters in an M-FLOP computational cost
 * Encoder-decoder with L/2 layers each in the encoder and decoder with P parmaeters and an M/2 FLOP cost
 * Decoder-only language model wiht L layers and P parameters, resulting M fLOPs
 * Decoder-only prefix-LM with the same architecture but with fully-visible self-attention

## Objectives for unsupervised modelling

* Prefix Language Modelling Thank you for inviting me | to your party last week
* BERT-style Thank you (M) (M) me to your party apple week.
* Deshuffling party for your to . last fun you inviting me Thank
* MASS-style Thank you (M) (M) me to your party (M) week
* IID noise, replace spans Thank you (M) me to your party (Y) week
* IID nose drop tokens Thank you me to your party week
* Random Spans Thank you (X) to (Y) week


The BERT0-style objective performs best, though prefix language modelling attains similar performance on translation tasks.

#### Simplifying the BERT objective

Can we modify the BERT-style denoising objective?

1. Don't include random token swapping
2. Avoid predicitng the entire uncorrputed text span

Dropping corrupted tokens completely gives a small improvement in the GLUE score.

#### Corruption Rate

Corruption rate changes have a limited effect on the model performance, but too much corruption is bad.

#### Corrupting Spans vs Tokens

Corrupting too big a span underperforms.


### Choice of Pretraining Dataset

C4

Unfiltered C4

RealNews-Like (filter C4 for news content domains)

WebText-like (filter C4 for thigns submitted to Reddit receiving a score of at least 3)

Wikipedia

Wikipedia + Toronto Books

Removing the filter from C4 uniformly degrades performance and makes the unfiltered variant perform worst in every task.

Pre-training on in-domain unlabelled data can imporve performance on downstream tasks. (eg, using RealNews-like dataset gives an increase in the Exact Match score for ReCoRD, reading comprehension on news articles)

### Size of Pretraining Dataset

Performance degrades as dataset size shrinks. Model begins to memorize the dataset.


### Training Strategy

Many different finetuning methods:

 * Adapter layers: Keep the model fixed, learn some layers on top
 * Gradual Unfreezing: Finetune more and more of the parameters over time

### Multitask Learning

 * Train the model on multiple tasks at once
 * One problem: How much data should each task do you use? Not so much data that it just memorizes the training set. How exactly to set the proprotion of data coming from each task can depend on various factors
	 * Dataset size
	 * Difficulty of learning the task
	 * Regularization
 * Other issues
	 * Task interference
	 * Negative Transfer

Different strategies:
 * Examples-proportional mixing. If hte number of examples in each of $N$ tasks's datasets is $e_n, n \in \{1, ..., N\}$ then set probabiliyt of sampling an example from the $m$th task during training to $r_m = \frac{\min(e_m, K)}{\sum \min(e_n,K)}$ where $K$ is the artifical data set size limit. This has the effect sampling less from tasks that have less data.
 * Temperature-scaled mixing: Adjust the temperature of the mixing rates. Raise each probability to $\frac{1}{T}$. As $T \to \inf$ then this index goes to 0 and the probability goes to 1, which implies equal mixing.
 * Equal-mixing: Sample examples from each task with equal probability. Likely suboptimal since it means that you overfit on the low-resource tasks and underfit on high-resource tasks.

### Combining Multi-Task Learning with Fine-Tuning

Consider the case where you're pretrained on all tasks and then finetuned on specific tasks (MT-DNN).

Leave-one-out fine-tuning: Pre-train on all the tasks except the target task, then finetune on the target task. Performance of leave-one-out was only slightly worse than not leaving out, suggesting that a model trained on a variety of tasks can still adapt to new tasks.


## Scaling

"You were just given 4x more compute, what should you scale to make the most of it?"

Start with baseline, 220M parameters and pre-trained and fine-tuned for $2^{19}$ and $2^{18}$ steps. Encoder and decoder are similar to BERT BASe.

Two variants with 16 and 32 layers in the encoder and decoder, producing models with 2x and 4x as many parameters as the original.

When increasing training steps, scale both pre-training and fine-tunning steps.

When increasing the number of pre-training steps, you're effectively including more pre-training data as C4 is so alrge that you cannot complete one pass over the data even when training for $2^{23}$ steps.

Anotehr way to do it would be to increase the batch size by a factor of 4. But training with a 4x larger batch size can give a different outcome to training for 4x as many steps.

The results say that if you want to improve performance with this additional budget, the best approach is to increase both the size by 2 and the number of training steps by 2. Increasing the number of size by 4 as opposed to increasing the training steps by 4 helps a little bit, but more data and bigger size = better performance.

"We did not observe a large difference between training a 2x bigger model for 2x as long and training a 4x bigger model on any of the tasks as we studied. This suggests that increasing the training time and increasing the model size can be complementary means of improving performance."


# Conclusions

1. Objective: Use a mean span length fo 3 and corrupt 15% of the original sequence
2. Longer Training: Additional pre-training is helpful, but too much repetition of the data is harmful.
3. Multi-task pre-training
4. Fine-tuning on individual tasks: Does slightly better than fine-tuning on all tasks at once.

## Outlook

1. The inconvenience of large models: Large models do better. This is not so good for low-resource tasks or low-resource training environments.
2. More efficient knowledge extraction: Provide model with general purpose knowledge. Would be nice if we could get good fine-tuning performance without pretraining on 1 trillion tokens of text first
3. Formalizing the similarity between tasks: Pre-training on unlabelled in-domain data can improve performance on downstream tasks. SQuAD was created using data from Wikipedia. Would be useful to have some notion of similarity between two datasets so that we can pre-train on datasets which are not similar and test transfer performance.
4. Language-agnostic: Training on just English doesn't get you good translation performance.