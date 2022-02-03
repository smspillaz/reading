# OOD Q and A

## Are generative models causal?

Bengio: Distinguish causal generative models from the broader class of generative models

Kording: Motor control: Generative models, they allow us to simulate the world around us

Bengio: What do we need to make the generative models more likely to be the causal truth

Kording: Can't figure out causality unless you can interact with the world

Bengio: Not sufficient to do intervention to discover the causal structure, still an identifiability problem

## Large pretrained multi-modal models are very robust to OOD. Why?

Bengio: Multimodality is not sufficient to recover much of the causal structure. Lay down some inductive biases that are congruent. Sparsity, interventions only affect one of the properties.

Bernhard: We're just avoid the problem if we keep doing IID. We have to build solutions that take into account the combinatorial nature of thesep roblems. You need to have modularity that reflects certain repeating elements of structure. Need to identify which module to use to solve the problem? Modularization is probably the key.

Amit: Often the data is very high dimensional, causal concepts in language are in words and sentences. One of the biggest challenges.

Bengio: Modularization. Think beyond the identification of one module = one mechanism. Physics: How are they expressed. They are expressed with mathematical language that has a standard re-used operations, multiplication, division and so on. The mechanisms are not just re-used but they are defined in terms of re-usable concepts (multiply, divide and so on).

Bernhard: Visual system can function in a large dynamic range.

## How to detect OOD? Benchmarks?

Kording: Benchmarks are super important to drive progress. Questions - what is a good benchmark? Biology has a nice one - we spend most of our time doing one thing but that's not what drives evolution. What prepares us for the encounter with a lion? Its a rare event!

Amit: Causal inference has had a problem that benchmarks are hard to construct because the counterfactuals are unknown. For OOD we can use prediction metrics, but the field is very much dependent on the diversity of domains collected - what is the right metric or the worst case?

Leyla: The role that simulation or causal generation plays in this.  Most animals do this as part of our OOD preparation.

Yoshua: This is kind of orthogonal to OOD generalization. Invovles issues of uncertainty.

Bernhard: Compositional generalization - I've seen a lion from the distance, if a lion can eat a gazelle then it can also eat a human.

## Disentanglement

Yoshua: That's the whole point. If you have identified the the causal mechanisms that relate them, then because of compositionality, its very likely that new setting can be explained with the variables and mechanisms that you already know. This means you can generalize perfectly OOD.

 - The kind of disentanglement we care about is not what people call disentangled
 - Disentangled variables do not necessarily have to be independent - they can still be dependent. Looking for independent latent factors is not the kind of thing that gets you the power?


Joshua: This is closely related to all the other quesitons
 - Our perspective on learning theory goes back to IID.
 - In natural learning you have nonstationary dynamics.
 - Need to assume that there's a way of factorizing


## Learning causal relationships by trying intervention experiments

You need an encoder that maps the pixels to putative causal variables.

Need to have causal mecahnisms that explain the relationships.

We want to do interventions that reduce epistemic uncertainty the most.

## How can we have good abstraction that aids generalization in OOD

Jovo: OOD construction is a bit artificial. You can make the distribution arbitrarily complex. Now its not OOD anymore, now its in-distirbution. You can keep playing the game of where learning comes in.

