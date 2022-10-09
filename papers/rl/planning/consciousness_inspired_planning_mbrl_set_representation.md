---
title: "A Consciousness-Inspired Planning Agent for Model-Based Reinforcement Learning."
venue: "CoRR"
volume: "abs/2106.02097"
year: 2021
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2106-02097"
ee: "https://arxiv.org/abs/2106.02097"
url: "https://dblp.org/rec/journals/corr/abs-2106-02097"
authors: ["Mingde Zhao", "Zhen Liu", "Sitao Luan", "Shuyuan Zhang", "Doina Precup", "Yoshua Bengio"]
sync_version: 3
cite_key: "journals/corr/abs-2106-02097/Zhao/2021"
tags: ["DeepMind"]
---
# Consciousness inspired Planning, MBRL with Set Representations
[[conciousness_inspired_planning_mbrl_set_representation.pdf]]

![[consciousness_bottleneck_mpc_overview.png]]

Basic idea:
 - GridWord, 8x8, agent need to navigate from one end of the world to another end of the world, not hit the lava and reach the goal state.
 - OOD: Train on starting from top and moving to bottom, test on starting from left and moving to right.

![[consciousness_planning_ood.png]]

Model idea:
 - CNN feature extraction
 - Final features are a set, as opposed to a vector
	 - Each feature vector in the set has a positional encoding attached to it.
	 - ![[consciousness_planning_feature_vector_set.png]]
 - UP (Unconcious Planner):
	 - Dynamic model: estimate $s_{t + 1}$ from $s_t$ from each action.
		 - Set-to-set prediction - copy tails on to the resulting set, forcing an order.
		 -  ![[consciousness_planning_dynamics_model.png]]
	 -  - Reward-termination estimator: maps $s_t, a_t$ to $r_t$ and $\omega_{t + 1}$
		 - Take mean of intermediate set, FC, then estimate Q values from that directly.
		 - $\omega_{t}$ - do we terminate at this state.
	 - Tree search MPC
	 - Losses:
		 - TD loss (current state value estimate to update target, distributional)
		 - dynamics consistency
		 - Reward estimation
		 - Termination Estimation (BCE loss, is this a terminating state)
 - CP (Concious planner)
	 - Same as UP, but there is a bottleneck in the attention phase.
		 - Do bottleneck by "semi-hard" attention (keeping top-k)
			 - Saved "bottleneck query" vectors
			 - Transform $S_1$ the set of objects into $K_1$ and $V_1$, then use the "bottleneck query" vectors as the query sequence, there are $k$ of them.
		 - ![[consciousness_inspired_bottleneck.png]]
		 - Expand to full $s_{t + 1}$ set by "integration"
			 - ![[consciousness_inspired_bottleneck_integrator.png]]