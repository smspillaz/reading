# Value Iteration in Continuous Actions States and Time

Classical value iteration approaches are not applicable to environments with continuous states and actions. For such environments the states and actions must be discretized, which leads to an exponential increase in computational complexity. In this paper, we propose continuous fitted value iteration (cFVI). This algorithm enables dynamic programming for continuous states and actions *with a known dynamics model*. Exploiting the continuous time formulation, the optimal policy can be derived for non-linear control-affine dynamics. This closed-form solution enables the efficient extension of value iteration to continuous environments. We show in non-linear control experiments that the dynamic programming solution obtains the same quantitative performance as deep reinforcement learning methods in simulation but excels when transferred to the physical system.The policy obtained by cFVI is more robust to changes in the dynamics despite using only a deterministic model and without explicitly incorporating robustness in the optimization

[[lutter_value_iteration_continuous_actions_states_and_time.pdf]]

[[lutter_value_iteration_continuous_actions_states_and_time]]

https://icml.cc/virtual/2021/session/12041

