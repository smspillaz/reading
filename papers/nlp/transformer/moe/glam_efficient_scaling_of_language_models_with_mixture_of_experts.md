---
title: "GLaM - Efficient Scaling of Language Models with Mixture-of-Experts."
venue: "CoRR"
volume: "abs/2112.06905"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2112-06905"
ee: "https://arxiv.org/abs/2112.06905"
url: "https://dblp.org/rec/journals/corr/abs-2112-06905"
authors: ["Nan Du", "Yanping Huang", "Andrew M. Dai", "Simon Tong", "Dmitry Lepikhin", "Yuanzhong Xu", "Maxim Krikun", "Yanqi Zhou", "Adams Wei Yu", "Orhan Firat", "Barret Zoph", "Liam Fedus", "Maarten Bosma", "Zongwei Zhou", "Tao Wang", "Yu Emma Wang", "Kellie Webster", "Marie Pellat", "Kevin Robinson", "Kathy Meier-Hellstern", "Toju Duke", "Lucas Dixon", "Kun Zhang", "Quoc V. Le", "Yonghui Wu", "Zhifeng Chen", "Claire Cui"]
sync_version: 3
cite_key: "journals/corr/abs-2112-06905/Du/2021"
---

GLaM: Sparsely activated mixture of experts architecture to scale the model capacity while also incurring substantially less training cost. Eg, GLaM has 1.2 trillion parameters, which is 7x larger than GPT-3 but only consumes 1/3 of the energy and requires 1/2 of the flops for inference.

GLaM is a "mixture of experts" model. Each MoE layer is interleaved with a Transformer layer. The gating module selects the 2 most relevant experts out of 64, then we compute the weighted average outputs of the experts.

Effectively this means that you have $O(E^2)$ different combinations of feedforwards instead of one.