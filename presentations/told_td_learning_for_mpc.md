# Task Oriented Latent Dynamics (TOLD)

 - For planning we onl yneed the learned model to faciliated reward and value prediction.
 - Task-oriented representation via TD-learning.

$$
\mathcal{J}(\theta; \Gamma)= \sum^{t + H}_{i = t} \lambda^{i - t} \mathcal{L}(\theta; \Gamma)
$$

Where the loss function for the dynamics model consists of:

1. Reward loss MSE
2. Q Temporal difference MSE
3. "latent state recovery loss" $||d_{\theta}(z_i, a_i) - h_{\theta-} (s_{i + 1})||^2_2$


The polciy minimizes the negative-weighted-Q-function.

To do inference in TD-MPC, we have an outer loop and innner loop, where the inner loop updates the rewards based on the trajectory dynamics, then use the selected top-k trajectories to update the mean and sigma of the belief (cross-entropy method).

Results when using latent space consistency:

![[told_latent_space_consistency_results.png]]

How is this related to [[muzero]] and [[dreamer_dream_to_control]]?

In muZero they don't have latent space consistency loss?

The basic idea is that $h_{\theta -}$ is a target network, so basically the consistency loss helps to make the learning of the dynamics network a bit more stable.

See also [[data_efficient_rl_self_predictive_representations]].