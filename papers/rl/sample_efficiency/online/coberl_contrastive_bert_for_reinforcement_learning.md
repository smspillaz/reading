---
title: "CoBERL - Contrastive BERT for Reinforcement Learning."
venue: "CoRR"
volume: "abs/2107.05431"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2107-05431"
ee: "https://arxiv.org/abs/2107.05431"
url: "https://dblp.org/rec/journals/corr/abs-2107-05431"
authors: ["Andrea Banino", "Adri\u00e0 Puigdom\u00e8nech Badia", "Jacob C. Walker", "Tim Scholtes", "Jovana Mitrovic", "Charles Blundell"]
sync_version: 3
cite_key: "journals/corr/abs-2107-05431/Banino/2021"
tags: ["DeepMind"]
---


 Contrastive BERT for Reinforcement Learning.

Combines a new contrastive loss and hybrid LSTM transformer to tackle the challenge of improving data efficiency.

Bidirectional masked prediction in combination with a generalization of recent contrastivem ethods.

Extending BERT masked prediction to RL isn't trivial because in RL there are no discrete targets. Instead use RELIC and extend it to the time domain and use it as a proxy supervision signal for the masked prediction.

Based on GTrXL [[stabilizing_transformers_for_reinforcement_learning]].

![[coberl_architecture.png]]

Main contributions:

1. A novel contrastive representation learning objective that combines masked prediction from BERT with a generalization of RELIC to the time domain
2. Gated architecture which allows learning from both BERT and LSTM
3. Improved data efficiency


Two existing methods:

 - Auxiliary self-supervised loss
 - World model and collect imagined rollouts

CoBERL is part of the first set of methods, auxiliary losses.

The inspiration comes partly from:
 - BERT: In the sense of bidirectional processing with masked prediction
 - RELIC: The targets are not discrete, but instead they are images. Having the target be the image itself isn't a good idea because there's too much correlation with nearby frames. Instead, use a contrastive objective where the positive and negative samples arise from the ordering of the trajectory.

Basically you guess which batch you're in for a given input token by looking at what the masked output token was and all the other input tokens in the batch.

The closest thing to this is [[curl_contrastive_rl]] and M-CURL (which is the masked contrastive loss)