---
title: "Socratic Models - Composing Zero-Shot Multimodal Reasoning with Language."
venue: "CoRR"
volume: "abs/2204.00598"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2204-00598"
doi: "10.48550/ARXIV.2204.00598"
ee: "https://doi.org/10.48550/arXiv.2204.00598"
url: "https://dblp.org/rec/journals/corr/abs-2204-00598"
authors: ["Andy Zeng", "Adrian Wong", "Stefan Welker", "Krzysztof Choromanski", "Federico Tombari", "Aveek Purohit", "Michael S. Ryoo", "Vikas Sindhwani", "Johnny Lee", "Vincent Vanhoucke", "Pete Florence"]
sync_version: 3
cite_key: "journals/corr/abs-2204-00598/Zeng/2022"
---

Large scale models (visual/language models), (language models) and audio LMs are trained on disjoint data. These models store different forms of commonsense knowledge across different domains.

Can we somehow integrate this or use it for multi-modal tasks? The authors demonstrate that this model diversity can be leveraged to build an AI system with structured Socratic dialogue.

Socratic Models use language as the representation by which inter-domain foundation models can be jointly used for inference. Imagine it as the "models talking to each other".


![[socratic_models_illustration.png]]

There are two primary components:

 - Assembling video into a language-based world-state history
 - Performing various types of open-ended text-prompted tasks based on that world-state history.

![[socratic_model_q_and_a.png]]

It is envisionedhere that you have a model that captions what the agent is doing, then generates language-based world-state history from this video. You can then use this text to perform open-ended reasoning later on (eg, "did I eat dinner today?" "Yes, I was eating a sandwich at 5.27 pm")

You can also go the other way around too, by providing a caption to search for and then finding video frames corresponding to that caption.