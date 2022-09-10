---
title: Contrastive Explanations for Reinforcement Learning via Embedded Self Predictions.
venue: ICLR
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/iclr/LinLF21
ee: https://openreview.net/forum?id=Ud3DSz72nYR
url: https://dblp.org/rec/conf/iclr/LinLF21
authors: ["Zhengxian Lin", "Kin-Ho Lam", "Alan Fern"]
sync_version: 3
cite_key: conf/iclr/LinLF21
---
# Contrastive Explanations for Reinforcement Learning via Embedded Self-Predictions

 => Explain why a learned agent prefers one action over another
 => Learn action values directly represented via human-understandable properties of expected features

 Motivation: How do humans explain their action preferences.
  - eg, via impact on expected future
  - I built more marines rather than saver minerals because I expect to be overtaken in the future


Generalized Value Functions to learn meaningful properties of expected future

Emebedded self-prediction, embed GVFs into a Q-network so that ation values are computed from meaningful GVFs.

To develop a sound explanation, use integrated gradient to show influence of GVF features on a preference of action A over action B.

Number of features can be large - compute minimal sufficient explanation to reduce size of explanation.

## Generalized Value Function

F(s, a) is a human understandable feature vector of state $s$ and action $a$. Gives the expected future accumulation of $F$ when folloing $\pi$ after taking $a$ in $s$.
 - Standard value function is when $F$ is the reward function
 - But you can have a more generalized value function which is an accumulation of some other features.

Idea: Use $Q^{\pi}_F(s, a) - Q^{\pi}_F(s, b)$ to explain why we might prefer $a$ over $b$.

Not "sound" because agent does not necessarily even consider GVFs in decisionmaking.

Embed the GVF into a Q-net work, so that action values/scores are directly computed from internally learned GVFs of agent's own policy.

Learn the GVF for $\hat \pi$. Combining function takes the GVF vector as input and learns the Q function. $\hat \pi$ is the greedy policy. Note that this is circular - GVF is based on policy, policy is based on GVF. Can we learn good ESP policies?

![[esp_dqn_gvf.png]]

Key idea: DQN style replay buffer with simultaneous training of GVF and DQN loss. Stop gradient of GVF before passing it to combining function, so learning to optimize the DQN loss doesn't have any impact on GVF (and instead we only update the GVF loss in hindsight).

Learns faster and more stable than the DQN agent in some domains.

![[gvf_cartpole_explanation.png]]