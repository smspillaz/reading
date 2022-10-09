---
title: "Fast and Slow Learning of Recurrent Independent Mechanisms."
venue: "CoRR"
volume: "abs/2105.08710"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2105-08710"
ee: "https://arxiv.org/abs/2105.08710"
url: "https://dblp.org/rec/journals/corr/abs-2105-08710"
authors: ["Kanika Madan", "Nan Rosemary Ke", "Anirudh Goyal", "Bernhard Sch\u00f6lkopf", "Yoshua Bengio"]
sync_version: 3
cite_key: "journals/corr/abs-2105-08710/Madan/2021"
---

A learning agent interacting with its environment is likely to be faced with situations requiring novel combinations of existing pieces of knowledge.

Decomposition is particularly relevant here for generalizing in a systematic way.

Main idea: Attention mechanism dynamically selects which modules can be adapted to the current task and we train the parameters of the selected modules quickly. The attention mechanism is a meta-parameter, specifying what to learn.

Results: Achieve faster adaptation.


![[meta_rim_architecture.png]]

The main idea is that you update the top-k modules in the inner loop. Input Attention and Communication Attention are in the outer-loop as meta-parameters.

The inner network is based on [[rim]].

# Architecture

There are two training loops. Concatenate several episodes to form a long sequence. On every time step, a subset $k$ of $N$ modules is leant over a shorter timespan, whereas the attention mechanisms between the modules which define connectivity and sparse communicaiton are learnt over logner timespans.

Input Attention: At every timestep, do sparse attention to figure out the top-k modules.

Communication Attention: Activated modules can read contextual information from othre modules, while non-activated modules are unchanged.

## Meta-Learning

The individual modules are learned quickly, the attention mechanism which defines how they communicate is learned slowly.

# Experimental Results

On GoToLocal, metaRIM gets to a high level of return after about 100k frames, compared to RIM at 200k frames and "vanilla LSTM" at 400k frames.

## Generaliation Reuslts

This is generalization from "easy" environments to "hard" environments.

![[meta_rim_generalization_experiment.png]]

What they mean by generalization here is "length generalization". On the "more difficult" environment, the zero-shot success rate goes from 1.0 to 0.45.