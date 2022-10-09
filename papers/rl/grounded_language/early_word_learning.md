---
title: "Understanding Early Word Learning in Situated Artificial Agents."
---
# Understanding Early Word Learning in Situated Artificial Agents

## Abstract

Models must overcome challenges that infants face when learning first
words. Agent that can interpret single word instructions in a simulated world.
Proposed a novel method for visualizing semantic representations in the agent.

## Introduction

Even if there is a relatively generic architecture, this paper shows that
it exhibits various aspects of early word learning.
 * Vocabulary from different semantic classes
 * Rate of word acquisition increases rapidly after initial slow period

Proposed methods to speed up wrd learning:
 * Moderating agent's experience by curriculum
 * Auxiliary learning objective reinforcing the association between the words and replayed visual experience.

## Environment

DeepMind Lab:
 * "Find and bump into a pencil."
 * "Find and bump into any blue object."
 * "Find and bump into any striped object."

At each time step, you get pixels as input and a single word representing the instruction.

Architecture: CNN + FF Language Embedder -> LSTM with action prediction and value estimation heads (A3C).

Appears to be only one action, eg, "find and bump into an X". The critical thing here is identifying the object.

## Experiments

Reward maximized at around 500,000 episodes in the training-from-scratch case,
100,000 episodes in the pre-training case.

Word learning rate seems to increase as time goes on. Curriculum learning helps
here. (Agent is considered to have larned a word after you get a reward of 9.8/10
over 1000 consecutive trials).

Auxiliary objective on the stored trajectories helps. Agent must predict whether
memory was positive, negative or zero reward.