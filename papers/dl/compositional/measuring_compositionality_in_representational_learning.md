---
title: Measuring Compositionality in Representation Learning.
venue: ICLR
year: 2019
type: Conference and Workshop Papers
access: open
key: conf/iclr/Andreas19
ee: https://openreview.net/forum?id=HJz05o0qK7
url: https://dblp.org/rec/conf/iclr/Andreas19
authors: ["Jacob Andreas"]
sync_version: 3
cite_key: conf/iclr/Andreas19
---

When inputs exhibit compositional structure, eg, objects built from parts or procedures, its is natural to ask whether this compositional structure is reflected somehow in the representations.

In this paper they focus on an oracle setting, where the compositional structure of the model inputs are known, but then the only question is whether this structure is represented in the model outputs.

Contributions:
 - Formal framework for measuring how well a collection of representations reflects oracle compositional analysis of model inputs, called TRE.
 - Survey of applications
	 - How does compositionality evolve in relation to other measurable properties?
	 - How well does compositionality of representations track human judgments about model inputs?
	 - How does compositionality constraint distances between representations?
	 - Are they necessary for out-of-distribution inputs?

## Evaluating Compositionality

The speaker produces some representation of the inputs. Are those representations compositional?

Some definitions:
 - Representations
 - Derivations: We assume that labels can be labelled with a tree-structured derivation
 - Compositionality: Represntations are compositional if each $f(x)$ is determined by the structure of $D(x)$. A model is compositional if $f(x) = f(x_a) * f(x_b)$ where $*$ is *any* kind of compositional rule.

### Example

![[measuring_compositionality_example.png]]

In this example you have some inputs, a speaker which encodes those inputs and then some listener which tries to understand those encodings.

We want to know how compositional are the encodings.

Here the encodings are sort-of-composiitonal. Like 'aa' means square, 'bb' means triangle, 'xxx' means dark blue, 'xx' means blue, green is indicated by both 'zzz' and 'byy'. How compositional is it?

### Tree-reconstruction error

Choose some distance function satisfying $\delta(\theta, \theta') \iff \theta = \theta'$

Choose some composition function $*: f(\Theta, \Theta) \to \Theta$

Define $\hat{f}_{\eta}(d)$ as a compositional approximation, where $\eta$ are the parameters, such that $\hat{f}_{\eta}(<d, d'>) = \hat{f}_{\eta}(d) * \hat{f}_{\eta}(d')$

Then given some dataset with inputs $x \in \mathcal{X}$ and derivations
$d \in \mathcal{D}$, compute:

$$
\eta^* = \arg \min_{\eta} \sum_i \delta (f(x_i), \hat f_{\eta}(d_i))
$$

Then:
$$
\text{TRE}(x) = \delta(f(x), \hat{f}_{\eta}(d_i))
$$

And then for the whole dataset, the TRE score is just an average.

How well does this capture compositionality? Basically if we assume that we have some model that adjusts the parameters such that it makes $\hat{f}_{\eta}(d_i)$ as close as possible to $f(x_i)$ as possible on the *components* (eg, $d_i \in \mathcal{D}_0$, then the TRE is measuring how close your "compositional" function is to the oracle composition function.

The TRE(x) = 0 for all x if and only if $f(x) = f(x_a) * f(x_b)$.

$\delta$ and $*$ are learnable operators.


### How does compositionality tie in with learning dynamics?

Take a simple meta-learning task. Presented with two example images depicting a visual concept and then you must determine if the third image is an example of the same concept.

What's the relationship between TRE and mutual information between the parameters and the dataset? Small TRE means high compositionality.

Mutual information and reconstruction error are initially low, they both increase, then both decrease after mutual information reaches a maximum. Compression in the bottleneck framework is associated with the discovery of compositional representations.

### Compositionality and Human Judgment

How close phrase embeddigns are to the composition of their constitutuent word embeddings. Composition is vector addition and distance is cosine distance.

TRE is anticorrelated iwth human judgemnts of compositionality. Eg, less TRE means more compositionality.

### Compositionality and Similarity

Topographic Similarity: Learned representation captures domain structure if distances between learned representations are correlated with distances between associated erivations.

Representations cannot be much further apart than the derivations that produce them.

### Compositionality and Generalization

Handout some subset of object pairs at training time and evaluate generalization.

Relationship between TRE and reward. Compositional languages have lower generalization error, but they have lower "absolute" performance. Compositional langauge can often result from poor communication strategies than successful ones.

![[relationship_between_tre_and_generalization.png]]

Low TRE is not a necessary condition for good generalization.

