# Treating RL as a black-box optimization problem

$\tau$ - sequences of states and actions $(s_0, a_0, s_1, a_1, ..., s_H)$

$G(\tau) = \sum^{H - 1} \gamma^h r(s_h, a_h)$ - sum of all rewards that you
accumulate - early rewards worth more than later rewrds.

$J(\theta) = V^{\pi_{\theta}}$ - if we don't know what's in J, we've lost
a lot of information about the problem. Exploiting the structure of J can
result in faster algorithms with better convergence properties.

Optimization as an iteractive procedure:

 - $\theta_{t + 1} = \theta_t + \eta \triangledown_{\theta} J(\theta_t)$
 - This function will eventually converge to a stationary point (gradient = 0)
 - In expectationm, the gradient norm will follow the inequality:

   $$E[||\triangledown J(\theta)||] \le C_1 \frac{C_{\text{curv}}}{N} + C_2 \frac{\sigma}{\sqrt{N}}$

 - take-away: curvature is a limiting factor at first, then noise becomes an issue.
   - the first term depends on the curvature - after N steps the constant will
     be some constant times another constant depending on the curvature
   - the second term is the noise of the problem
 - early on, the curvature term dominates the inequality
 - but for large values of $N$, the noise is what slows you down.


Why does curvature hurt?

 - $J(\theta) \approx J(\theta_t) = (\theta - \theta+t)^T \triangledown_{\theta} J(\theta_t) - \frac{1}{2\eta}||\theta - \theta_t||^2$
 - Notice that we're making a linear approximation of the function - we do
   not fully trust the approximation.
   - the divergence term ($\frac{1}{2\eta||\theta - \theta_t||^2$)
   - The divergence term means that we make a small move
   - We do not trust the linear approximation
   - How accurate our approximation is dependso n how much the derivative changes

 - If we can bound the speed at which our gradients change:
   $$||\triangledown_{\theta} J(\theta) - \triangledown_{\theta} J(\theta')|| \le L||\theta - \theat'||$

 - Then we know that:

   $$J(\theta) \ge  J(\theta_t) = (\theta - \theta+t)^T \triangledown_{\theta} J(\theta_t) - \frac{L}{2}||\theta - \theta_t||^2$$

   - From the equation above

 - So $\theta_{t + 1} = \theta_t + \frac{1}{L}\triangledown_{\theta} J(\theta_t)$
 - The faster the gradients move, the bigger the L and the smaller the stepsize
   we can use.
 - Issue: the gradients might change much more in one direction than other.
   - Gradient descent might oscillate on the surface, even if you're converging
     reasonably along the x-axis.

 - Newton method: Move more in directions where the gradient doesn't change
   qucikly - use $\frac{1}{2 \eta} (\theta - \theta_t)^TH(\theta - \theta_t)$
   - Use the hessian to inform the divergence the quality of the linear approximation

   - Interesting fact: $\theta' = H^{\frac{1}{2}}\theta$
   - Changing the divergence equivalent to changing the representation
   - A good divergence is one where the curvature has nice properties.

 - Mirror descent: Replace divergence with $D$ - bregmant divergnce - distance between $\theta$ and $\theta_t$
   - Each distance function $D$ gives you a different convex opt algorithm

Reasoning with policies:

 - So far we've reasoned with parameters so far.
 - We probably want our divergence to be in terms of the induced policies.
 - One thing we can do $\P_{\theta}(\tau) = \mu(s_0) \Prod^H \pi_{\theta}(a_h|s_h)P(s_{h + 1}|s_h, a_h)$
   - Regualrize the optimization by $\frac{1}{2\eta} KL(P_{\theta_t}|P_{\theta})$
   - So if there are different parameters, but they lead to the same trajectories
     then they have a distance of 0.

 - No closed form solution
   - Replace KL with quadratic approximation (TRPO / NPG)
   - Use a better approximation to do multiple optimizations steps (PPO).
   - Inner/outer loop algorithm.


Natural Policy Gradient:

 - Taylor Expansion of KL: $(\theta - \theta_t)^TF(\theta_t)(\theta - \theta_t) + o(||\theta - \theta_t||^2)$
   - No first order term, because the mimima at $\theta = \theta_t$ is zero.
   - The $F(\theta_t)$ matrix is the "fischer information matrix"
 - Gives $\theta_{t + 1} = \theta_t + \eta F(\theta_t)^{-1} \triangledown_{\theta} J(\theta_t)$
   - Newton update, but you place the hessian with the fischer information matrix.
   - F is positive semidefinite
 - This is NPG

Replacing penalty with constraint:

 - Equivalance between penalized problem and constrained optimization problem
   - Correspondance between $C$ and $\eta$ is complicaetd
 - In practice, solve the problem with a fixed $\eta$, then $C$ can drift
   - $\theta_t + \etaF(\theta_t)^{-1}\triangledown_{\theta} (\theta_t)$
   - Use line-search to find parameter $\eta_t$ such that the constraint is satisfied.
   - Being able to adjust the length of the update at each timestep is a huge benefit.
 - This is TRPO

Replacing linear approximation with another approximation:

 - We don't want a function that's linear in terms of parameter, rather one that
   is linear in terms of policies
 - From $\theta$-linear to $\pi$-linear
 - $J(\theta) = J(\theta _t) + \sum_{s, a} d^{\theat}(s) \pi(a|s)Q^{\pi_t}(s, a)$
   - $d^{\theta}(s)$ is the stationary distribution induced by $\pi$
   - If you want to improve this quantity, you have to take the derivative
     with respect to $\pi$ - but $d^{\pi}(s)$ has a tricky derivative.
   - Replace the stationary distribution with $d^{\pi_t)$ - assume that it does not
     change

 - Sample actions from $\pi_t(a|s)$ - need a stationary distribution, so sample from here
 - Use importance ratio $\frac{\pi(a|s)}{\pi_t(a|s)}$
 - Clipped to prevent poor estimation
 - This is PPO

Deterministic policies:

 - Going back to the convergence rate: they depend both on the curvature and the noise
 - But the signal-to-noise ratio of determinstic policies is very small
 - Noise is an issue in two ways:
   - If your policy becomes deterministic, $\sigma$ grows to infinity
   - When you sample trajectories according to the current policy, you're going to
     sample the same trajectory over and over again. So the probability that you
     sample something else is quite small, meaning that when you do, you make
     a massive update in parameter space to account for that.
   - Second order methods can't address this because they strink the update when
     the curvature is large and boost it when the curvature is small.
   - Must prevent the policies from going near the boundaries. Add curvature to the
     loss function.

Ways to add curvature near boundaries:

 - Add entropy $H(P_{\theta}) = -\sum P_{\theta}(\tau) \log P_{\theta}(\tau)}$
   - Only has a small effect, does not prevent the policy from going to the boundary
   - Difference between entropy of uniform policy and deterministic policy is finite
   - If the expected return of the deterministic policy is big enough, it will outweigh
     the entropy term
 - KL term - $P(\theta_t||P(\theta))$ - at each step, prevent KL from being too big,
   prevents you from moving too much towards one
 - $KL(P_{\theta_0}||P_{\theta})$: log-barrier
   - The first term in the KL is a fixed policy, $P_{\theta}$ can never become
     a deterministic policy because then the term becomes infinity.

How to counteract the variance?

 - Getting the true gradient can be difficult
 - Stochastic estimates of the variance
 - You want the sigma to be as small as possible

   - Mini-batch gradient descent - sample multiple trajectories instead of
     one in order to minimize the variance.

 - Control variates:
   - We want to estiamte $E_{\xi}[\triangledown_{\theta}J(\theta, \xi)]$ from some samples
   - Lets say we know $E_{\xi}[z(\xi)]$ - introduce another random variable
   - Then $\triangledown_{\theta}J(\theta, \xi_i) - z(\xi_i) - E_{\xi}[z(\xi)]$
   - Lower variance if $z(\xi_i)$ is positively correlated with $\triangledown_{\theta}J(\theta, \xi_i)$

Stochastic variance reduction methods:

$\theta_{t + 1} = \theta_t - \alpha(\triangle_{\theta} J(\theta, \xi_i) - g_i + \frac{1}{N} \sum g_j)$

 - So we have some $g_i$ that we stored in memory
 - Store the last computed gradient for each datapoint in memory
 - This thing here has a zero-mean
 - These are as fast as the batch method if we know the true gradient.
 - Sigma goes to zero faster enough that the rate is fast enough.

Control variates in RL: baselines:

 - A baseline is some term that we add to the Q function and you want it to
   be positively correlated with your Q function
 - Replace $Q^{\pi}(s, a)$ with $(Q^{\pi(s, a) - z(s))$
 - Carefully chosen baselines can help, but choosing a baseline is an open question

Conclusion:

 - PG gradients can be tackled as a pure optimization problem
 - Curvature: careful choice of the parameterization can help
 - Entropy and relative entropy can add curvature
 - Baselines are helpful to deal with noise, but there are more powerful tools
   which will be presented later.

# Reducing the variance and connection to value-based methods (4:13)

https://neurips.cc/virtual/2020/protected/tutorial_7cebd0178b69b2e88774529e1e59a7b0.html

Variance is problematic in PG, even if the obejctive is well-behaved, the returns
can have high variance.


Assume that we get on-policy samples. Run the policy, collect trajectories,
weight actions according to what the policy did.

## What are the sources of variance

 - From state sampling
 - From action sampling
 - From sampling returns from a state

## Strategies to mitigate variance


State sampling:
 - $g(\theta, s) = \sum  Q^{\pi}(s, a) \triangledown \pi(a|s)$
 - Simple idea: use a mini-batch, where average $g(\theta, s_i)$ for multiple $s_i \sim d_{\pi}$
   - Keep a replay buffer and use a minibatch update rather than one update from
     each step.
   - Note: When you sample from a buffer its not really giving you states from $d_{\pi}$

Action sampling:
 - Assume that we sample actions according to $\pi$
 - The stochasticity is from the fact that we sampled this action
   - Idea: Remove stochasticity by just summing over all actions:
   - $\sum_a \pi(a|s)Q^{\pi}(s, a) \triangledown \ln \pi(a|s) = \sum Q^{\pi}(s, a) \triangledown(a|s)$
   - We may not have access to $Q^{\pi}$
     - If so, we cannot consider all possible actions

 - More typical strategy: baseline

   - $z(s, a) = b(s)\triangledown \ln \pi(a|s)$
   - To get a gradient estimator, subject $b(s)$ from $Q(s, a)$
   - why does this make sense? this control variate z is unbiased in expectation
     across all the actions
   - the control variate should be correlated with our estimator.
   - the expected value of the random variable is zero.


 - What baseline gives minimum bias?

   - Solve $\min_{g_j} \sum \text{Var}[g_j(\theta, s, A) - z_j(s, a)]$
   - $b^*(s) = \frac{\sum_j \sum_a Q^{\pi}(s, a)p^2_{ja}}{\sum_j \sum_a p^2}_{ja}$
   - where $p_{ja} = \frac{\partial}{\partial \theta_j} \pi(a|s)$
   - There are some algorithms out there that use this baseline
     - better to use a baseline that corresponds to the advantage function $Q^{\pi(s, a) - V^{\pi}(s)$

Return Sampling:

 - The returns for a trajectory can be high variance
 - Idea: Estiamte $Q^{\pi}(s, a) = E[R(\tau)|S = s, A = a]$
   - $\hat Q(s_l, a_l)$ can be high variance
   - Replaces $R(\tau)$
     - Natural choice is to look at the returns
 - Option 1: Other idea: Directly approximate the action-values by
   using policy-evaluation methods
   - SARSA, expected-SARSA
   - Sample an action $a' \sim \pi(\cdot|S')$
     - $w = w + \alpha(R + \gamma q_w(S', a') - q_w(S, A)) \triangledown q_w(S, A)$
   - Expected SARSA:  replace $q_w(S', a')$ with sum over all policy-weighted actions:
      - $\sum_{a'} \pi(a'|S') q_w(S', a')$
      - No point in sampling the next action and the next state.
        Slightly lower variance.
 - Option 2:
   - One-step returns: $\hat Q(s_l, a_l)  = R_{l + 1} + \gamma v_w(S_{l + 1})$
     - This estimator is stochastic
     - Approximate value function $v_w(s) \approx V^{\pi}(s)$
     - Estimate values using temporal difference learning.
   - Original actor-critic uses this section option. Baseline is $v_w(s)$
 - Option 3: n-step returns
   - Take $n$ rewards, then bootstrap using value estimate of state at $n$ steps
     ahead.
   - Original actor critic uses $n = 1$
   - Can define n-step TD error. We can update the value function using an n-step return.
 - Option 4: Averaging n-step returns: We can average over many n-step returns
   - Eg, average 1-step, 2-step, 3-step, 4-step etc returns.
   - Weight all the returns proportional to some $\lambda$ that decays.


OK, how do we pick amongst these options? (Return sampling)

 - Goal: reduce the variance of the gradient estimator
 -  The gradient estimator would introduce bias
 - Different options result in different bias and variance properties

 - Direct approximation is effectively a 0-step return:
   - Zero variance, high bias if $q_w(s_l, a_l)$ is inaccurate
 - 1-step return:
   - Low variance, but potentially high bias due to inaccuracy in $v_w(S_{l + 1})$
 - n-step returns: More variance, but less bias depedending on $n$
   - If $n > $ episode length, then $\hat Q(s_l, a_l)$ is just a sample of the return


Updating $v_w$

 - Estimator $Q^(s_l, a_l) = R_{l + 1} + \gamma v_w(S_{t = 1})$ uses a given value estimator $w$
   - Value estimates should be independent of your reward in the current trajectory
 - Bad outcome:
   - We perfectly fit $v_w$ using a trajectory sampled under $\pi$
   - If we use that exact same trajectory for our policy updates, then our
     update is zero, because we have $r$ minus some baseline.

## Off-policy learning

## Data re-use for mini-batch policy updates

 - Why are value-estiamtes inaccurate?
   - Arises from function approximation, insufficient samples
 - Reduction in bias:
   - Improve the approximator
   - Update with as many samples as you can

 - More powerful function approximators will have less bias, but need more data.
   - We need to be as sample efficient as possible with the data we do see.

 - Data-re-use:
   - Store all observed data and extract as much as possible from it
   - Problem: old-data is under a different policy. Updates are going to be off-polciy.

 - Is off-policy a problem?
   - You can use the old data to update $q_w$ and $v_w$ - use expected SARSA in a minibatch.
   - Update $v_w$ using TD-learning
     - store the probability of what taking the action was when we took
       that action
     - divide our the probabilities - importance sampling ratios

 - If off-policy an issue for values?
   - TD methods known to have divergence issues.
   - Divergence can occurr if we do not correct the state distribution
      - Implicit weighting is given by state distribution in replay buffer
      - $d$ is not equal to the on-policy state distribution
   - Eg, as the policy changes, the states that you are likely to visit
     also change.
   - Fix: Use prior corrections: If the problem is that the state distribution
     is wrong, fix that using importance sampling

Prior corrections:

 - We reach some state $s$ from a behaviour $b$
 - Re-weight the TD-update: $w = w + \alpha \rho_t \delta_t \delta_w(S_l)$
    - Adjust action probabilities back to $s_0$.
 - Too much work!

 - Practical alternatives:
   - Gradient TD-methods provide convergence wihout needing prior corrections
   - Emphatic TD-methods
   - Just use more powerful function approximators

Data re-use: opens up other variance redution strategies for the gradient estimator

 - Can re-use old data to sample the policy update
 - Benefits:
   - Reduce variance in update using mini-batches
   - Increase the number of updates (replay)
   - But this is off-policy!

 - Common approach to use replay: Ignore state weighting
   - Sample states from the buffer
   - Sample action
   - Implicit state weighting $d$ is not $d_{\pi}$ - bias!

 - One could argue that the bias in the gradient estimator is not such a big deal
   - Each gradient estimate is transient anyway
 - An Off-Policy Gradient Theorem using Emphatic Weightings
  - When you use a biased gradient and you sample the wrong state distribution
    you can get really poor solutions.
  - Depends on the problem!

