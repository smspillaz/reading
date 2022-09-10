---
title: Learning Multi-Level Hierarchies with Hindsight.
venue: ICLR
year: 2019
type: Conference and Workshop Papers
access: open
key: conf/iclr/LevyKPS19
ee: https://openreview.net/forum?id=ryzECoAcY7
url: https://dblp.org/rec/conf/iclr/LevyKPS19
authors: ["Andrew Levy", "George Dimitri Konidaris", "Robert Platt Jr.", "Kate Saenko"]
sync_version: 3
cite_key: conf/iclr/LevyKPS19
---
# HAC (Hierarchical Actor-Critic)

Basic idea - extend on HIRO with multi-layer hierarchies

N policies in a stack.

Each of the non-worker policies proposes a subgoal to the next one.

Each policy gets a certain amount of steps to execute before it another subgoal is proposed to it.

## Learning with hindsight

Hindsight action transactions:
 - Use the subgoal state achieved in hindsight
 - Eg, manager issued subgoal A and agent navigated to B
	 - Manager pretends that issued subgoal B and learns that agent follows the direction

Hindsight goal transitions:
 - Basically relabel what the goal was for a given low-level policy trajectory.


Subgoal testing:
 - Negative reward if you propose an unachievable goal
 - Basically, when doing subgoal testing, you don't add any exploration noise - you propose a goal and let pi_0 follow it exactly
 - If pi_0 fails, then you get a penalty
 - The idea is to ensure that you don't propose too-ambitious subgoals for your timeout period