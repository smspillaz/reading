---
title: "Improving Compositional Generalization with Latent Structure and Data Augmentation."
venue: "NAACL-HLT"
pages: "4341-4362"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/naacl/QiuSPNLST22"
ee: "https://aclanthology.org/2022.naacl-main.323"
url: "https://dblp.org/rec/conf/naacl/QiuSPNLST22"
authors: ["Linlu Qiu", "Peter Shaw", "Panupong Pasupat", "Pawel Krzysztof Nowak", "Tal Linzen", "Fei Sha", "Kristina Toutanova"]
sync_version: 3
cite_key: "conf/naacl/QiuSPNLST22"
---

Training set - Creating an event or creating an org charge.

During testing, you hae to generalize to to a combination.

Two challenges:
 1. Compositional Generalization
 2. Natural language variation: Humans can express the same thing in different ways.

Two lines of work:
 - Specialized approach works well on synthetic dataset
 - Generic seq2seq models work well on natural dataaset but don't generalize well.

We want a seq2seq model with greater flexibility.

Training examples are recombined using the *Compositional Structure Learner*. A generative model with a quasi-syncrhonous context free grammar backbone, induced from the training data.

CSL can recombine examples recurisvely and also defines a probabilistic sampling distribution over input-output pairs.

We assume that the conditional distribution of $y|x$ is uncahnged between source and target distributions. However, any o the following could be true:

$$
p_s(x, y) \ne p_t(x, y)
$$

$$
p_s(x|y) \ne p_t(x|y)
$$
$$
p_s(x) \ne p_t(x)
$$
$$
p_s(y) \ne p_t(y)
$$

## Derivational Generative Models

A derivation is a tree of functions which derives some element $z = <x, y> \in \mathcal{X} \times \mathcal{Y}$.

## Compositional Structure Learner

We formalize the CSL model using QCFGs. Generate input-output pairs at the same time. Allows one to many alignment between nonterminals.

Train a generative model based on the grammar.

We factorized the probability of derivation in terms of conditional probabilities of sequentially expanding a rule from its parent.

Let $r$ denote the rule expanded from $r_p$. We assume conditional independence:

$$
p_{\theta}(z) = \prod_{r, r_p, i \in z} p_{\theta}(r|r_p, i)
$$

Factor the distribution into latent states representing parent-rule application contexts.

$$
p_{\theta}(r|r_p, i) = \sum_{s \in S} p_{\theta}(r|s)p_{\theta}(s|r_p, i)
$$

Where $p_{\theta}(s|r_p, i) \propto e^{\theta_{r_p, i, s}}$ and $p_{\theta}(r|s) \propto e^{\theta_{s, r}}$.

You want to find a MAP estimate based on some prior that encourages compositionality:

$$
\arg \max_{\mathcal{G}, \theta} p(\mathcal{G}, \theta) \times \prod_{x, y \in \mathcal{D}} p_{\mathcal{G}, \theta}(x, y)
$$


## Training

We might want to jointly optimize the grammar induction and weights, but we use a two stage process.

We prefer smaller grammar. Use a grammar induction algorithm.

Then when you get the grammar, train generative latent variable mdoel by minimizing the log likelihood.

This allows you to decompose trianing data into parst that can be recobmined in novel ways.

Grammar induction algorithm provides a storng inducitive bias.

Sample synthetic data and then use that to train T5.

# Results

Synthetic dataset - it is designed as a generative model but it can solve the syntehtic dataset on its own.

Induced grammar also has high coverage. This enables you to use T5 to solve SCAN and COGS.

CSL on non-synthetic tasks - CSL can only generate examples that are covered by its grammar.

There is a strong potential for using latent variable model as data generators.

Question: Isn't there a chance that you basically just genearte the test set?

 - In the case of the synthetic data, yes, that's the point.