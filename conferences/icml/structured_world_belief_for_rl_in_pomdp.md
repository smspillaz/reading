# Structured World Belief for Reinforcement Learning in POMDP

Object-centric world models provide structured representation of the scene and can be an important backbone in reinforcement learning and planning. However, existing approaches suffer in partially-observable environments due to the lack of belief states. In this paper, we propose Structured World Belief, a model for learning and inference of object-centric belief states. Inferred by Sequential Monte Carlo (SMC), our belief states provide multiple object-centric scene hypotheses. To synergize the benefits of SMC particles with object representations, we also propose a new object-centric dynamics model that considers the inductive bias of object permanence. This enables tracking of object states even when they are invisible for a long time. To further facilitate object tracking in this regime, we allow our model to attend flexibly to any spatial location in the image which was restricted in previous models. In experiments, we show that object-centric belief provides a more accurate and robust performance for filtering and generation. Furthermore, we show the efficacy of structured world belief in improving the performance of reinforcement learning, planning and supervised reasoning.

https://icml.cc/virtual/2021/spotlight/9540

[[structured_world_belief_for_rl_pomdp.pdf]]

Object-Centric temporal models give you a way to get a symbolic representation of a scene.

 - Model produces a set of vectors as opposed to a set.


Because you have a set of vectors, each vector represents one object - long term generation.

These models overlook partial observability (eg, out of view objects).

Can you integrate object centric representations with belief states into one model.

## Sequential Monte-Carlo

 - Produce a set of particles (each particle represents one hypothesis for the state of the world)

![[structured_world_beliefs_model_for_pomdp.png]]

 - Each particle associated with a particle weight - how likely does it explain the observations that you have seen.
 - In previous models having belief states is not possible - you don't keep multiple states.


Maximize the log-probability of the image sequence ($\log p(x_{1:T})$) via the AESMC ELBO objective.

$$\mathbf{L}_{\phi, psi} = \frac{1}{T} \sum^T \log \sum^K w^k_t$$

where 

$$
w^k_t = \tilde w^{a^k_{t - 1}}_{t - 1} p_{\theta}(x_t|s^k_t) \frac{p_{\theta}(s_t^k|s_{t - 1}^{a_{t - 1}^k})}{q_{\theta, \phi}(s_t^k|s_{t - 1}^{a^k_{t - 1}}, x_t)}
$$

## Experiments

Belief tracking in 2D branching sprites dataset - objects disappear  - show the position particles that are produced by the model. When objects become invisible, split the trajectories according to the multiple hypotheses that you have.
