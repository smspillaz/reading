---
title: Encode, Tag, Realize - High-Precision Text Editing.
venue: EMNLP/IJCNLP
pages: 5053-5064
year: 2019
type: Conference and Workshop Papers
access: open
key: conf/emnlp/MalmiKRMS19
doi: 10.18653/V1/D19-1510
ee: https://doi.org/10.18653/v1/D19-1510
url: https://dblp.org/rec/conf/emnlp/MalmiKRMS19
authors: ["Eric Malmi", "Sebastian Krause", "Sascha Rothe", "Daniil Mirylenka", "Aliaksei Severyn"]
sync_version: 3
cite_key: conf/emnlp/MalmiKRMS19
---

Proposes the LaserTagger method; a sequence tagging approach that does text summarization as a text-editing task, eg, by predicting a sequence of edits.

To predict edits, use BERT encoder along with autoregressive Transformer decoder.

Performs comparably to seq2seq baselines with a large number of training examples and outperforms them when the number of examples is limited.

Also, inference time is 2x faster.

## Problem Context

Using a full sequence-to-sequence model when the output overlaps significantly with the input is a bit wasteful.

Another inductive bias is the copy one - choose which tokens to copy, then infill the missing words. These still require a large training set however, since they depend on output vocabularies as large as those used in standard seq2seq.

## Contributions

Propose a text-editing model that applies a set of edit operations on the input sequence to reconstruct the output.

You only need a small vocabulary which consists of edit operations in order to reproduce a large percentage of the output sequences in the test set. Having a smaller vocab helps to reduce the number of training examples required to train accurate models.

Two versions of the model are described:

1. LaserTagger FF: Based on BERT
2. LaserTarget AR: Autoregressive, BERT encoder with a transfer decoder.
3. Evaluations
4. Inference time evaluations and sample efficiency evaluations.
5. Controllability evaluations.

## Related Wrok

1. Text Simplification: Eg, sentence compression (applying a drop operation on the token/phrase level), while more intricate systems also do split/reoder/substitution. There is also a text editing model called EditNTS which introduces an interpreter mode and generates added tokens one-by-one from a full coabulary. See Also Levenshein Transformer which does text editing by performing a sequence of deleting and insertion actions.
2. Single document summarization: Shorten texts in a meaning preserving way (eg, deletion based methods, neural-encoder-decoder to do abstractive summarization)
3. Grammatical Error Correction: System is presented with some text and needs to fix the mistakes. Can be solved either with a classifier for specific error types, or a statistical MT method.

## Model

Three steps:

1. Encode (build a representation of the input)
2. Tag (assign edits tags from a pre-computed output vocabulary to the input tokens)
3. Realize (apply a rule-based mechanism to convert tags into the output text tokens)



Tags consist of two components, the base tag and the added prhase.

Base tag: KEEP or DELETE.

Added prhase: Can be empty, or can consist of one in a small vocabulary V, which defines a set of words and phrases that can be added into the sequence before the current token.

Additional task specific tags can be added, eg, SWAP:

 - Can only be applied to the last period of the first sentence, instructs the realize step to swap the order of the sentences.

Other tags:

 - PRONOMINALIZE: Look up entity mention in a dictionary with appropriate pronouns so that the model doesn't have to guess them from the context.


## How to optimize phrase vocabulary

We want to minimize the number of phrases in the vocab, while maximizing the number of output texts that can be reconstructed.

This is related to the minimum k-union problem, which is NP-hard.

How to identify candidate phrases to be included then?

 - Align source and target texts using the LCS.
 - n-grams in the target whcih are not part of the LCS are prhases to be included.
 - sort the phrases by te number of prhase sets in which they occurr and pick the $l$ most frequent phrases.

## How to convert training targets into training target tags

No need to convert the LCS. Do it greedily:

For each word in the target
1. Greedily match against a word in the source (eg, two pointers)
2. If no match for that word, match against phrases in $V$.
	1. If a match found, mark the most recent word in the source as keep (along with the relacement phrase), then advance in the target accordingly

If a target requires adding a phrase that is not in $V$, it is filtered out.

# Model Architecture for Tagging

1. Encoder: BERT Transformer
2. Decoder: Autoregressive


# Experiments

## Sentence Fusion

 - Balanced Wikipedia DiscoFuse. 10.5% require input reordering.
 - Evaluation: Exact Score and SARI (F1 scores of added/kept/deleted n-grams)

## Split and Rephrase

* WikiSplit dataset. 1M human-editor created examples of splits. A phrase vocabulary of size 500 gives 31% coverage of the targets.


Main result: SARI as a function of the training data size for three models. Tagging outperforms seq2seq unless you have 10s of 1000s of data points.


## Abstractive Summarization

- Reduce length of text while preserving its meaning.
- Can add new words and reorder the sentence.
- Even though a text-editing approach is not well-suited for extreme summarization exmaples (complete paraphrase with zero lexical overlap), in practice limited paraphrasing capability already good enoguh.

## Grammatical Error Correction

# Inference Time

For batch size 8, LaserTagger AR is 10x faster than Seq2Seq BERT. Only need one layer of decoder instead of 12 and no encoder-decoder cross-attention.

LaserTagger FF is 100x faster than BERT, but a little less accurate.

# Qualitative Evaluation

Error patterns:
 - Imaginary Words
 - Repeated Phrases
 - Premature EOS
 - Hallucinations 
 - Coreference Issues
 - Misleading rephrasing
 - Lazy sentence splitting


# Limitations of this approach

1. Arbitrary word reordering is not feasible, but limited reordering can be achieved with SWAP tokens.
2. Might be tough on languages not as morphologically rich as English.

