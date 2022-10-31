---
title: "How Do Neural Sequence Models Generalize? Local and Global Context Cues for Out-of-Distribution Prediction."
venue: "CoRR"
volume: "abs/2111.03108"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2111-03108"
ee: "https://arxiv.org/abs/2111.03108"
url: "https://dblp.org/rec/journals/corr/abs-2111-03108"
authors: ["D. Anthony Bau", "Jacob Andreas"]
sync_version: 3
cite_key: "journals/corr/abs-2111-03108/Bau/2021"
---

After a neural sequence model encounters an unexpected token, can its behaviour be predicted?

Both RNN and transformer models exhibit structured, consistent generaliation in OOD contexts.

There are two models of generaliation:
 - local context model: generalization consistent with the last word observed
 - global context model: generaliation is consistent with the global structure of the input.

NNLMs tend to interpolate between thee two forms of generalization.

Noise is also a mediating factor - eg, input noise encourages global generalization, noise in the context encourages local generalization.

## Example

"The pandemic won't end children can..."

"Let him easter..."

"After we at the pizza, the pizza ate..."

How should these sentences be completed? They're all pretty low-probability. In-distribution behaviour won't tell you all that much.

## Terminology

We call $P(X_{1:n - 1})$ the global context.

We call $X_{n - 1}$ the local context.

A context is surprising if $p(X_L|X_G) \lt \epsilon$ and $p(X_L) > \tau$ for each $i$ in the sentence. Which is to say that the local contexts are high-probability, but the global contexts indicate low probability.


## Methods of Generalization

Local context model: Ignore the global context, model only next-word based on local context.

Global context model: ignore the local context, model only based on the global context.

Linear Interpolation: $\lambda p_L + (1 - \lambda) p_G$.

Log-linear interpolation: linear interpolation on a log scale.

## Experiments

Formal Languages: Genrate three determinsitic finite automata, then generate language based on these through a random walk. To generate surprising test examples, sample the random walks then append a symbol outside of the state machine.

Natural Languages: WMT News, Turku Dependency Treebank, GSD Treebank.  To make surprising examples, truncate the contexts, then sample low-probability next-tokens from a language model, as long as that token is one of the 198 most common tokens in that language.

### Metrics

To compute the generalization performance, estimate $p_L$ from bigram counts in the training set, then estimate $p_G$ from a random restart of the model $p_{\text{LM}}$, using one step of beam search with beam size 15.

They expect that if a trained model performs well on in-distribution validation, then $p_{\text{LM}}(v, X_G) = p(v|X_G)$ and $p_{LM}(X_n|X_g, v) = p(X_n|X_G, v)$.

### Models

They trained a GRU with 2 hiddens and a transformer with 4 heads, 2 layers and hidden size of 512.

### Results

What model of generalization fits the best? To measure this, you measure the probabilities given by the model and the probabilities estimated above according to the generalization model.

Results are ... mixed. In each language, the local context model is a good predictor for regular languages and english, but noot so good for Finnish and Chinese.

GRU generalization is more predictable than transformer.

### What controls interpolation?

Can the weighting between local and global context be controlled?

Noising:
 - Random token substitution
 - Hidden state dropout

### Explaining the experiments

Let say that we have some log-linear model optimizing:

$$
\arg \min -\sum_{X_{1:n}} \log p(X_n|x_{1:n-1}) + \lambda ||\theta||^2
$$

If we suppose that any model with only local or global features are worse than this model:

$$
\mathbb{E}|p(X_n|X_G, X_L) - p(X_n|\tilde{X})| \lt \epsilon
$$

eg that for training $\tilde{X}$ is $X_G$ or $X_L$, then in a surprising context, $p(x_n|X_{1:n - 1})$ can be approximated by $\tilde{p}(X_n|X_G) \tilde{p}(X_n|X_L)$, eg, the product of the conditionals.