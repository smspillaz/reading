---
title: Human Instruction-Following with Deep Reinforcement Learning via Transfer-Learning from Text.
venue: CoRR
volume: abs/2005.09382
year: 2020
type: Informal Publications
access: open
key: journals/corr/abs-2005-09382
ee: https://arxiv.org/abs/2005.09382
url: https://dblp.org/rec/journals/corr/abs-2005-09382
authors: ["Felix Hill", "Sona Mokra", "Nathaniel Wong", "Tim Harley"]
sync_version: 3
cite_key: journals/corr/abs-2005-09382/Hill/2020
---

# Human Instruction-Following with Deep Reinforcement Learning via Transfer Learning from Text


Instruction-following with Deep RL typically invovles a simulator and templates.

This paper proposes a conceptually simple method for training instruction-following agents with deep RL that is robust to natural human instrucitons.

The basic idea is to apply BERT on tasks requiring an agent to identify and position every-day objects relative to other objects in naturalistic 3D simulated rooms. You can get substantially aove chance zero-shot rnasfer from sythetic template commands to natural instrucitons.


## SHIFTT method

1. Train or acquire pretrained language model $L$
2. Construct language-dependent object manipulation task and binary spatial relationship
3. For each episode:
	1. Sample a subset $G' \subset G, ||g|| > 2$ of unique objects and individual objects from $G''$
	2. Samle some spatial relationship
	3. Construct an instruction according to a template "Put the $w_1$ $w_s$ the $w_2$" where $w_x$ is an everyday name for an object or relation $x$
	4. Spawn all $g \in G''$ and an agent at a random position and orientation
4. Trian the agent using RL to maximize expected cumulative rewards
5. Have human testers interact with episodes and pose instructions tot he agent.



## Architecutre


### Language Encoding

1. BERT + mean pooling
2. BERT + self-attention(optimize representation to present environment or tasks)
3. BERT + cross-modal self-attention: Explicit pathway to bind visual experience to specific contextual word representations. The transformer permits interactions on the word level rather than on the sentence embedding level.
4. Pretrained sub-word embeddings
5. Typo noise


Baselines:
1. Random mean pooling
2. Word-level and word-piece transformers
3. Human


## Results/Discussion

Substnatial transfer from text requires contextual encoders. The transfer effect is much stronger in the case of full context-dependent BERT representations.