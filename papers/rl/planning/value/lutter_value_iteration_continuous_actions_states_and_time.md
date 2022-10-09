---
title: "Value Iteration in Continuous Actions, States and Time."
venue: "ICML"
pages: "7224-7234"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/LutterM0FG21"
ee: "http://proceedings.mlr.press/v139/lutter21a.html"
url: "https://dblp.org/rec/conf/icml/LutterM0FG21"
authors: ["Michael Lutter", "Shie Mannor", "Jan Peters", "Dieter Fox", "Animesh Garg"]
sync_version: 3
cite_key: "conf/icml/LutterM0FG21"
---


# Value Iteration in Continuous Actions States and Time


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