# Learning to Play Clash Royale - Oracle Planner

Why is this important?
- Useful for testing
- Practice opponents / single player versions of multiplayer games
- Design tutorials


## Clash Royale

You do very short battles by picking 8 cards from your collection. Like rock paper scissors. No single best strategy. Learning algorithms might cycle around policies without leading to better ones.

Cards have a certain elixr cost.

You can only see your own cards - you don't know what your opponent will do.

For the whole game there are like 60000 discrete actions. But only 8 cards (1-2305 actions) are valid at a time.

Partial observability: you cannot see what your opponent will do. Hard to model the opponent in that case.

Exploration is hard because if you do greedy strategy will deplete all your elixr. You need to learn how to intentionally wait for the costlier cards to become available.

## Exploration

Multi-armed bandits.

Thompson Sampling: Choose action with probability proportional to probability that you win by that action. Model it with a beta distribution. For every action maintain success/failure counts. Not the value function, just the success/failure count.

A value function used to estimate the probability of winning for both players. You can learn value functions using machine learning or use heuristics. In this work, use a simple heuristic function - tower health.

## Oracle planner

You do a small rollout and then use the heuristic to determine if you're likely in a good state.

![[mcts_clash_royale.png]]

You can do several iterations of this to find a good root node and then figure out if you want to continue.

If you have a very large branching factor you would spend a lot of time expanding the breadth of the tree instead of the depth - when you encounter a novel state you always expand for a fixed number of steps.

Oracle planner is nice but it requires a game implementation that runs faster than real time. Not really a fair opponent.

## Follower policy

Imitation learning - collect data using self-play.

This results in relatively poor performance. The follower only takes good actions in good states. Never sees bad actions.

DAgger - data collected using oracle policy, oracle planner later tells you what actions you should have taken in those states. Basically you need to go to bad states and then use the oracle planner to get out of them.

## Problem - strategy fusion

Policy is trained to predict the average of oracle actions from different states.

You're trying to match what two planners in two episodes are telling you.
