# Value Iteration in Continuous Actions States and Time

Classical value iteration approaches are not applicable to environments with continuous states and actions. For such environments the states and actions must be discretized, which leads to an exponential increase in computational complexity. In this paper, we propose continuous fitted value iteration (cFVI). This algorithm enables dynamic programming for continuous states and actions *with a known dynamics model*. Exploiting the continuous time formulation, the optimal policy can be derived for non-linear control-affine dynamics. This closed-form solution enables the efficient extension of value iteration to continuous environments. We show in non-linear control experiments that the dynamic programming solution obtains the same quantitative performance as deep reinforcement learning methods in simulation but excels when transferred to the physical system.The policy obtained by cFVI is more robust to changes in the dynamics despite using only a deterministic model and without explicitly incorporating robustness in the optimization

[[lutter_value_iteration_continuous_actions_states_and_time.pdf]]

https://icml.cc/virtual/2021/session/12041



## Value Iteration

Works if you have a transition function and discrete states and actions.

Continuous states and actions - you approxmiate the value function.

Hard to do this for continuous actions. You cannot solve the maximization.


## Theorem

The optimal policy can be derived if the dynamics are known and the reward function can be given as:

dynamics: $x = a(x) + B(x) u$

reward: $r(x, u) = q(x) - g(u)$

and the optimal action is given by $u^* = \triangledown \tilde g (B(x)^T \triangledown_x V)$

Basically perform gradient ascent on the value function.

$g$ defines the step size.

## Continuous Fitted Value Iteration (cFVI)

Substitute the optimal policy into the dynamics.

 - value update step: $V^{k + 1}(x_t) = r_t(x_t, u_t) + \gamma V^k (x_{t + 1})$
 - dynamics update step: $x_{t + 1} = x_t + \triangle t [a(x_t) + B(x_t) \triangledown \tilde g (B(x_t)^T Vx)]$


## cFVI algorithm

![[cfvi_algorithm.png]]

The resulting algorithm is basically:
 - Computes the N-step value function target (value function rollout)
 - Fit the value function network to the target value function
 - In the case of real-time dynamic programming, add the data of the current policy to the replay memory.


## Example

Example of the learned value function for the pendulum task

![[cfvi_pendulum.png]]

If you extend the horizon, the learning speed is much faster. But not too much because then you exploit your approximation.