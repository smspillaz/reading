---
title: Transformers are Meta-Reinforcement Learners
---

# Transformers are Meta-Reinforcement Learners

 - Transformers can handle long sequences
 - MetaRL: Infer task from a sequence of trajectories, fast adaptation strategy required


Formulate each task as a distribution over working memories. Associate them using self-attention to create at task-representation in each head.

Select the memory associated with the current timestep and feed it into the policy head.

**Transformer optimization is often unstable, espcially in the RL setting. Fix this by applying T-fixup weight initialization**.

## Related Work

 - Meta Learning: Learn inductive biases from a distribtuion of tasks , learn different components of the system like the optimizer, neural architectures, weight initializations, conditional distributions
 - Memory-based meta-learning: $RL^2$ - formulate the learning process as an RNN where the hidden state is a memory.
 - Meta-RL:
	 - PEARL: Off-policy method to learn task latents and explore via posterior sampling
	 - MAESN: Create task variables but optimize them with on-policy gradient descent.
 - Transformers for RL


## The Meta-Reinforcement Learning Problem

Define $p(M) : M \to [0, \infty)$ as a distrbution over a set of MDPs.

Sample an MDP from this distribution, with its own state space, action space, transition probabilities, rewards, initial states, gamma and $H$.

Tasks share a similar structure, but reward function and transition dynamics may vary.

Learn a policy such that during meta-testing, we can adapt the new tasks sampled from the same distribution.

## T-fixup Initialization

Use Xavier Initialization for all parameters excluding the input embeddings. Use Gaussian initialization for all input embeddings.

Scale linear projection matrices in each encoder attention block and positionwise feedforward by $0.67N^{-\frac{1}{4}}$


## Method

### Representing the task

Define a task $T(\phi)$ as a distribution oer working memories, where $\Phi$ is the space of all working memories.

Find a representaiton for a task given its distribution.

Represent each task as a linear combination of working memories sampled by the policy interacting with it:

$$
\mu_T = \sum^N \alpha_t \cdot W(\phi_t(s_t, a_t, r_t, \eta_t))
$$

where the attention weights sum to 1 and $W$ is an arbitrary liner transformation function.

Define $\phi^k$, $\phi^q$ and $\phi^v$ as a representation of the working memory at timestep $t$ i the key, value and query spaces.

So the idea is that we have query-key attention between the current working memory and past ones.

### Transformers and Memory Reinstatement

We consider the transformer to be an architecture that refines the memories over $l$ layers.

Theory: Consensus representation as the memory representation that is closest on average to all likely representations and minimizes the Bayes risk. Basically the theory is that more layers can't make you worse on average.

## Experimental Setup

**Meta Taining**: Sample a batch of tasks with the goal fo learning to learn. Run a sequence of $E$ episodes. Concatenate all the epsiodes to form one trajectory and maximize the discounted comulative reward. In this case $E = 2$ (so you only get two episodes).

**Meta Testing**: Different tasks, same distributuon as the training set. Freeze all parameters and run some epsiodes.

**Memory write logic**: At each timestep, feed networ kwith sequene of working memories

Plots on the top of figure 4 are "training tasks" and the bottom plots are "test tasks".

**Fast Adaptation**: Run meta-testing on 20 test tasks and over 6 sequential episodes. Bascially you get adaptation quickly because self-attention is "lightwieght and only requires a few working memories to achieve good performance".

**OOD**:TrMRL surpasses all baselines wit ha good margin (well, it does marginally better than $RL^2$)


## Effect of working memory sequence length

The sequence length needs to be long enough to disambiguate the task parameters