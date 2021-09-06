# Vector Quantized Models for Planning

Recent developments in the field of model-based RL have proven successful in a range of environments, especially ones where planning is essential. However, such successes have been limited to deterministic fully-observed environments. We present a new approach that handles stochastic and partially-observable environments. Our key insight is to use discrete autoencoders to capture the multiple possible effects of an action in a stochastic environment. We use a stochastic variant of Monte Carlo tree search to plan over both the agent's actions and the discrete latent variables representing the environment's response. Our approach significantly outperforms an offline version of MuZero on a stochastic interpretation of chess where the opponent is considered part of the environment. We also show that our approach scales to DeepMind Lab, a first-person 3D environment with large visual observations and partial observability.

[[ozair_vector_quantized_models_for_planning.pdf]]

https://icml.cc/virtual/2021/poster/9543

Model-based planning approach for partially observable environments.

AlphaGo - uses a goal simulator

muZero - removes the simulator - learns a deterministic model.

Ideally we'd like to be able to plan over uncertainty. You have to consider multiple possible outcomes in the future.

Handle multiple opponents with unknown or complex action spaces. Other agents introduce uncertainty. Effectively the environment becomes non-stationary.

Uncertainty also arises from partial observability.

Plan at an abstract level like humans.

## VQ-VAE to learn latent variables for state transitions

![[vqvae_planning.png]]

VQ-VAE produces a discrete representation of each state.

The idea is to encode a sequence of states and actions into a sequence of discrete latents that you can reconstruct back into the original sequence.
 - Learn a conditional VAVAE encoder-decoder pair
 - Encoder takes $s_1, s_2, ..., s_{t + 1}$... and $a_1, ..., a_{t}$ and produces a discrete latent $z_{t + 1}$.
 - Quantizer quantizes $z_{t + 1}$ into $e_{t + 1}$
 - Decoder: Takes a discrete latent $z$ and states and actions until $t$, reconstructing at $t + 1$. So $e_{t + 1}$ represents the additional information in $s_{t + 1}$ given previous states and actions.

![[vq_vae_codebook_reconstruction.png]]

The whole point is to keep the codebook as light as possible - all the static information remains in the previous trajectory, then the information that you can't reconstruct from the past trajectory is in the codebook.

Transition model predicts values and policies at each step conditioned on the future latents representing future states.

 - Construct a planning path which comprises of a state followed by a sequence of interleaved actions and latent variables until a maximum depth is reached.
 - This is an autoregressive model - you output a policy over actions and ap oliyc over discrete latent codes and a value function.
 - Use teacher forcing.

![[vq_hybrid_planning_module.png]]

Augment MCTS with stochastic nodes.

This approach plans over the player's actions and the environment state transitions.

The basic idea is that we have a non-stationary environment. In this case there is an opponent. There are several things that the opponent *could* do and we want to explicitly rollout and plan through each of them. So eg, we learn the 7 "effects" that might happen from each state (eg, actions that the opponent takes), then we imagine what the environment looks like for each of those effects and roll-out.

Note that you have a double-step MCTS

VQ-agent performs as good as two-player muZero while only observing the player's actions.


Also something like minimax as well - you can assume that the environment takes the action which MINIMIZES your Q-function return.

![[minimax_vq_planning.png]]