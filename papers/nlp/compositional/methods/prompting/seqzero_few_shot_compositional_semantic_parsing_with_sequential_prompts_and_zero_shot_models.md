---
title: "SeqZero: Few-shot Compositional Semantic Parsing with Sequential Prompts and Zero-shot Models."
venue: "CoRR"
volume: "abs/2205.07381"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2205-07381"
doi: "10.48550/ARXIV.2205.07381"
ee: "https://doi.org/10.48550/arXiv.2205.07381"
url: "https://dblp.org/rec/journals/corr/abs-2205-07381"
authors: ["Jingfeng Yang", "Haoming Jiang", "Qingyu Yin", "Danqing Zhang", "Bing Yin", "Diyi Yang"]
sync_version: 3
cite_key: "journals/corr/abs-2205-07381/Yang/2022"
---

They decompose the problem into a sequence of subproblems, which correspond to sub-clauses of the formal language. The LM only generates short answers using prompts for predicting sub-clauses.

In this case they're evaluating on semantic parsing (text-to-sql). You can decompose into FROM, SELECT and WHERE clauses.

Their algorithm takes an input utterance, a prompt and a grammar.

Example:

![[seqzero.png]]

Here, the prompt in the first case is "the sentence talks about:" and the correct answer is "city".

Then you have a template which replaces the placeholder with "city": eg, "from ity, the sentence asks to select:"