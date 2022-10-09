---
title: "NeuroLogic A*esque Decoding: Constrained Text Generation with Lookahead Heuristics."
venue: "NAACL-HLT"
pages: "780-799"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/naacl/LuWWJKKBQYZSC22"
ee: "https://aclanthology.org/2022.naacl-main.57"
url: "https://dblp.org/rec/conf/naacl/LuWWJKKBQYZSC22"
authors: ["Ximing Lu", "Sean Welleck", "Peter West", "Liwei Jiang", "Jungo Kasai", "Daniel Khashabi", "Ronan Le Bras", "Lianhui Qin", "Youngjae Yu", "Rowan Zellers", "Noah A. Smith", "Yejin Choi"]
sync_version: 3
cite_key: "conf/naacl/LuWWJKKBQYZSC22"
---

Basic idea: Tree-search generation using A*. You incorporate heuristic estimates of future cost.

Eg, "write a sentence with these concepts". You can do lookahead to see that selecting "winter" is more likely
to generate "snow" later on, so you pick "winter".

The lookahead heuristic approximates cost at each decoding step based on continuations of the sequence-so-far.

Their decoder is based on NeuroLogic, which is basically just a constraint satisfaction problem.

How do you come up with the heuristic? You need some function that maximizes: $f(a) = s(a) + h(a)$, eg
score-so-far + heuristic cost.

What kind of heuristic works? Remember that it needs to be admissible and monotonic.

$$
Y_t = \arg \text{topk}_{y_{\le t} \in Y_t'} \{s(y_{\le t}) + \max_{y < t}(y_{< t} y_t, y_{> t})\}
$$

The score-so-far in this case is $s(y_{\le t}) = \log p_{\theta}(y_{\le t})$

Basically each element is a length-l continuation of the sequence. It degrades
to beam searhc if you set $l$ and $h$ to zero.

How to generate lookaheads?

 - Greedy
 - Sampling
 - Bream

Experiments:

 - CommonGen: Commonsense generation task with lexical constraints
 - Machine Translation: WMT17 EN-DE test data where you require certain terminology
 - Table-to-text: Esnure that output text is consistent with input structured data (E2ENLG)
 - Question Generation: Generate a question containing some keywords
 - Commonsense story generation: RocStories: given some prompt, generate the rest of the story, control for diversity by using unique n-grams