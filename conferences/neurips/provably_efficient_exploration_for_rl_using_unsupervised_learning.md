# Provably Efficient Exploration for Reinforcement Learning using Unsupervised Learning

 - We have an Episodic MDP
 - Transition kernel and reward function


Not necessary to treat each observation as an individual state - similar observations share information. If you just take one step, what you perceive about the environment is basically the same as before.

A more ideal solution is to congregate similar observations.

Assumption: observations are generated from a small number of latent state. Latent states can be regarded as a compressed representation of the original. You cannot see the true latent, but you can see an observation of it.

Because the number of latent states are small, an ideal solution should be able to learn a near optimal policy polynomial in the number of latent states.

## Theoretical Results

A number of works have shown that there is a sample complexity in the number states. Require additional dynamics assumptions, or difficult to implement in practice.

Goal: Design exploration strategy with no additional dynamics assumptions in poly(|S|).

## RL with rich observations

Inspired by empirical successes

 - Transform observations to low-dim state
 - Use tabular RL method to generate a policy from states to actions.


Challenges:
 - No prior knowledge of the latent states (we don't know how many there are what their structure is)
 - Observation data non-trivial to gather
 - Construction abstraction while achieving efficient exploration. We have to visit each state a certain number of times.
 - We also need to learn a good policy


## Solution: Unsupervised learning oracle + tabular RL

High-level idea: simulate the process of running a tabular RL algorithm directly on the state space.

Learn a decoding function that can map observations to initial states

Apply tabular RL on decoded states to do policy iteration. As more observations are collected, the unsupervised learning oracle is able to learn more accurate decoding maps..

The framework requires no additional dynamics assumption and is PAC-learnable. Compatible with various algorithms.