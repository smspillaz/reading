---
title: "Quark: Controllable Text Generation with Reinforced Unlearning."
tags: ["ai2"]
venue: "CoRR"
volume: "abs/2205.13636"
year: "2022"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2205-13636"
doi: "10.48550/ARXIV.2205.13636"
ee: "https://doi.org/10.48550/arXiv.2205.13636"
url: "https://dblp.org/rec/journals/corr/abs-2205-13636"
authors: ["Ximing Lu", "Sean Welleck", "Liwei Jiang", "Jack Hessel", "Lianhui Qin", "Peter West", "Prithviraj Ammanabrolu", "Yejin Choi"]
sync_version: 3
cite_key: "journals/corr/abs-2205-13636/Lu/2022"
---

Large scale language models can learn behaviours that are misaligned with user expectations.

How can we unlearn these things?

![[quark_controllable_unlearning_pipeline.png]]

Quantized Reward Konditioning

Basically, you optimize some reward for quantifying an unwanted property while not straying too far from the original model. Reward function doesn't have to be differentiable.

The quantization is pretty important because it helps with training stability. Otherwise the reward function has too high variance. So by sampling from high reward quantiles and using the KL divergence penalty during learning, you improve the language model but don't stray too from from the original model.

Its not like regular RL where you just try to drive down the reward. Instead what happens if that you *condition* on the reward and generate samples based on having the reward token present. So good tasks have the "good" token present, bad generations have the "bad" token present.

You can also feed into your own training but sampling from what you think highly-rewarding generations will be.

Then at test time, just ask for nice sentences.

## Experiments

Experiments include unlearning toxicity (from realtoxicityprompts), unlearning unwanted sentiments,  unlearning degenerate repetition.

## Ablations

How much does the KL term matter? A larger $\beta$ on the KL term encourages you to stay closer to the original model, meaning that you still get the bad completions.

How much does the number of quantiles matter? More quantiles leads to more effective reward maximization, but strays more from the original model.

Can you just train on the highest reward quantile: Nope, means that you only learn to generate one thing.

Can you just condition on random rewards? Nope, because then you don't maximize reward anymore.