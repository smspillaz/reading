# What can learned intrinsic rewards capture?

Basic idea: you essentially have an RNN which learns to give the reward which is used to update the policy in the inner loop -
the process of updating the parameters for the policy don't rely on the task-specific reward, but only the
intrinsic-reward given by the RNN

The paper posits that the intrinsic rewards server as helpful signals to improve the learning
dynamics of the agent (so that on a familiar task, even in a different action space, you
know what to give "intrinsic" rewards for).

Proposes a gradient based method for defining a parameterized intrinsic rewards function.

"Lifetime return": Discounted return over a set of episodes for a given task. Start at
a randomly initialized policy for a given task, use the intrinsic reward function to give
a reward to the agent during the task. Use the lifetime return to compute
the "lifetime return" over the extrinsic rewards, try to maximize this.

This allows for exploration across multiple episodes (eg, the best strategy is explore) until
the point where you find something that is giving you an extrinsic reward, at which point
the best strategy changes to exploit.
