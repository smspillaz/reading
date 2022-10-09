---
title: "Characterizing Intrinsic Compositionality in Transformers with Tree Projections"
---
There is an apparent tension between compositional human language understanding and transformers where you can route information arbitrarily.

Develop an unsupervised and parameter free method to functionally project the behaviour of any transformer into a space of tree-structured networks. Given an input sentence, produce some binary tree that appropriates the transfromer's representation building process.

How it works: Given a string, you compute context-free representations for all spans of the string via attention masking. Use distance between average-pooled context-free and contextual representations to populate a chargt data structure.

Eg, "red apples are delicious":

 - red
 - apples
 - are
 - delicious
 - red apples
 - apples are
 - are delicious
 - red apples are
 - apples are delicious
 - red apples are delicious

Make encodings for each one.

Then we define:

$$
\text{SCI}(S, T) = \sum_{s \in T}d(v_p^{S}, \tilde v_p)
$$
(where $v_p^S$ is a vector representation of words in $S$ and $\tilde{v}_p$ is a context free representation of some span $p$.

So basically, the SCI score is the sum of distances between span represnetations and the context-free representation of the sentence.

Some proofs in the paper about how the binary tree function is an upper bound on the cumulative SCI scores.

SCI minimization provides two natural ways to measure intrinsic compositionality of $f$ on $\mathcal{D}$. You can take:

$$
t_{\text{score}} = \frac{\sum_{S \in \mathcal{D}} \mathbb E_T \text{SCI}(S, T) - \text{SCI}(S, \hat T_{\text{proj}}(S))}{|\mathcal{D}|}
$$


This measures how much is the transformer model like a tree structured model.

Then we can use COGS/M-PCFGSET problems to train the model. Basically the idea is that you want to induce a compositional structure in the transformer, then compare it against the tree-based model.

They observe the 7/8 encoders that they trained become more tree-like.