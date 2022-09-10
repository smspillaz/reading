---
title: Learning to Coordinate Manipulation Skills via Skill Behavior Diversification.
venue: ICLR
year: 2020
type: Conference and Workshop Papers
access: open
key: conf/iclr/LeeYL20
ee: https://openreview.net/forum?id=ryxB2lBtvH
url: https://dblp.org/rec/conf/iclr/LeeYL20
authors: ["Youngwoon Lee", "Jingyun Yang", "Joseph J. Lim"]
sync_version: 3
cite_key: conf/iclr/LeeYL20
---
# Learning to Coordinate Manipuilation Skills via Skill Behaviour Diversification

## Background

 - Hierarchical Task Learning is nice
 - Usually different parts of an agent do different things at the same time (both hands play
   the piano simultaneously)
 - Hierarchical RL:
   - Usually you have one meta policy, and a set of low level policies such as options
   - High Level policy decides which low level policy to use
   - Options framework not flexible enough to support simultaneous activation of several
     skills all at once
 - Multi-agent:
   - Split the observation and action space into separate agents:
   - Problems:
     - Credit assignment
     - Lazy agents
     - How to co-ordinate the agents

## Proposed solution

 - Train re-usable skills for each agent in isolation
 - Recombine the skills using a meta-policy
 - Ensure that the re-usable skills we learn are diverse (eg, minimal mutual information
   with other skills)


 - Meta-policy:
    - Choose a skill to execute for each agent every T_low timesteps
    - Allow skills to be conditioned on a "variant"
    - co-ordinate many skills by manipulating the behavioural embeddings
    - behaviour embedding space is continuous