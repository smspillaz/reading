---
title: Self-supervised Visual Reinforcement Learning with Object-centric Representations.
venue: ICLR
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/iclr/ZadaianchukSM21
ee: https://openreview.net/forum?id=xppLmXCbOw1
url: https://dblp.org/rec/conf/iclr/ZadaianchukSM21
authors: ["Andrii Zadaianchuk", "Maximilian Seitzer", "Georg Martius"]
sync_version: 3
cite_key: conf/iclr/ZadaianchukSM21
---
# Self Supervised Visual Reinforcement Learning with Object-Centric Representations

https://iclr.cc/virtual/2021/spotlight/3422

Autonomous Learning has several challenges - learning is self-supervised. Observations are high-dimensional, tasks and observations are compositional. It is difficult to disentangle everything into a vector. Can you disentangle it into a *graph* or a *set* instead? If you do this, then you can use a goal-conditioned attention policy to discover new skills in relational to things that you discover in the environment.

How can we enable a robot to autonomous learn in such environments.

Prior work: self-supervised RL: Goal images, observation needs to manipulate its environment such that the environment is as close to the goal as possible.

Prior work: Use latent space, use distance in latent space as reward signal. Harder for complex tasks where objects are involved. See [[skew_fit_state_covering_self_supervised_reinforcement_learning]].

Problem: Binding problem. Even if you successfully represent many objects in one representation, hard to represent combinations if both are there.

Some dimensions encode task-irrelevant information, but they're needed for reconstruction.



Object-centric representations provide better goals. Observations and represented as a set of low-dimensional vectors. Each object representaitons can be additionaly structured. Disentangling location and appearance methods. See [[scalor_generative_world_models_with_scaleable_object_representations]] . Several other related works, in particular [[slot_attention]] 

## Contributions

 - Show that structured object-centric representations learned with generative world models can improve the performance of a self-supervised visual agent
 - Develop SMORL, an algorithm that uses those representations to discover skills
 - Even with a fully disentangled ground truth, there is a large benefit from using SMORL in environments with complex compositional tasks such as rearranging many objects.

## Related Work

1. Self-supervised visual RL: Multi-task RL problems from images without any external reward signal. Typically done with VAE ([[skew_fit_state_covering_self_supervised_reinforcement_learning]]). But if you do it this way, you might be incentivised to solve tasks that are incompatible.
2. Learning object-centric represnetaitons: See [[contrastive_structured_world_models]], [[monet_unsupervised_scene_decomposition_representation]] which don't explicitly contain features like position and scale.

## SMORL (Self-Supervised Multi-Object RL)
![[smorl_architecture.png]]
We design a novel goal-condtioned attention policy compatible with object-centric representations.

Propose an efficient self-supervised training mechanism that explores additional structure in the latent space.

We encode the observation and goal. We pick a subgoal $z_g$ from the set of possible sub-goals and provide that as an input to the goal-conditioned attention policy. Then solve for all the sub-goals.

Now as our input to the policy is a varying length-set, we have an attention-based policy. Based on multi-head attention policy where queries depend only on sub-goals and keys and values are based on the input set. This is compatible with variable-size input sets $Z$. Attends to elements that are important for sub-goal.

### SCALOR (encoder)
![[scalor_object_centric_representations_disentangled.png]]

![[scalor_architecture.png]]

See [[scalor_generative_world_models_with_scaleable_object_representations]]. SCALOR in a nutshell is a big-ol generative model.

$$
p(o_{1:T}, z_{1:T}) = p(z^{\mathcal{D}}_1)p(\text{bg}_1) \prod^T p(o_t|z_t)p(z_t^{\text{bg}}|z_{<t}^{\text{bg}}, z_t^{\text{fg}})p(z_t^{\mathcal{D}}|z_t^{\mathcal{P}})p(z_t^{\mathcal{P}}|z_{<t})
$$

Separately, if this were a graphical model:
* $p(z^{\mathcal{D}}_t)$: Latent variables of objects discovered at present step
* $p(z^{\mathcal{P}}_t)$: Latent variables of objects propagated from previous step.
* $p(o_t|z_t)$: Rendering
* $p(z_t^{\text{bg}}|z_{<t}^{\text{bg}}, z_t^{\text{fg}})$: Background transition
* $p(z_t^{\mathcal{D}}|z_t^{\mathcal{P}})$: Object discovery (new objects)
* $p(z_t^{\mathcal{P}}|z_{<t})$ Propagation of objects


The structure for object properties is defined by:
 - Prescence
 - Where the object is
 - What the object is (appearance of the object)

We estimate $q(z_{1:T}|o_{1:T})$ using variational inference by maximizing the ELBO.


## Contributions of this paper

 - Self-supervised Multi-Object RL that autonomously learns skills in compositional environments
 - Goal-codnitioned attention policy compatible with object-centric representations
 - Efficient self-supervised training that exploits additional structure in the latent space.

## Self-supervised setting

You don't have any reward signal or goals from the environment at the training stage. Agent must rely on self-supervision in the form of an internally constructed reward signal.

Self-propose some goals in the latent space and then try to achieve them. The idea is that if you have a structured latent space then those goals that you sample will be meaningful manipulations of the world.

But if you just use a VAE there might be conflicts / representational difficulty.

The reward function is:

$$
r(z, z_g) = \begin{cases} -||z^{\text{where}}_k - z_g^{\text{where}} \textrm { if } \min_k ||z^{\text{what}} - z_g^{\text{what}}|| < \alpha_i \\ r_{\text{no\_goal}} \end{cases}
$$

## Composing Independent Sub-goals during Evaluation

At evaluation time you receive a goal image from the environment, then that is processed by SCALOR to yield a set of goal vectors. Assume that subgoals are independent of each other can you can sequentially achieve them by cycling through all of them until they are solved.

## How to use SMORL

Use multi-head attention.

You have many objects that you get in your representation. Need to flexibly vary your behaviour based on the goal at hand.

We have some goal-specific query: $Q(z_g)$  . Each object is matched with the query via an object-dependent key and contributes to the attention's output via the value.

We also concatenate some other representation for object $n$ to the vectors:
 - what
 - where
 - depth





## Training SMORL
Training SMORL:

First we need to provide a feasible goals

Provide goal-dependent roal function.

Train as usual goal-conditioned RL agent.

Goal Generation:
 - Use first observations:
	 - $p(z^{\text{where}}|z^{\text{what}})$ to observed data to estimate valid location
	 - Pick random object representation
	 - Sample new $z^{\text{where}}$ from $p$ given $z^{\text{what}}$
 - Reward function for each timestep:
	 - Find most similar object: $k = \arg \min_i ||z^{\text{what}} - z^{\text{what}}_g||$
	 - Reward in a subsapce of locations: $-||z^{\text{where}}_k - z^{\text{where}}_g||$

 SMORL training combines SAC with object-centric representaitons.

 Tested the object in several multi-object environments of `multiworld` environment.

Environment has dense reward.