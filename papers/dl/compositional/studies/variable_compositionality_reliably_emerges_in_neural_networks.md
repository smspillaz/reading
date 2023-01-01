---
title: "Variable Compositionality Reliably Emerges in Neural Networks"
---

They argue that languages that emerge between networks are in fact straightforwardly compositional, just with variation.

If you introduce a variation-based framework, then you will find that the languages emerging between networks have straightforward compositional structure.

Measures for compositionality:
 - Topographic Similarity: Measure correlation between pairwise meaning distances and edit distances between associated signals. Perfectly compositional language has score of 1
 - Residual Entropy: Eg signal encodes one and only one part of the meaning. Not all compositional languages score highly, since sparsity is only one feature of a compositional system.

Kinds of variation:
 - Unanimity (Synonymy and Homonymy): Homonymy minimized when each atom of meaning maps to a single form, Homonymy minimized when each atom of form maps to a single meaning. We want to maximize both, eg, we don't want these many-to-one or one-to-many mappings.
 - Word order freedom: Compositional languages can sometimes allow you to adjust the word order.
 - Entanglement: Consider "Went". It entangles meaning and tense together.