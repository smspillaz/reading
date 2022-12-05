---
title: "Transformers generalize differently from information stored in context vs in weights."
venue: "CoRR"
volume: "abs/2210.05675"
year: "2022"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2210-05675"
doi: "10.48550/ARXIV.2210.05675"
ee: "https://doi.org/10.48550/arXiv.2210.05675"
url: "https://dblp.org/rec/journals/corr/abs-2210-05675"
authors: ["Stephanie C. Y. Chan", "Ishita Dasgupta", "Junkyung Kim", "Dharshan Kumaran", "Andrew K. Lampinen", "Felix Hill"]
sync_version: 3
cite_key: "journals/corr/abs-2210-05675/Chan/2022"
---

How does generalization work when you rely on in-context learning vs weight-based learning? Does the transformer come to different solutions?

This paper finds that there are different solutions depending on the training mode. If you memorize things in the weights, you get generalization that is more rule-based. If you rely on the context, you get things that are exemplar based (copy what's in the examples).

How does this play out in practice?

Lets say you have a dataset of tokens X, W, A and B. The inputs are cartesian coordinates and the outputs are tokens corresponding to a class. You see the following examples (plus noise):

 - bottom left -> WA
 - top left -> XA
 - bottom right -> WB

A *rule based* system would classify top right as XB (first token corresponds to y-coordinate, second token corresponds to x-coordinate).

An *example-based* system with classify as either XA or WB, but not both, because it is copying from the examples.

The training regimes for transformers are consistent with this finding. If you train weights-based, the context is completely irrelevant and you have to rely on the weights to predict (the labels are consistent). If you train examples-based, the labels are few-shot, so they shift every episode, meaning that you need to look at the examples.


Do these patterns hold for pretrained language models? Lets try an LLM, but instead of shape and color, use nonsense words.