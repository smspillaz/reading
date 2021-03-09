# SMiRL

Many RL algorithms have benefitted from entropy-regularized / novelty-seeking behaviour (eg, entropy term).

Works if the learning environment is stable, but not so great if you have non-stationarity.

## Method

Maintain an estimate of the distribution of visited states $p(s)$. Try to construct the policy $\pi$ such that we visit likely future states taht we have already visited.

Entropy-minimizing objective is a good auxiliary learning signal for unstable and unsupervised RL environments.

1. Observe states $s$
2. Compute reward under the current state model
	1. If the state is too new we don't know much about the reward - keep within our comfort zone
3. Update state model with newest observation and history
4. Sample and execute an action conditional on previous observation and state model
5. Do similar actions to the ones that you've already done

The goal is to minimize the entropy of the state marginal distribution under its current policy $\pi$ at each timestep.

$$
\sum^T H(s_t) \le - \sum^T E_{s_t \sim d^{\pi_{\theta}}(s_t)} [\log p_{\theta_{t - 1}} (s_t)]
$$

Then the reward is $\log p_{\theta_{t - 1}}$

We have to perform multiple updates on the state model before updating the policy. We also have to augment the experience with sufficient statistics. If we don't do this then otherwise the rewards that we calculate at each timestep will be biased. They augment experience with sufficient statistics of the state distributions at each timestep.

![[smirl_pseudocode.png]]

VAE:

 - For high-dimensional observations. Two modifications
	 - Don't reset the VAE as is done on line 2
	 - State model's domain is the latent space of the VAE


For each timestep we have to compute the SMiRL reward, record the states and re-fit the state model.

If you're using images it is more convenient to use some sort of nice encoding of the image. When you're using a VAE you have to use quite a lot of training data to get it working - instead of resetting the VAE (like how the experience is reset), don't reset it.

The state model domain can also be the VAE latent space.

Question: How to bootstrap? Initially all states are unfamilar?

 - Answer: We basicaly want to pick states that make it likely that we stay in the same state
 - If you pick a state where you're likely to be knocked out of it by the environment, then this is a state with high entropy and we don't want that.

Is there a reward coming from the environment? No. The SMiRL gives you an environment for staying in known states.

## Test Environments

 - Dodge fireballs
 - Dodge enemies
 - Humanoid next to a cliff

Measuring the stability of an environment:

 - Compare state distribution entropies induced by different policies
	 - Random policy
	 - SMiRL
	 - Entropy maximization


In stable environments you would expect the gap between SMiRL and random to be quite small and RND (entropy maximizing) - random > 0

In unstable environments SMiRL - random < 0 and RND - random = 0

## Results