---
title: Data-Efficient Reinforcement Learning with Self-Predictive Representations.
venue: ICLR
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/iclr/SchwarzerAGHCB21
ee: https://openreview.net/forum?id=uCQfPZwRaUu
url: https://dblp.org/rec/conf/iclr/SchwarzerAGHCB21
authors: ["Max Schwarzer", "Ankesh Anand", "Rishab Goel", "R. Devon Hjelm", "Aaron C. Courville", "Philip Bachman"]
sync_version: 3
cite_key: conf/iclr/SchwarzerAGHCB21
---
# Data Efficient Reinforcement Learning with Self Predictive Representations

=> We posit that an agent can learn more efficiently if we augment reward maximization with self-supervised objectives based on structure in its visual input and sequential interaction with the environment.

=> Self-Predictive Representations: trains an agent to predict its own latent state representations multiple steps into the future

=> compute target representations for future states using an encoder which is an exponential moving average of the agent’s parameters

 =>  On its own, this future prediction objective outperforms prior methods for sample-efficient deep RL from pixels.
 => We further improve performance by adding data augmentation to the future prediction loss, which forces the agent’s representations to be consistent across multiple views of an observation

 Context: We have RL agents that can rival human performance, but data efficiency sucks.
  => Human performance evaluated after 2 hours experience on each game
  => RL agents: anywhere between several months to years of experience (500-5000x amount)


  Direct comparison: 100K steps per environment, roughly 2 hours of gameplay.

  Key points: SPR is a representation learning algorithm that augments model-free agents. Latent self-predictive transition model + optional data augmentaton.

  ## Supervised -> Self-Supervised Learning

  Move away from purely supervised learning to self-supervised. We have much richer structure compared to sparseness. We have dense training signals.

  What kind of structure?
   -> Visual nature of inputs (representations should be consistent across augmentations)
   -> Sequential interaction with environment: representatons should be predictive of what will happen in the future.

   ![[spr_data_efficient_nutshell.png]]

   SPR in a nutshel:
    -> train an agent to predict its own latent state representation multiple steps into the future using latent transition model
	-> model operates entirely in the latent space (no reconstruction) and is self-supervised (no external supervision)
	-> optionally perform data augmentation on inputs and targets, which forces agent's representation to be more consistent.

	We optimize the q-learning loss and the cosine similarity loss.

	We have a second target network which is an exponential moving average of the online encoder. Key idea: predict what latents the EMA would make .

## Data augmentation

Yarats et al: Shows that data augmentation provides a significant boost to sample efficiency.

Data augmenation is different: The data augmentations that are applied are very minor - shift images by 4 pixels.

Data-efficient rainbow as baseline.

## Analysis

Dynamics modelling is key: performance improves linearly with prediction depth.

Target encoder is necessary: Using target network with stop-gradient significantly boosts performance (0.27 -> 0.41 median HNS)

Data augmentation not strictly speaking necessarily, but needs an alternative form of noise like dropout.

