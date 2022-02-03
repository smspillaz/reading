---
title: Schema Networks - Zero-shot Transfer with a Generative Causal Model of Intuitive Physics.
venue: ICML
pages: 1809-1818
year: 2017
type: Conference and Workshop Papers
access: open
key: conf/icml/KanskySMELLDSPG17
ee: http://proceedings.mlr.press/v70/kansky17a.html
url: https://dblp.org/rec/conf/icml/KanskySMELLDSPG17
authors: ["Ken Kansky", "Tom Silver", "David A. M\u00e9ly", "Mohamed Eldawy", "Miguel L\u00e1zaro-Gredilla", "Xinghua Lou", "Nimrod Dorfman", "Szymon Sidor", "D. Scott Phoenix", "Dileep George"]
sync_version: 3
cite_key: conf/icml/KanskySMELLDSPG17
---

# Schema Networks

"A generative model for object-oriented reinforcement learning and planning"

1. Knowledge is represented with scheams (local cause-effect relationships involving one or more object entities)
2. Traverse relationships to select actions
3. Deals with uncertainty, multiple causation etc in a principled way


## Definition

1. Parse input into a list of entities $E_i$
2. All entities share a collection of attributes
3. Entity-attribute: a binary variable which indicates the prescence of an attribute on an entity $a_{i, j}$
4. Entity-state: an assignment of states ot all attributes of that entity $E_i^{(t)} = (a_{i, 1}^{(t)}, ..., a_{i, M}^{(t)})$
5. Grounded-schema: Binary variable associated wity an entity-attribute and the next timestep, depending on the present values of a set of entity-attributes. When all preconditions are satisfied, the schema is active. May predict rewards and be conditioned on actions.
6. Schema Network: A factor graph that contains all grounded instantiations of a set of ungronuded schemas over some window of time.
7. The complete state of the MDP is $s^{(t)} = (E_1^{(t)}, ..., E_N^{(t)})$


$\phi^k$ denotes the variable for schema $k$, and may be bound to specific $a_{i, j}$ values. Multiple grounded schemas can predict the same attribute through an OR gate. A schema only activates when all of its preconditions are satisfied (eg an AND gate).

So many schemas can predict one entity-attribute $a_{ij}$ but all entity-attributes bound to a schema must be active to predict that schema $\phi^k$.

An entity-attribute is active at the next timestep if either the schema predicts it to be active or its self-transition is active


## Training

Preprocess the entity states into a representation that is "more convenient for learning".

Eg, for N entities over T timesteps, we want to predict $a_{i, j}$ based on the attribute values of the $i$th entity and its spatial neighbours at time $t - 1$.

To learn the structure of the network, cast the probem as a supervised learning problem over a discrete space of parameterizations and apply a greedy algorithm that solves a sequence of linear-programming relaxations. We want to find:

$$
y = f_W(x) = \bar{\bar{X} W} 1
$$

where all the variables invovles are binary variables and $W \in \{0, 1\}^{D' \times L}$

Then we want to satisfy the following objective:

$$
\min_{W \in \{0, 1\}^{D' \times L}} \frac{1}{D}|y - f_W(X)|_1 + C|W|_1
$$

Eg, we want to minimize the prediction error with a model that is as sparse as possible. This is an NP hard problem. Greedily add schemas that have perfect precision and increase recall in prediciton of $y$.

## Transfer Learning

Schema Neworks are able to transfer to new breakout variations because they understand the rules and dynamics of the system.