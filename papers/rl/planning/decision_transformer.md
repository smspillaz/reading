---
title: "Decision Transformer: Reinforcement Learning via Sequence Modeling."
venue: "NeurIPS"
pages: "15084-15097"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/nips/ChenLRLGLASM21"
ee: "https://proceedings.neurips.cc/paper/2021/hash/7f489f642a0ddb10272b5c31057f0663-Abstract.html"
url: "https://dblp.org/rec/conf/nips/ChenLRLGLASM21"
authors: ["Lili Chen", "Kevin Lu", "Aravind Rajeswaran", "Kimin Lee", "Aditya Grover", "Michael Laskin", "Pieter Abbeel", "Aravind Srinivas", "Igor Mordatch"]
sync_version: 3
cite_key: "conf/nips/ChenLRLGLASM21"
---

Basic idea: Model the next action based on the state and reward-to-go in a big autoregressive transformer:

$$P(a_t|R_t, s_t, a_{t  - 1}, R_{t - 1}, ..., s_0)$$
The idea is that you condition on having a high return at test time, so that you pick "good actions". Then you can train on basically random data and distill the good stuff. Assuming that its in your random data...

The method beats CQL and BC, which is cool. Though the BC benchmark is a little flawed. They compared "BC%" which is basically BC with %-data ranked by return. DT is closer to BC-10%

Longer context length? Seems to help, you can get better credit assignment.

It can also handle "gaps" in activity, eg, long distractor empty room that doesn't mean anything.

Though one though on this - does it handle out of distribution lengths? This can be sensitive to the positional encodings.

Another point: How do you decide the return-to-go? If you pick it from the training data, you're leaking the episode length. They say that they pick the max return-to-go for that task. If you have the same initialization, this is a bit problematic.