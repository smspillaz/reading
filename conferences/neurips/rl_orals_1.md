# Improved Sample Complexity for Incremental Autonomous Exploration in MDPs

 - Unsupervised RL and skill discovery.
 - State Space Coverage (MaxEnt)
   - Provably maximizes entropy, can't solve downstream tasks
 - "Reward-free" exploration
  - following initial exploration phase, you can compute optimal behaviour for reward
 - Incremental autonomous exploration
  - Explore a reward-free and open-ended environment and discover "controllable tasks" and master them incrementally 
  - Possibly very large, resettable - two parameters
    - explore and stop when all L-controllable states have been identified
    - L-controllable if the shortest path distance is no bigger than L
    - Expected hittting time of the policy to s
    - Find an epsilon-optimal policy.
  - Instance of goal-conditioned RL
    - Solving the problem may require an exponential number of steps
    - Might require going through noisy states
    - Cannot properly explore intermediate states
    - Focus on incrementally L-controllable staes: there is some unknown order of states such that $s_i$ is
      controllable in L steps by a policy defined only on that trajectory.
      - If you go through non-controllable states to get to a state, then that state is not incrementally L-controllable

  - For every goal states $g \in S_L$ find a policy such that it is accurate.
   - Near optimal policies.

  - DisCo: Discover and Control
    - Split into state space into three cases
      - K: states that are L-controllable
      - U: observed states
      - unobserved states
    - Phase 1: For each state in U, compute the goal reaching policies to nearby states
    - Phase 2: Sample collection: execute the goal-reaching policies for each goal state in K,
      then explore nearby states. Basically dynamic programming?
  - Sample compleixty guarantee: $O(\frac{L^5 S_{L + \epsilon} A}{\epsilon^2}$ - 5 is a branching factor
  - Can do cost-free exploration: each transition associated with a non-unit task, value function corresponds
    to expected cost.
  - Minimize the "value function".


How about when the environment is non-fixed?

 - Hi, thanks for your question! We indeed assume that the environment is fixed and doesn't change between applications of the reset actions.
   To handle non-stationarity in this autonomous exploration setting and still obtain provable guarantees, Gajane et al. (https://arxiv.org/pdf/1910.08446.pdf) recently introduced a meta-algorithm that tracks possible environment changes and uses any algorithm from the "stationary" setting as a subroutine (as such, our proposed algorithm Disco may be integrated in it). For completeness, there are also other recent works in RL settings orthogonal to autonomous exploration that are able to cope with non-stationary dynamics, e.g., Cheung et al. (https://arxiv.org/pdf/1906.02922.pdf) or Domingues et al. (https://arxiv.org/pdf/2007.05078.pdf).


# Escaping the Gravitational Pull of Softmax

(1) Softmax gravity well

 - key property: Non-uniform Lojasiewicz Inequality: Gradient dominance

 - Negative results: if we use softmax policy gradient to maximize expected reward,
   we observe that the gradients starts on a plateau and this plateau can be pretty long.
   There can be multiple plateaus. Problematic behaviours in practice.
 - Escape time: Lower bounded by constant over initial probability of optimal action.
 - Every sub-optimal deterministic policy is potentially able to attract more iterations
   - Once the iteration is attracted, the optimal action's probability decreases and
     escape time is prolonged.

(2) Softmax damping

 - Convex function over simplex, strongly convex over interior of simplex.
 - As long as the true distribution is 1-hot, then the convergence rate is slower than linear
 - Gradient information not strong enough to maintain a linear rate of convergence.

(3) Escort Transform (escort policy gradient)

 - Do polynomial normalization instead of exponential normalization
 - $\frac{\theta(s, a)|^p}{\sum_{a \in A} |\theta(s, a')|^p}$
 - This results in differences in convergence rate upper bounds.
 - Escapes from plateaus much faster.
 - We expect a linear rate ot be preserved in the gradient.

Does this work imply that we should replace softmax everywhere with the escort transformation?
 - More work is required
 - this work only considers the optimization perspective and there's a more important general
   difference in probabilistic transforms.

# FLAMBE: Structure Complexity and Represnetation Learning and Low Rank MDPs

Representation learning for RL
 - Succinct and useful transformations that allow us to solve downstream tasks.
 - Autoencoding, latent dynamics, contrastive learning

Theory of representation learning for RL
 - What does it mean to have a good representation?
  - In supervised learning: it would achieve good performance in downstream tasks
  - RL: approximate key-quantities like value function from our represenaton
 - How do learn a good representation in a provably efficient manner?

Low-Rank MDP:
 - Transition operator admits a low-rank operator
 - Embedding dimension is much larger than the state space.

 - Why?
  - Provide an easy answer to the first quesiton: for any reward the optimal policy and
    Q function are linear in $\phi(x, a)$
  - Algorithmically tractable if $\phi$ is known advance (if ground truth is embedding is known in advance)
  - Provably sample-efficient - inherently linear
  - Statistically tractable even without $\phi$

FLAMBE
 - Learn a  low-rank MDP model that universally approximates the environment
 - Uses a nonlinear funciton approximation to scale to rich observations
 - Provably sample/computationally efficient in online/exploration setting

Main Result:
 - Model-based realizability: $\Phi, \Upsilon$: parameterized by neural networks
   - Computational assumption that allows you to sample from these function classes.
 - System Identification guarantee
 - Sample complexity is polynomial in d, |A|, H, $\frac{1}{\epsilon}, \log(|\Phi| |\Upsilon|)$

In comparison with Linear MDP approaches, FLAMBE does not require that the feature map is known in advance.


Algorithm:
 - $\rho_0$ - random policy
 - For some steps $j$ to $J_{\text{max}}$
  - Use $\rho_{j - 1}$ to collect data
  - Learn dynamics using all data
  - Compute exploratory policy using $\Phi$
  - Continue to push forward till you approximate the environment.

The agent is just trying to get good coverage over the state space - then once you have a reward function
you can do policy optimization.


# On efficiency in Hierarchical Reinforcement Learning

Efficient = "statistically efficient" + "computationally efficient"

This paper:
 - RL and planning in MDPs give rise to repeating sub-problem structure
 - Model based thompson sampling algorithm exploiting that structure
 - Both statistically efficient, formalized under regret bound.

Induced subMDPs:
 - Induced by state space partition
 - MDP for each partition in the state space

Equivalent subMDPs:
 - Equivalent if there is a bijection between their state spaces
 - Through this bijection, subMDPs have same transition probabilities and reward at internal staes.

Hierarchical structure:
 - State space aprtition yields:
  - Maximum size of induced subMDP
  - K number of subMDP classes
  - D total number of exit states

Garbage collection robot:
 - You have a building
 - L rooms in the building
 - Each room divided into regions defining the robot state

Repeating subMDPs
 - L rooms grouped into K types

M: max number of divided regions in a room
K number of room types
D: number of doors

Initialization:
 - Prior knowledge, planning algorithm sampling function, inference function

At each episode:
 - Sample M
 - Plan
 - Execute the plan, get a dataset


PSHRL: PSRL for HRL:
 - Posteriro sampling for Hierarchical Reinforcement Learning
  - Apply PSRL with particular kind of prior that includes only MDPs that obey hierarchical structure
  - Eg "I have not started working yet but I know which rooms have the same type"


Regret Bound:
 - If P^0 exhibits hierarchical structure with maximum states M and K subMDP classes,
 - Then we can bound the regret in terms of H, M, K, |A|T

Computationally Efficient Planning:
 - Exit profile for subMDP: a vector that assigns a real number of each exit state
 - Summarizes outside structure
 - Induced policy can be viewed as an option from the start state.

Plan with Exit Profiles:
 - Options induce a high-level MDP
   - State space: start states and exit sates in all subMDPs with cardinaltiy O(D)
 - Plan with exit profiles
   - Input MDP
     - Step 1: option generation based on exit profiles
     - Step 2: plan with options in the high level MDP

# Finite Time Analysis for Double Q-learning

Double Q learning- overcome the overestimation issue with Q-learning
 - Max sampled Q value is greater than max expected Q value.

Contributions:
 - First infite time analysis of double-Q learning.


In Synchronous dobule-Q
 - initial Q^A and Q^B
   - with probabiltiy 0.5 update Q^A, but use Q^B to evaluate how good an action is
     even though we used Q^A to pick it.

Converges to Q^* with high probability.

Double Q-learning more suitable for high-accuracy regime - where $\epsilon$ dominates.

Proof sketch:
 - construct sequence G_q to bound $||Q^B_t - Q^A_t||$
 - construct sequence $D_k$ to bound $||Q^A_t - Q^B_t||$
 - remove conditional probability and obtain overall bound.


# Towards Minimax Optimal RL in Factored MDPs

What is a factored MDP?

 - Factor state and action spaces are factored into
 - $P(s|A)$ is the product of the state-action components
 - rewrad is the sum of action components

Many applications:
 - Hierarchical RL: subtask dependencies
 - Cooperative RL: each agent has their own transitions - goal is to maximize a joint reward

Can we design algorithms for FMDPs that are always more efficient?

 - F-EULER: matches the lower obund

General procedure of otimistic model-based RL:
 - Estimate transition
 - For step $h$ $H$, compute UCB by value iteration
 - Execute the greedy policy

 - choice of bound $b$ - upper bound on estimation error - incorporate knowledge of the factored structure.

Solution:
 - new bonus term
 - with correct bonus we can continue the analysis.

# Efficient Model-based RL through Optimal Policy Search and Planning

Model Learning: Should be able to distinguish aleatoric and epistemic uncertainty

Well-calibrated: Take the true dynamic inside a confidence interval.
 - True system must lie within the epistemic uncertainty bounds.
 - Set of possible models lie within the confidence intervals

Policy aspect of the algorithm:
 - We want to output a policy that can exploit the information that we have
   and at the same time explore to reduce epistemic uncertainty

 - Greedy algorithm: select a policy by maximizing expected performance (don't explore enough)
 - UCRL: Optimism in the face of uncertainty: Provably efficient - joint optimization over policies and models
   - H-UCRL: Reduction from UCRL to Greedy
   - Hallucinate control over possible models
     - Augment the space of policies with hallucinated policies
     - Then UCRL ios nothing more than a greedy planning problem


H-UCRL:
 - Starting state to a goal state
 - You get the true policy, one-step ahead uncertainty
   - Select most favorable outcome with hallucinated policies
   - Use a policy to select again the one step ahead predictions
   - Only requires one-step ahead uncertainty - we know how to recalibrate these.

# Model based Policy Optimization with Unsupervised Model Adaptation

Distribution mismatch:
 - dynamics model is learned using real data collected by old policies
 - dynamics model is generates data using *current* policy

this creates a mismatch!

Occupancy measure: Discounted distribution of states and actions

State-visit distribution

Integral probability metric: measures between two distributions.

Lower-bound for expected return.

Domain adaptation:
 - Two probability merasures, Hypothesis are all K-Lipschitz continuous for some K. Then for every $h \in H$,
we can bound the error.

Unsupervised model adaptation:
 - Align the distributions on a feature level by minimizing IMP between two feature distributions
 - Wasserstein distance loss between the two distributions learned to describe the environment.
   - Minimize IPM between feature distributions from real and simulated data.

 - Adaptation Augmented Model Based Policy Optimization:
  - Based on MBPO: Train model adaptation loss in comparison to real data distribution.

# Variational Policy Gradient Method for RL with General Utilities

RL with general utilities - problems beyond cumulative reward

 (a) exploration
 (b) risk aversion
 (c) imitation

Maximizing a policy's long term utility

 - $\max_{\theta} R(\pi_{\theta}) = F(\lambda^{\pi_{\theta}})$
 - $\lambda^{\pi}$ is the un-normalized state-action occupancy measure

Lots of general utilities that you can define over $\lambda^{\pi}$
 - Exploration
 - Imitation
 - Other stuff

Moving beyond cumulative rewards is hard - bellman equation, value function, q function
etc do not converge and all fail

is policy search still valuable ?

Can we do a policy search in the parameter space?


Policy gradient for general utilities

 - Chain rule: If you want to partial gradient with regard to $F(\lambda)$

Variational Policy Gradient Theorem:
 - $F^*% is the convex conjucate of $F$, $z$ is the shadow reward, $V(\theta, z)$ is the cumulative reward.
 - Every first order stationary solution is a global optimal solution.

Hidden convexity:
 - $\max R(\pi_{\theta}) \iff \max_{\lambda \in L} F(\lambda)$

Improves convergence rate of RL.

# Sample-Efficient Reinforcement Learning of Undercomplete POMDPs

POMDP: You only have an observation, not the whole state.


Computational barriers:
 - Planning is NP hard
 - Parmeter estimation: Estimating HMMs is harder than learning parity with noise.
 - Statistical hardness of RL in POMDPs

Why is exploration challenging?
 - Different hidden states can emit the same observation

Cannot model POMDPs as MDPs
 - Cannot treat observation as a state - it is not markovian
 - You can only view the trajectory as a state, but that's exponentially complex.

Existing works make strong assumptions for exploration.
 - Assume initial distribution covers evry state
 - Other works only consider policies that can visit every state.

Observer Operator Models:

 - Probability of observation sequence as a product of operators
 - Operator view of POMDPs

 - moments constriant: Replace probability matrices with empirical estiamtes
    - determine width of confidence set gby martingale concentration
