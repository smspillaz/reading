---
title: "ATOMIC: An Atlas of Machine Commonsense for If-Then Reasoning."
tags: ["ai2"]
venue: "AAAI"
pages: "3027-3035"
year: "2019"
type: "Conference and Workshop Papers"
access: "open"
key: "conf/aaai/SapBABLRRSC19"
doi: "10.1609/AAAI.V33I01.33013027"
ee: "https://doi.org/10.1609/aaai.v33i01.33013027"
url: "https://dblp.org/rec/conf/aaai/SapBABLRRSC19"
authors: ["Maarten Sap", "Ronan Le Bras", "Emily Allaway", "Chandra Bhagavatula", "Nicholas Lourie", "Hannah Rashkin", "Brendan Roof", "Noah A. Smith", "Yejin Choi"]
sync_version: 3
cite_key: "conf/aaai/SapBABLRRSC19"
---

ATOMIC is an atlas of everday commonsense reasoning, organized through 877k textual descriptions of inferential knowledge.

There are nine if-then relation types to distinguish causes vs effects, agents vs themes and voluntary vs involuntary, actions vs mental sttaes.

They show that neural models can acquire simple commonsesen capabilities and reason about unseen events.

Motivation: Given some observation, we can reason about unobserved causes and effects. Eg "X repels Y's attack" - X probably wants to protect themselves. Plausible pre-conditions are: "X knows how to repel Y's attack".

In this paper they create a knowledge repository of these sorts of implicit facts, then see if an NNLM can reason about unseen events by leveraging the repository.

Relation types:
 - If event then mental state
 - If event then event
 - If event then persona

They use GloVe and represent the event phrase as a sequence of word vectors and encode it into a vector-space representation using some encoding function, in this case a bidirectional GRU. The decoder takes this and predicts some target.

They do a train/valid/test split at random and measure BLEU scores of sequence generation.

At inference time use beam search to get the 10 most likely inferences per "dimension" of reasoning.