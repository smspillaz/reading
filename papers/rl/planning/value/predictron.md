---
title: "The Predictron - End-To-End Learning and Planning."
venue: "ICML"
pages: "3191-3199"
year: 2017
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/SilverHHSGHDRRB17"
ee: "http://proceedings.mlr.press/v70/silver17a.html"
url: "https://dblp.org/rec/conf/icml/SilverHHSGHDRRB17"
authors: ["David Silver", "Hado van Hasselt", "Matteo Hessel", "Tom Schaul", "Arthur Guez", "Tim Harley", "Gabriel Dulac-Arnold", "David P. Reichert", "Neil C. Rabinowitz", "Andr\u00e9 Barreto", "Thomas Degris"]
sync_version: 3
cite_key: "conf/icml/SilverHHSGHDRRB17"
---
# The Predictron: End-to-End Leraning and Planning

Predictron: Fully abstract model represented by markov reward process which can be rolled forward
for many "imagined" planning steps.

Each foward pass accumulates internal rewards and values, ensure that the accumulated
values approximate the true value function.

General Idea: The 0th step is just model-free value function estimation (eg, v0)

The 1st step estimates v1 then adds $\gamma$ r0 at the 0th step (v1 - v0).

The $\lambda$ model does something similar, except that you have an additional
discount based on linear interpolation, so in the future the value
function estimate matters more and more and the estimated rewards matter less and less.

All that is required is that the scores of the trajectories produced by the abstract model are
consistent with the scores that you would get in the real environment.

$k$ is a hyperparameter. Depends on your task - effectively it specifies the granularity that you need to use.

# Introduction

MBRL: Learn a model and plan in the model. Use the model with a markov reward
or decision process.

Even if you can reconstruct the environment in a pixel-perfect way, turns out
this still doesn't beat model-free if you try to plan in this space.

Predictron: Integrates learning and planning in one end-to-end procedure.

In this formulation, the model is completely abstract and the only point is
to facilitate an accurate value prediction. We'd hope that there's some
correlation between being accurate and being able to plan correctly.

Train the predictron to predict many different value functions and variety
of pseudo-reward functions and discount factors.

# MRP

$s', r, \gamma = p(s, \alpha)$ where $s'$ is the next state, $r$ is the rewrad
and $\gamma$ is the discount. $\alpha$ is iid noise.

Return: Cumulative discounted reward over a trajectory.

Value function: Expected return from a state.

# Predictron Architecture

$\bold{s} = f(s)$ - something that encodes the state (eg, history of obs)
into $\bold{s}$ which is internal, hidden.

Model: $\bold{s}', \bold{r}, \bold{\gamma} = m(\bold{s}, \beta)$, maps
from one internal state to the next, predicting also internal reward,
internal discount.

Value: $\bold{v} = v(\bold{s})$ - internal return from internal state $\bold{s}$.

k-step Predictron: roll the internal model forward $k$ steps.

$\bold{g}^k - \bold{r}^1 + \bold{\gamma}^1(\bold{r}^2 + \bold{gamma}^2(...))$

$\lambda$-predictron: combines together many $k$-step pre-returns. Basically
you have a mini-neural net which computes weights for every $k$-step:

$\bold{g^{\lambda}} = \sum^L \bold{w}^k \bold{g}^k$

$\bold{w}^k = \begin{cases} (1 - \bold{\lambda}^k \Pi^{k - 1} \lambda^j \text{ if } k < K \\
\Pi^{K - 1} \lambda^j \text{ otherwise }\end{cases}$

Analagous to the forward-view temporal difference(\lambda) algorithm.

The idea is that each $\lambda^k$ weight acts as a gate on the computation
of the $\lambda$-prereturn, so $\lambda^k = 0$ will truncate at layer $k$
while $\lambda^k = 1$ will utilize deeper layers based onadditional steps of the model.
Enables the computation of adaptive depth.

# Updating the model

Minimize the sample loss of returns.

$L^{k} = \frac{1}{2}||E_p[g | s] - E_m[g^{k} | s]||^2$

Looks like this is minimizing the value function difference between the $k$-step predicted
value and the actual value function $g$.

Question: Does this mean the prereturn at each $k$ needs to be the same as the
return given $s$?

## Consistency update

Each rollout of the predictron generates a trajectory in the abstract space.

Reguarlize such that E_{m}[g^{\lambda}|s] - E_{m}[g^k|s] is close in the L2 norm.
We only update $g^{k}$ in this case, not $g^{\lambda}$.

## Experiment with planning indication

The task is to solve the maze in a certain way $g$.

Each step we show the vector we get from $w^kg^$.

I guess what this is showing is the high-value states at each timestep. So
assuming that our state vector is just the entire map, then the high-value
states are the highlighted ones.