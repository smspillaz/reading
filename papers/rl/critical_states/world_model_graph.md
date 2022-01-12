---
title: World Model as a Graph - Learning Latent Landmarks for Planning.
venue: ICML
pages: 12611-12620
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/icml/Zhang0S21a
ee: http://proceedings.mlr.press/v139/zhang21x.html
url: https://dblp.org/rec/conf/icml/Zhang0S21a
authors: ["Lunjun Zhang", "Ge Yang 0003", "Bradly C. Stadie"]
sync_version: 0
---

# Planning

Simulating the future after taking a sequence of actions, then picking the actions that lead to the best actions.

Given some replay data, learn the forward dynamics.

Problem: Learned model quickly diverges from reality as model error compounds.

This is really hard in robotics beacuse:
 - Physics is complicated
	 - Non-deterministic transition functions
 - Model error compounds as planning horizon increases
 - Long-horizon planning too difficult for action-by-action rollouts if your action timestep is small



# Rethinking planning

Humans plan days or months ahead and don't plan every single action to take.

We are able to break down a long-term plan into a todo list that has much shorter horizon goals.

A missing piece in planning is the ability to analyze the structure of a problem and decompose it into subproblems.

## $L^3P$ - model the world as a graph

Key ingredients:
 - Plan for subgoals to reach
 - Learn world model as a graph rather than one-step forward dynamics
 - Nodes are learned in structured latent space
 - Use reachability predictions to decide when to replan. Don't plan at every other step.


![[L3P_overview.png]]

## Metric-constrained latent space:

Reconstruction loss with additional reachability term

$$\mathcal{L_{\text{rec}}} = ||f_D(f_E(g)) - g||^2_2$$

$$\mathcal{L}_{\text{latent}} = (||\mathcal{L_{\text{rec}}} - \frac{1}{2}(V(g_1, g_2) + V(g_2, g_1)))^2$$

The last term is the reachability term.

How to obtain the reachability estimates? Use Q-learning with HER.

$$Q(s, a, g) = \sum_t^{D(s, a, g} \gamma^t \cdot -1 + \gamma_{t = D(s, a, g)} \gamma^t \cdot 0 = -\frac{1 - \gamma^{D(s, a, g)}}{1 - \gamma}$$

Where $D$ is the number of steps it takes for the agent to reach the goal from the current state after the action is taken.

$V$ is the number of steps it takes for the policy to transition between the goals.

In the sparse reward setting, you get a reward of 0 at the goal and -1 at every other step.

$V$ marginalizes the actions in the function $D$. $D$ and $V$ are like the edges on the graph.


## How to obtain the nodes - clustering

If we do clustering in the reachability-constrained latent space, then the goals that are reachable from one and other will be grouped together. The nodes on the graph will be the centroids in the latent space.

## Online planning

Leverage temporal abstraction.

1. Propose landmarks with graph search
2. Estimate steps it will take to get to the subgoal
3. Keep the goal fixed for this many actions
4. Regardless of whether you meet the goal, run the graph search again and remove the immediate previous goal from the list.

# How well does it work?

Can you solve long-horizon tasks by stiching together simpler goals. Can you apply it to robotic manipulation tasks?

On the point-maze and end-maze tasks - during training, initialize positions and goals are distributed uniformly. During testing you have to traverse one end to another in the maze. Eg, dynamically sitch together the simpler goals seen during training that you saw during training time. Note that this very long path is not seen during training.

Compared to prior methods, this addressed two failure modes:
 - Graph based methods tend to switch proposed subgoals quickly and tend to fall into a loop
 - When agent pursues subgoal unsuccessfully, other methods tend to get stuck by proposing the same subgoal whereas L3P proposes a different subgoal.


# Ablations

Online plnaning module is important since graph is more sparse and compact.

L3P is robust to number of learned landmarks.

For graph search, replacing hard-min with soft-min improved stability.

Common-trick: Once distance is above a certain thershold, set it to infinitity.

For now, only able to handle *static* environments.
