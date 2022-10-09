---
title: "Phasic Policy Gradient."
venue: "ICML"
pages: "2020-2027"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/CobbeHKS21"
ee: "http://proceedings.mlr.press/v139/cobbe21a.html"
url: "https://dblp.org/rec/conf/icml/CobbeHKS21"
authors: ["Karl Cobbe", "Jacob Hilton", "Oleg Klimov", "John Schulman"]
sync_version: 3
cite_key: "conf/icml/CobbeHKS21"
---
# Phasic Policy Gradient

When doing actor-critic, usually you have one feature processing network, then a policy and value head. The idea is that features trained by each objective are complimentary, so its better to let the two heads help each other.

But, there's a risk that you have competing objectives and strictly speaking, the avlue function objective is off-policy.

## Algorithm

Decouple both training objectives whilst still allowing for some injection of the learned value function into the policy network.

![[phasic_policy_gradient.png]]

 - You have a *policy network* which predicts both policy and value.
 - Then a *value network* which predicts only the value.


You have a *policy phase* and an *auxiliary phase*.

In the policy phase, optimize the training of the policy network, eg use PPO, clipping updates so that they don't deviate too much from the old policy (TRPO). Also update *value network* using MSE using the taret values calculated via generalized advantage estimation.

In the auxiliary phase, we take our sample buffer store the outcome of the policy function.

We then have a loss function for the value prediction from the policy network (where the target is the output of the value network) plus a regularization term which ensures that the updated policy diverge from the previous policy. So basically, by updating value prediction head of the policy network, we can "help" our policy prediction network learn better features offline, but we make sure to do it such that the policy head "compensates" by predicting the same distribution.

![[ppg_algorithm.png]]