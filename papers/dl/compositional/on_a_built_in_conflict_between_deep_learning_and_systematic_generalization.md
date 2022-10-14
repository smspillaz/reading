---
title: "On a Built-in Conflict between Deep Learning and Systematic Generalization."
venue: "CoRR"
volume: "abs/2208.11633"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2208-11633"
doi: "10.48550/ARXIV.2208.11633"
ee: "https://doi.org/10.48550/arXiv.2208.11633"
url: "https://dblp.org/rec/journals/corr/abs-2208-11633"
authors: ["Yuanpeng Li"]
sync_version: 3
cite_key: "journals/corr/abs-2208-11633/Li/2022"
---

Internal function sharing is one of hte reasons to weaken OOD or systematic generalization in deep learning for classification tasks. Function sharing re-uses boundaries, meaning that you use fewer parts for new outputs.

![[built_in_conflict_dl_decision_boundaries.png]]

Lets say that you have two decision boundaries, cyan and pink.

Function sharing means that you re-use boundaies and avoid redundant ones for training predictions.

Deep learning prefers (a) over (b) because it has fewer partitions.

## Systematic Generalization

A function $f$ enables systematic generalization if $\forall(x, y) \in \mathcal{D}_{\text{test}}: y = f(x)$

Function sharing means that you merge two regions to re-use functions and avoid learning redundant functions with the same effect on the training data.

A deep learning algorithm prefers $f$ over $g$ if $f$ is more refined than $g$ and the predictions would be equal. This seems to assume that you already have $f$ and concerns whether you would have to learn $g$ as well - you won't learn $g$ if $f$ works just as well.

## Why does the conflict happen

Proposition 1: If $f(x) \not \in f(X_{\text{train}})$ then $f$ must distinguish $x$ from the training outputs. But then we could have another function $f'$ which predicts the output and keeps the prediction for other inputs.

Proposition 2: Any new output is resisted.

Conflict: For all inputs and labels in $\mathcal{D}_{\text{test}}$, $y \ne f(x)$.

### Experiments

Trained and test label combinations are mutually exclusive, but test labels for each output factor are seen in training.

Deep model architecture. $x$ is the input and $f(x) = \hat y_1$ and $\hat y_2$ are the outputs.

Layers duplicated after $h$.

