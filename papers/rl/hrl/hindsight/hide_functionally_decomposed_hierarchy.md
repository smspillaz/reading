---
title: Learning Functionally Decomposed Hierarchies for Continuous Control Tasks With Path Planning.
venue: IEEE Robotics Autom. Lett.
volume: 6
number: 2
pages: 3623-3630
year: 2021
type: Journal Articles
access: closed
key: journals/ral/ChristenJAH21
doi: 10.1109/LRA.2021.3060403
ee: https://doi.org/10.1109/LRA.2021.3060403
url: https://dblp.org/rec/journals/ral/ChristenJAH21
authors: ["Sammy Christen", "Luk\u00e1s Jendele", "Emre Aksan", "Otmar Hilliges"]
sync_version: 0
---

![[hide_arch.png]]

## Task Decomposition
 - 2-layer HRL
 - Explicit task decomposition by explicitly separating the state
   spaces in each layer
 - Different layers have different state spaces 
 - Allow for different control agents ot be transferred across hierarchies
 - Planning in 2D and in 3D
   - Receives information for planning then provides subgoal

## Planner
 - Planner input: Global information (position in space, final goal
   - MVProp: Based on value iteration and CNNs - produces a global value map
     - can't produce reasonable subgoals yet

     - attention mechanism: create a local value map around the agent
       gaussian distribution with covariance matrix parameterized by a CNN
     - agent-relative subgoals passed to the lower layer
     - we can better adapt to obstacles such as corners


## Control
 - Control layer: Learn how to reach the planner's subgoals
   - This is responsible for the low-level control to achieve the subgoals from the planner
   - Learn to blindly follow the planner
   - Control layers joined with relative subgoals which are important for generalization
     and scaling
   - Train the control layer with DDPG
   - Hindsight technqiues to deal with nonstationarity

## Testing
 - Tested on control tasks.
   - Navigation:
     - Train ant in 3D environment with sparse rewards
     - You can solve the training task
     - If you flip the layout, SOTA approaches overfit, HiDe generalizes nicely.
       - attention mask learns reachable sequence - avoid obstacles such as corners.
   - Even possible to transfer across agents.
     - Attach the planner of the goal-setting agent to the controller of the humanoid.
   - Even possible to transfer across domains.


Directions for future work:
 - Occlusions
 - Multiagent