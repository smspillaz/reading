---
title: Between words and characters - A Brief History of Open-Vocabulary Modeling and Tokenization in NLP.
venue: CoRR
volume: abs/2112.10508
year: 2021
type: Informal Publications
access: open
key: journals/corr/abs-2112-10508
ee: https://arxiv.org/abs/2112.10508
url: https://dblp.org/rec/journals/corr/abs-2112-10508
authors: ["Sabrina J. Mielke", "Zaid Alyafeai", "Elizabeth Salesky", "Colin Raffel", "Manan Dey", "Matthias Gall\u00e9", "Arun Raja", "Chenglei Si", "Wilson Y. Lee", "Beno\u00eet Sagot", "Samson Tan"]
sync_version: 3
cite_key: journals/corr/abs-2112-10508/Mielke/2021
---

Examines the question of "what are the units of text that we want to model"?

Many different choices:
  - words?
  - bpe?
  - subwords?
  - characters/bytes?


There is probably no single bullet, but its worth thinking about.

Recently there has been some interest in trying to learn the tokenization ourselves, by learning likely word boundaries, unsupervised.

## Multiword tokens

A large range of phenomena make it highly non-trivial to identify and even consistently define linguistic units:
 - Contractions (don't)
 - French "aux"
 - Compounds (copier-coller)
 - Logical-derivatives: "anti-Trump"

Several word forms can be represented by the same token. Multiword tokens.

These days tokenization involves the task of segmenting into "non-typographically motivated units", which are often smaller then classical tokens and therefore called sub-words.

## Pre-Tokenization

Many tooks now known as "pre-tokeniers" have been in use for a while. Denotes the task of segmenting sentences into atomic units in general.

It is also common for tokenizers to do normalization (spelling correction, NER, replace entities with ENT, space normalization, punctuation normalization, etc). Normalization is irreversible.

## Augmenting word-level pre-tokenizer tokens with character information

Word-level models have one weaknes, which is inability to deal with OOV tokens. Rare words are replaced with UNK at training time. Two drawbacks of this approach:

 1. UNK not acceptable when you want to do NLG
 2. UNKs have no features. But the new word might be similar to other words!
 3. In LOTE, removing rare words is infeasible.

### Spelling Information

King, Kim, Jozefow: Deterministically construct a word's embedding from its spelling. But this implicitly trains a CNN to get the "frequent words right" instead of anticipating novel words.

FastText gives you embeddings from overlapping n-grams.

CharacterBERT/CharBert: Enhance BPE units embedding with character embeddings.

Pinter: Mimic embedding of a word given its spelling using a helper RNN (eg, regress word2vec embeddings using RNN from character embeddings)

## Open vocabulary language modelling with tokenizer-defined words made of characters.


Extending a closed-vocabulary generative model to an open-vocabulary one (eg, predicting novel words at test time) is diffcult because you have to model a PMF for an infinite set of sentences.

Luong and Manning, Mielke and Eisner: Augments the ordinary closed-vocab RNN by adding an auxiliary task - make the word embeddings predictive of their spellings using the word embedding as an input to an RNN. Then if a word is OOV, you can generate a new word by just spelling it with the smaller model.

Kawakami et al: Each word is spelled out if it cannot be *copied* from the recent past using a cache.

El Hihi and Bengio: have higher layers of a multi-layer RNN update sparsely.

## Learning Segmentations to find concatenative word-like pretokenizer tokens

Can you learn the tokenization with machine learning? Treat it like a segmentation problem to find segments corresponding to the real units.

### Character level models learning to skip steps

Elman RNN: Prediction "surprise" when it comes to word boundaries.

Schmidhuber / Doval and Gomez: Split microblog texts in which spaces are delted.

HM-RNN (Chung): Multiple timescales, but learn skip/update. However other work shoes that this does not work so well.

### Marginalization over all possible segmentations

Latent variable approach.

#### Approximate Marginalization

Average Hidden States

Hiraoka: N-best tokenizations fed into any sentence encoder

Chan: MAP inference through beam search.

Hiraoka: Unigram LM tokenization proposal distributions, n-best tokenizations of a sentence are fed into any sentence encoder model independently, average in line with a-priori tokenization likelihood.



#### Exact Marginalization using additional independence assumptions - segmenting neural language models

Segmentation as a sequence-to-sequence task. Go from characters to a cocvering sequence of substrings.

Segmentation decisions can use word context, find a covering using dynamic programming. Central independence assumtion: model does not depend on ay other segments when scoring a segment, merely on surrounding characters.

Sun and Deng: "Segmental Language Model": train on chinese characters and use learned segments to compete on chinese word segmentation.

Kawakami: Multimodal, training on image captions - if the model has access to the image segmentation performance improves.

He: Transformer model as a leanred tokenizer.


### Bayesian Nonparametric Models

Bayesian view of autoregressive language models may prove beneficial. Reinterpret smoothing and backoff as inference.

Teh: Hierarchical PYP language model, where we have n-gram distributions of arbitrarily large orders.

Goldwater: Explain how new words are coined, two stage language models (generator which creates new lexemes and adaptor, which governs reuse)

Assign positive probability to an infinite number of possible lexemes, it then becomes possible to try and infer word boundaries, perform unsupervsed word segmentation.

## Unsupervised Chinese Word Segmentation

For CJK (the article says Vietnamese but this is just wrong), word segmentation can be tricky.

Popular unsupervised approaches:
 - Discriminative
 - Generative

Discriminative models rely on a "goodness measure" for segmentation. For example, mutual information, variation of branching entropy, minimum descriptor length.

Generative models focus on finding the optimal segmenation of the highest generative probability, eg, HMM, HDP, NPY.


## Learning subword vocabularies

How to use subword units?

 - One option, manually constructed rule-based systems
 - Data-drive segmentation learners
 - Simple heuristics 

Subword segmentation might be a bad idea when you have nonconcatenative morphological phenomena.

### Manually constructed linguistic analyzers

* Porter Stemmer
* Finite state tools
* BITE (Tan et al): Convert inflected forms into lemma and tag to protect against noise and improve on dialectical data
	* Eg, "Hoping" => "Hope V.PTCP;PRS"
	* "Ate" => "Eat PST" (allows sharing of tense information)

### Dealing with other languages

#### German / Finnish / Swedish / Dutch

How to split the compound words? (Koehn and Knight, Braschler and Ripplinger, Macherey)

#### Sanskrit

Processes that occurr at and cross word boundaries.

#### Arabic

#### Chinese

Convert characters to stroke orders or romanization sequences before applying BPE in order to capture glyph or prounciation.


### Unsupervised Morphological Segmentation

Minimum Description Length

Initial: Lightly guided by additional information on possible morphological structure, eg, partitioning word types into sets of steps with either suffixes or prefixes.

Morfessor: Recursive MDL model based on unigram morph requenceis and lengths. Has a tendency to over-segment.

Morfessor CatMAP: Categories Maximum A-Posteriori, HMM-based model of the sequential nature of loose morphological categories. Priors can be learned in a semi-supervised way using wordlists. Remains ideal for concatenative morphology such as English, Finnish Turkish, German.

Paradigm Learning: Incorporate the notion of morphological paradigms and inflection classes.

### Modern Fast Subword segmentation algorithms

* *BPE*: Replace pairs of adjacent symbols with a new symbol representing the pair.
* *WordPiece*: Don't merge the most often co-occurring pair but pairs that increase the likelihood reached by an n-gram language model trained with this updated vocabulary
* *UnigramLM*: Just use a unigram LM, not an n-gram LM like WordPiece. Iteratively removes subword units from a starting vocabulary that contains far more subword units than are desired. Prune the lowest-probability items.
	* BPE-dropout: Skipping of individual merges provides some regularization


## Shared Vocabularies in multilingual models

Johnson et al: Should we oversmaple low-resource languages when learning a data-driven tokenizer and to what degree?

Acs and Rust show that BERT-based transformers are still biased towards high resourced languages. Visible in the word's "fertility", eg the minimum number of subwords a word is split into on average. This is lower for English than it is for finnish.

These granularity differences affect the sharing of semantic representations.

### Character Level Models

Character sequences are much longer than word or subword sequences which makes inference time longer.

chung et al: A bi-scale RNN; enable the decoder to produce character sequences - they demonstrate improved performacne over a subword level decoder.

Lee, Gao: Convolution and pooling layers at the input of the encoder.

