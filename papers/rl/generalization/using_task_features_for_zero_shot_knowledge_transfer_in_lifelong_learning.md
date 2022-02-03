---
title: Using Task Features for Zero-Shot Knowledge Transfer in Lifelong Learning.
venue: IJCAI
pages: 1620-1626
year: 2016
type: Conference and Workshop Papers
access: open
key: conf/ijcai/IseleRE16
ee: http://www.ijcai.org/Abstract/16/232
url: https://dblp.org/rec/conf/ijcai/IseleRE16
authors: ["David Isele", "Mohammad Rostami", "Eric Eaton"]
sync_version: 3
cite_key: conf/ijcai/IseleRE16
---

Develop a lifelong learning reinforcement method based on coupled dictionary learning that incorporates high-level task descriptors to model the inter-task relationships. Using task descriptors improves the performance of the learned task policies.

Given on the descriptor of the new task, the lifelong learner is also able to accurately predict the task policy through zero-shot learning using the coupled dictionary, eliminating the need to pause and gather training data before addressing the task.

The algorithm is called "Task Descriptors for Lifelong Learning (TaDeLL)", which encods the task descriptions as feature vectors that identify each task, treating these descriptors as side information in addition to training data on the individual task.

Use *coupled dictionary learning* to mdoel the inter-task relationships.

 - Coupled dictionary learning enforces the notion that tasks with similar descriptions should ahve similar policies, but still allows discretionary elements the freedom to accurately represent the different task policies.


Task descriptors enable the learner to accurately predict the policies for unseen tasks given only their description.

## Efficient Lifelong Learning Framework

A lifelong learner encounters some task and the agen'ts goal is to learn the optimal policies for each task. Knowledge learned from previous tasks should accelerate training on each new task.

ELLA was designed to work in this framework. It assuems the parameters for each task model can be factorized using a shared knowledgebase $L$. The parameters for task $\mathcal{Z}^{t}$ are given by $\theta^{t} = Ls^{t}$ where $L \in \mathcal{R}^{d \times k}$ are the shared basis over the mdoel space and $s^t \in \mathbb{R}^{k}$ are the *sparse coefficients* over teh basis.

Then the multi-task learning obejctive for policy gradient is:

$$
\min_{L, S} \frac{1}{T} \sum_t [-\mathcal{J}(\theta^{t}) + \mu ||s^{(t)}||_1 + \lambda ||L||^2_F]
$$

where $\mathbf{S} = [s^{(1)}, ..., s^{(T)}]$ is the matrix of sparse vectors.

## Coupled Dictionary Optimization

Many multi-task and lifelong learning approaches have found success with factorizing the policy parameters for each task as a sparse linear combination over a shared basis. This means that each column of $L$ serves as a reusuable policy component represneting a cohesive chunk of knowledge. The coefficient vectors in $S$ basically tell which parts of $L$ to pick for a given policy.


We assume the same thing about the task descriptors  - we assume that the features cna be linearly factorized using a latent basis $D \in R^{d_m \times k}$ over the descriptor space.

We couple hte two bases $L$ and $D$, sharing the same coefficient vectors $S$ to reconstruct both the policies and the descriptors. Therefore for a task $\mathcal{Z}$ we have:

$$
\theta^{(t)} = Ls^{(t)}, \phi(m^{(t)}) = Ds^{(t)}
$$

To optimize the coupled bases $L$ and $D$ during the lifelong learning process, we empoy techniques for coupled dictionary optimization from the sparse coding prior work. Thus, the lifelong learning objective is reformulated as:

$$
\min_{L, D, S} \frac{1}{T} \sum_t [-\mathcal{J} (\theta^{(t)}) + \rho ||\phi(m^{(t)}) - Ds^{(t)}||^2_2 + \mu ||s^{(t)}||_1] + \lambda(||L||^2_F + ||D||^2_F)
$$

## Zero-shot transfer

Incorporating task descriptors enables the approach to predict a policy for the new task immediately given only the descriptor. Observe a data instance in one feature space (eg, the task descriptor) then infer its underlying latent signal in other feature spaces (the policy parameters) using the dictionaries and sparse coding.

Given the descriptor $m^{(t_{\text{new}})}$ we can estimate the embedding of the task int he latent descriptor space via LASSO on the learned dictionary $D$

$$
\tilde {s}^{(t_{\text{new}})} = \arg \min_s ||\phi(m^{(t)}) - Ds||^2_2 + \mu ||s||_1
$$

Since $s$ is coupled with $L$ and $D$, we can then use $s$ as a selector vector for $L$ as well to predict ap olicy by $Ls^{(t_{\text{new}})}$ .