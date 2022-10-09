---
title: "Plug and Play Language Models - A Simple Approach to Controlled Text Generation."
venue: "ICLR"
year: 2020
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/DathathriMLHFMY20"
ee: "https://openreview.net/forum?id=H1edEyBKDS"
url: "https://dblp.org/rec/conf/iclr/DathathriMLHFMY20"
authors: ["Sumanth Dathathri", "Andrea Madotto", "Janice Lan", "Jane Hung", "Eric Frank", "Piero Molino", "Jason Yosinski", "Rosanne Liu"]
sync_version: 3
cite_key: "conf/iclr/DathathriMLHFMY20"
---
Controlling attributes of generated language (eg, switching topic/sentiment) is kinda hard to do without tuning the architecture on attribute specific data.

Alternative: PPLM: Combine a pretrianed LM with one or more simple attribute classifiers that guide the text generation. Attribute model can be a simple classifier consisting of BoW.

Sampling: foward/backwrad pass in which the gradients from the attribute model push the LM's hidden activations in the direction of the classifier.

So basically MPC for NLG. Nice. You don't actually need MPC in a way, since:

$$
p(x|a) \text{ (conditional generation on attributes)}
$$
$$
p(a|x) \text{ (attribute given the text)}
$$
$$
p(x) \text{ (text)}
$$
$$
p(x|a) \propto p(a|x)p(x)
$$

But you do MPC anyway.

At each generation step, shift the history in the direction o the sum of two gradients - LL under $p(a|x)$ and LL under $p(x)$.

![[pplm_architecture.png]]

Basically, its MPC but not in the way that its usually seen. There are no "controls" to update. Instead the latents are retained during the initial foward pass, then their gradients are computed through the backward pass and an optimizer step is taken on them, then the distribution is updated again.

# Problem: Adversarial Optimization

Obvious problem: as you maximize $p(a|x)$ you forget about your original objective, which is to get fluent language.

To ensure that, three solutions:

* Update the gradients to minimize KL divergence between output distribution of modified and unmodified language models
* Post-norm geometric mean fusion