# Challenges in Reinforcement Learning
 - Choosing actions
 - Choosing environments
 - Dynamics or not?


## MCTS

Focus the search into very promising directions. This yields very good performance.

Four stages:
 - Selection
 - Expansion
 - Simulation
 - Backprop


MCTS is limited to discrete actions.

Start in the root note. Compute value function for each action. Then pick the action with the highest values and compute those values.

Then we backprop the values.

At each node where you make a decision, you have an upper confidence bound. This estimates which action you would like to do which trades off between exploration and exploitation.

### Backpropagation

 - Typically what people do is take the average over all samples in a node.
 - Another possibility is max (take the action with the highest value) but there is no convergence proof for this.

These two approaches either make the tree wide or deep.

We want something-between - we want something that looks far but still converges.

"Power mean":

$$
\bar X_n(p) = \frac{\sum^K \frac{n_i}{n} \bar X^p_{i, n_i}}^{\frac{1}{p}}
$$

For $p = 1$ corresponds to average. For $p \to \inf$ corresponds to max.

Prove that for any finite $p$, the algorithm converges to the optimal solution.

## Self-paced Curriculum RL

Requirements:
 1. Principled
 2. Automatically converge from easy to hard tasks


Example: Ball and net. Where does the ball come from? Easier if you throw directly into the net.

We have a context - some parameters of the enviornment - desired context distribution and a starting one. We put the context variable $c$ as part of everything.

$$
\max_{\theta} E_{\mu(c)} [E_{p_c(s_0) [V^{\theta}](s)]
$$

$/mu(c)$ is the desired context distribution.


How to move the context distribution? On the top we have the optimization objective where we maximize the value function and we have a KL divergence between the current context distribution and the desired context distribution. We want to minimize the distance but maximize the value that you get in the current context.

We have a finite number of samples, we want to keep the learning stable, so we require that the learning does not jump around too much.

We want to maximize the parameters of the agent in such a way that we maximize the value function for the current context distribution. We don't necessarily change the value function parameters but the policy parameters.

Weight the KL divergence for context distributions by $\alpha$. As $\alpha \to \inf$ then we end up in the final task distribution.

### Comparison

Standard RL doesn't find any solution. Random curriculum beats that. GoalGAN works quite well.

## Questions

 - you need a lot of data right?
 - discrete case: the results are OK. Depends on the task about whether to use the self-paced learning. Discuss this with Pascal. Some new work on extending the distributions.
 - can the system learn the augmentations or the parameters of the environment? you could do model learning and learn controls for the system in low-dimensions, then use that as part of this self-paced learning
	 -       I suppose this would be like learning disentangled representations of the environment such that you can generate new instances?