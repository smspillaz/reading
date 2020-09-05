# MuZero

Planning algorithms based on lookahead are good, but they require you to know the dynamics of the environment.

Doesn't work on visually rich envirnments though, best to just use model-free.

Basic idea: Predict aspects of the future that are relevant for planning. Via a recurrent process predict the
policy, value function and immediate reward. Don't need to recnostruct the original observation - hidden
states just represent whatever is relevant. Kind of like game tree search with alpha-beta pruning, except that
you use an RNN to pick a policy at each turn.

Deep RL has mostly been just about predicting the value function or optimal policy directly without any lookahead.

Formal definition:
 * Given previous hidden state $s^{k - 1}$, candidate action $a^k$ and dynamics $g(s, a) \to h \to [r^k, s^k]$, you get
   reward $r^k$ and new hidden state.
 * Compute policy and value function from hidden state.
 * Initial hidden state comes from past observations into encoder.
 * Do MTCS at each iteration:
   * Sample action from search policy
   * Store trajectory data into replay buffer.
