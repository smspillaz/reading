---
title: "Evaluating the Impact of Model Scale for Compositional Generalization in Semantic Parsing."
venue: "CoRR"
volume: "abs/2205.12253"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2205-12253"
doi: "10.48550/ARXIV.2205.12253"
ee: "https://doi.org/10.48550/arXiv.2205.12253"
url: "https://dblp.org/rec/journals/corr/abs-2205-12253"
authors: ["Linlu Qiu", "Peter Shaw", "Panupong Pasupat", "Tianze Shi", "Jonathan Herzig", "Emily Pitler", "Fei Sha", "Kristina Toutanova"]
sync_version: 3
cite_key: "journals/corr/abs-2205-12253/Qiu/2022"
---

They look into what makes CG work in semantic parsing.

The main result is that they show model scale doesn't matter so much, but prompt tuning can help a lot. The model performance is strongly dependent on the retrieved examples. Like if you have an oracle retriever which knows what the relevant examples are, it does much better than just sampling uniformly from the training data. Adding more examples also helps, up to a certain point. It helps more in the non-oracle case, usually because then you're increasing coverage of the data space.