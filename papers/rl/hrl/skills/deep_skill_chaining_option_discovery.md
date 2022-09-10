---
title: Option Discovery using Deep Skill Chaining.
venue: ICLR
year: 2020
type: Conference and Workshop Papers
access: open
key: conf/iclr/BagariaK20
ee: https://openreview.net/forum?id=B1gqipNYwH
url: https://dblp.org/rec/conf/iclr/BagariaK20
authors: ["Akhil Bagaria", "George Konidaris"]
sync_version: 3
cite_key: conf/iclr/BagariaK20
---
# Option Skill Chains

## Algorithm

(1) Collect trajectories that trigger new option o_k’s termination condition
    β_ok .
(2) Train o_k ’s option policy π_ok .
(3) Learn o_k ’s initiation set classifier I_ok .
(4) Add o_k to the agent’s option repertoire.
(5) Create a new option o_{k+1} such that β_{o_{k+1}} = I_ok .
(6) Train policy over options πO .

Steps 1, 3, 4 and 5 continue until the MDP’s start state is inside some
option’s initiation set. Continue steps 2 and 6 indefinitely.

## Experiments

To make a note on the experiments, we improve from reward -1500 to -500
within about 1000 episodes.

Similar plots produced showing the initiation sets for each option.
 - Plots (c) and (d) show an option for getting from some other room
   to the room with the key
 - Plot (b) shows picking up the key
 - Plot (b), (c), (d) [bottom] show navigating to the key


In general, you get a different sub-policy for each room.

## Drawbacks

 - Dependent on good exploration

## Contributions

 - Shows how to learn the options
 - Doesn't treat options as fixed