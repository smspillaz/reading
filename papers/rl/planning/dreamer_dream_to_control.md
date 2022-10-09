---
title: "Dream to Control - Learning Behaviors by Latent Imagination."
venue: "ICLR"
year: 2020
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/HafnerLB020"
ee: "https://openreview.net/forum?id=S1lOTC4tDS"
url: "https://dblp.org/rec/conf/iclr/HafnerLB020"
authors: ["Danijar Hafner", "Timothy P. Lillicrap", "Jimmy Ba", "Mohammad Norouzi"]
sync_version: 3
cite_key: "conf/iclr/HafnerLB020"
---
# Dream to control: Learning behaviours by latent imagination

 - Similar to muZero and other papers which plan in the latent space.
 - Main contributions:
   - Shows how you can learn a good latent space:
     - Reward prediction
     - Contrastive estimation
     - Reconstruction
   - The policy is based explicitly on the latent space, so
     no need to control variance with value baselines
   - Can predict states from both (s_{t - 1}, a_{t - 1}, o_t)
     tuples and also from (s_{t - 1}, a_{t - 1}) (tramsition model,
     no observations from the environment).

 - Value estimation
   - $V_{\lambda}$
   - Need to estimate the value of the imagined trajectory (because we don't know what that is!)
   - Many alternatives:
     - $V_R$: Sum up rewards, ignore anything that happens in future
     - $V_N$: Estimate rewards beyond $k$ using the value model
     - $V_{\lambda}$: exponential weighting

 - Algorithm:
   - Off-policy learning
   - Use experiences to imagine trajectories
    - Predict rewards from those trajectories and the value function
    - Compute value estimates using $V_{\lambda}$
     - Update parameters of policy and value prediction networks via advantage estimation
   - Compute state from a history, compute future action from the policy and add some exploration noise.