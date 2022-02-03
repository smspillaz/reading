---
title: Grounded Language Learning for Transfer in Deep Reinforcement Learning
venue: CoRR
volume: abs/1708.00133
year: 2017
type: Journal Articles
key: journals/corr/abs-2106-13906
ee: http://arxiv.org/abs/1708.00133
url: https://dblp.org/rec/journals/corr/abs-1708-00133
authors: ["Karthik Narasimhan", "Regina Barzilay", "Tommi S. Jaakkola"]
cite_key: journals/corr/abs-2106-13906/Narasimhan/2017
sync_version: 3
---
# Grounded Language Learning for Transfer in Deep Reinforcement Learning

Explore the utilization of natural language to drive transfer for reinforcement learning.

Learning generalized policy representations is a hard problem.

Textual environment descriptions provide a compact intermediate channel to facilitate effective transfer.

Use an MBRL based approach consisting of a differentiable planning module, a model-free component and a factorized state represnetaiton to effectively use entity desriptions. The model maps text descriptions to transitions and rewards in an environment, which should "speed up learning in unseen domains".


The environment is a 2D game with some text descriptions of the objects.

Use a [[value_iteration_networks|differentiable value iteration module]] (Tamar, Wu, etc).

The main contribution of this work is the use of environment descriptions for generalization across domains rather than generalizing across text instructions.

When talking about transfer, the agent is allowed to interact with an learn about the unseen environment, but only after it has learned about the first environment.

### Model

A represnetation generator $\phi$ and a value iteration network.

The representation network takes a state observation and a set of text descriptions as produces a tensor output. Then the VIN encoded value iteration into a recurrent network with convolutional modules.

What does the representation generator look like?

 - Each cell is converted to a corresponding real-valued vector. There are "object embeddings" (see Milkolov).
 - Description is converted int oa vector and encodd using an LSTM/BOW.
 - The two vectors are then concatenated to rpdouce a representation of the cell.


## Final Prediction

After doing the VIN on the initial representation, use a model-free action-value functon, implemented as a DQN. It is a function of the Q that comes from the VIN and the Q that comes from something else $Q_r$.



## Transfer Learning

Transfer from multiple source tasks to multiple target tasks.

- First train the model to get optimal performance on the set of source tasks.
- Then initialize am odel for the target domain. Previously seen objects retain their entity embeddings, but new words get initialized randomly.


## Experiments

 - *Freeway*: Cross a freeway while avoiding cars
 - *Bomberman*: Seek an exit door while avoiding enemies
 - *Friends & Enemies*: Twenty different non-player entities each with different dynamics and interaction. Meet all friendly entities while avoiding enemies.


Text descriptions came from AMT.

### Baselines

 - No Transfer
 - DQN
 - Text-DQN
 - AMN
 - VIN (but no text)


Studied transfer from one game to antoher.


## Discussion

Proposed utilizing antural language to drive trnasfer. Employ a model-aware RL approac htaht trie sto capture the dynamics of the environment using a VIN and a two-part state representaiton.