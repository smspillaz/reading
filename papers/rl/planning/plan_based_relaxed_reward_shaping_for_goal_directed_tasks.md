---
title: "Plan-Based Relaxed Reward Shaping for Goal-Directed Tasks."
venue: "ICLR"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/SchubertOT21"
ee: "https://openreview.net/forum?id=w2Z2OwVNeK"
url: "https://dblp.org/rec/conf/iclr/SchubertOT21"
authors: ["Ingmar Schubert", "Ozgur S. Oguz", "Marc Toussaint"]
sync_version: 3
cite_key: "conf/iclr/SchubertOT21"
---
# Plan based relaxed reward shaping for goal-directed tasks

RL with sparse rewards limited by exploration, shape reward with exploration bonus.

Potential-based reward shaping - invariance of the opitmal policy is guaranteed.

Final-volume-preserving reward shaping (ours): Allows for more general types of reward shaping functions, doesn't guarantee invariance of opitmal policy. Same long-term behaviour - after time, they end up in the same final volume. FVRS introduces a less strict notion than the complete invariance that PBRS introduces. Basically, you end up in the same place

This allows us to introduce information into reward shaping in a more direct way.

Example: Two possible paths that get to the goal. The value of the policy can depend on all states along the trajectory. Eg, you want to ascribe a higher value to Pi_2 since it comes closer to the goal region.

We compare in a plan-based setting. We have a black-box planner which provides a crude plan that cannot be executed in an open loop, but we can use it as additional information to the RL agent. Compare PBRS and FVRS

Robotic manipulation examples. FVRS increases sample efficiently significantly over PBRS. More often agents are consistently successful and become successful earlier. Improved efficiency across all examples and RL algorithms.