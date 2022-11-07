---
title: "Constraint-based graph network simulator."
venue: "ICML"
pages: "18844-18870"
year: "2022"
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/RubanovaSPB22"
ee: "https://proceedings.mlr.press/v162/rubanova22a.html"
url: "https://dblp.org/rec/conf/icml/RubanovaSPB22"
authors: ["Yulia Rubanova", "Alvaro Sanchez-Gonzalez", "Tobias Pfaff", "Peter W. Battaglia"]
sync_version: 3
cite_key: "conf/icml/RubanovaSPB22"
---

Many traditional simulation systems model the constraints of a system then select a state which satisfies the constraint.

In this paper, they have a framework for constraint-based elarned simulation, where a scalar constraint function is implemented as a GNN, then future predictions are computed by solving the optimization problem defined by the learned constraint.

What's nice about this is that you can improve simulator accurracy by just "thinking" more.

Example:
 - Bowling ball alley
	 - Explicit foward integration model
	 - Ball and pin cannot be in the same place at the same time
	 - Energy and momentum must be conserved

CGNS - is a future state consistent with the current and previous states?

Learned simulator semantics: You have some simulator which maps $X_{<t}$ to $X_{t + 1}$. Then the predictor takes $X_{<t}$ and returns $Y$ which represents the system's temporal evolution.

Constrainted-based GNS: Predictor iteratively solved for $\hat Y$ to satisfy a constraint function $f_c$ using $\triangledown_Y f_C$.

Instead of predicting the desired state directly, the simulator uses a differentiable constraint function $c = f_C(X_{<t}, Y)$, where $c$ quantifies how well $Y$ agrees with $X_{<t}$. The main idea is that you have a solver which finds $Y$ such that $c$ is maximal, then update the simulator using the solved $Y$.

$f_C$ is a trainable neural network with non-negative scalar output.

Graph: Don't explicitly provide positions. Include only velocity and static properties. The edges provide relative displacement vectors

Generalization: To larger systems, eg a longer rope with more nodes.

Loss: Predicted update from the last solver iteration and the corresponding ground truth update.