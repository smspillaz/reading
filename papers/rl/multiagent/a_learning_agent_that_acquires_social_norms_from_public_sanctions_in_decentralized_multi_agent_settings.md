---
title: A learning agent that acquires social norms from public actions in decentrlalized multi-agent settings
---

Society is characterised by social norms. Introduce a training regime for multi-agent settings where all agents access "sanctioning" events but learning is otherwise decentralized.

Construct an agent architecture containing a classifier mdoule that categorizes observed beahviorus as either approved or disapproved and a motivation to punish in accord wiht the group.

Key issue that this paper is trying to solve: How to align incentives? Coordination is really hard when all agents are maximizing. Trajedy of the commons.

Critical assumption: "public sanctioning". There are discrete events when agent $i$ makes their disapproval of agent $j$ known by "punishing" them. These events are public, so everyone can learn from them.

*Classifier Norm Model*.

Agents have a private representation of the group's schema for what constitutes approved behaviour. Then you view other actors in the scene and generate a prediction for whether society at large would approve or disapprove.

# Setup

## Definitions

You have a partially observed general-sum Markov game.

At each step each player takes an action. Each player gets an observation. After the joint action, game state changes.

Extend this to include a "sanctioning observation".

## Sanctioning Observation

**Sanctioning Opportunity**: A situation where one agent can sanction another by taking an action that causes a reward or punsihment. If you punish, this is a "disapproval event"

**Approval Event**: If you have a sanctioning opportunity but *dont* punish, this is an approval.

There is a sanction-observation function that at time $t$ returns a global view of sanctioning opportunities at time $t - 1$, sancitoning decisions and context for those decisions.

## How to learn the social norms

Learn the social norm by training a classifier on the public sancitoning observations. Binary cross-entropy loss is fine.

## Learning politices

Core idea: Sanctioning should happen in tandem with the rest of the group. So if you guess that an action will be disapproved, the motivation to sanction goes up.

Each agent's own policy is a private neural network with no parameter sharing and each agenti s independently trained to maximize long-term $\gamma$-discounted return. The pseudoreward term shapes sanctioning behaviour.

# Environments where this can be applied

- Allelopathic Harvest: Berries and patches. Agents have heterogeneous tastes, eg, half the agents get double reward from red berries. Easier to eat the berries than plant them for everyone else.
- Cleanup with Startup Problem: Cleanup two types of pollution. Agents need to coordinate.

Both games contain start-up and free-rider problems. To achieve high reward you have to distribute work amongst yourselves and the work should advance the same goal.

Startup problem: No point working towards a goal if nobody else will contribute

Punishment mechanism: Zap other agents with a beam. Punishment is material - it freezes the other agent for 25 steps and applies a mark of disapproval. Getting zapped again gets you more penalty.

# Experiments

## Existence and Beneficial effects of social norms

We can learn the classifier with high balanced accuracy. The fact that you can learn to classify from a single frame means that the normative behaviour can be something like "zap if agent might compete with you"

Does CNM lead to better outcomes? Costs of norm enforcement are overcome by increased berry consumption on AH.

CNM agents demonstrate the "bandwagon" effect.

## How does CNM establish social norms?

Stabilization comes from disapproval of re-planing behaviours that would otehrwise push the system away from equillibrium.

CNM agents push further away from the center and towards the corners (good).

Second criteria: deviations away from the equillibrium should be disapproved (sanctioned).

Free-rider problem: If others are contributing, defect and slack off.