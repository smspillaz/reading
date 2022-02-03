---
title: Parrot - Data-Driven Behavioral Priors for Reinforcement Learning.
venue: ICLR
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/iclr/SinghLZYRL21
ee: https://openreview.net/forum?id=Ysuv-WOFeKR
url: https://dblp.org/rec/conf/iclr/SinghLZYRL21
authors: ["Avi Singh", "Huihan Liu", "Gaoyue Zhou", "Albert Yu", "Nicholas Rhinehart", "Sergey Levine"]
sync_version: 3
cite_key: conf/iclr/SinghLZYRL21
---
# Parrot

 => How can we pre-train RL agents?
 => Pre-training behavioural priors captures complex IO relationships observed in successful trials from a wide range of previously seen tasks.
 => Can be used to rapidly learn new tasks without impeding exploration.


 Typically you utilize random exploration, learning to slow learning.

 Quite different from how people acquire new skills - learning to play tennis, you'd re-use skills you had already.

 Dominant paradigm: Meta-RL: Trained to maximize reward over a distribution of environments. When given a new task, maximize reward for new tasks as quickly as possible. Running large scale RL experiments take a fair bit of effort.

 What if we have access to offline datasets from previously seen tasks? The data could come from previously learned policies, human demonstrations, unstructured teleoperation of robots.

 Kind of common in CV and NLP but not RL.

 Requirements for pre-training an RL agent are different because you need to capture rich input-output relationships. Contrast to CV/NLP where you just learn good representations.

What would make a good representation for RL?

(a) Must provide an effective exploration strategy
(b) Simplify the policy learning problem
(c) Allow the RL agent to retain full control over the environment.

## Related Work

 * RL and Demonstrations: Usually you have to collect demonstrations for the specific task being learned. In this case, use data from *other* prior tasks to speed up RL for new task.
 * Generative Modelling: Several prior works:
	 * IntentionGAN
	 * InfoGAIL
	 * In this work, use behavioural prior to augment model free RL as opposed to using it for planning.
	 * Variational Autoencoders: Our model is obseration-conditioned and allows for closed-loop feedback control + is invertible.
 * Hierarchical Learning: Similarity to HRL literature, high-level policy that controls a low-level one. Shares more similarity with the options framework, but the behavioural prior is not concerned with temporally extended abstrations but rather transforming the MDP into one where potentially useful behaviours are more likely.
 * Meta-learning: Meta-learning tries to learn the learning method, this is more like transfer.


## Problem

Let $p(M)$ denote a distribution over MDPs with the constraint that the state and action spaces are fixed. Only the dynamics and reward function change.

Assume that the behavioural prior is trained on data that *structurally resembles the potential optimal policies for all or part of the new task*. Eg, if you have to place a bottle, the prior data includes some behaviour like picking up objects.

$$
M \sim p(M), \pi_M(\tau) = \arg \max_{\pi} \mathbb{E}_{\pi, M} [R_M], \tau_M \sim \pi_M(\tau)
$$
This is kind of like meta-RL, but you don't have to access any task in $p(M)$ except the task you are learnng. RL only performed on the target environment, skills come from prior environments.

## Method
 

 PARROT: Prior AccelRated ReinfOrcemenT.

 use the behavioural prior to explore effectively. Maximize reward for task of interest. Priors should execute meaningful behaviours. The basic idea is to learn invertible functions to map noise vectors to complex high-dimensionals. Comes from normalizing flows.

 The new MDP essentially transforms the original into a simpler one, as long as you share partial structure. Since the mapping is invertible, then for every environment action, there exists a point within the Gaussian distribution that maps to that action.



 Prior: Takes observatons and outputs an action that makes sense in that context. Also take noise which allows you to generate several possible valid actions. Allow you to sample from a simple distribution and transfer to a complex multimodal one.

 ![[parrot_flow.png]]

 Parameterize our prior using flow-based generative models.

 The models are also invertible - for any action, there exists some input which allows to see the situations to which applies.

 Sampling trajectories from the prior is much more effective.

 In general the way it works is that you encode an image, then condition individual transformations $f_i$ of an overall mapping $f_{\phi}$. Then sample from the distribution. The point is that you sample things which are relevant to what you observe, without directly predicting actions. The RL algorithm can tweak what gets sampled.

 When you start in the new environment, "random" exploration means doing things that were useful in other problems.

 Transforms the MDP into an easier one since random actions are transformed into ones that are likely to lead to rewards.

May be several possible useful tasks - prior may not maximize the reward for the task at hand.

![[parrot_rl_policy_input_to_prior.png]]

We have a new RL policy that produces the latent $z$ used by the prior. The invertibility property of the prior guarantees that there exists some $z$ that generates the action. So basically the RL policy generates "observations" for the prior.

Transfer the learned prior to new environments with new objects. Compare against VAE based approach in our experiments. PARROT outperforms BC + RL and prior works in hierarhical imitation and RL.

## How to learn the mapping?

![[parrot.png]]
 How can we learn a prior from data? Use generative models. Eg GPT3, autocomplete.

 Deep generative model: takes noise as input, produce actions. it can represent $p_{\text{prior}}(a|s)$ using $f_{\phi} : \mathcal{Z} \times \mathcal{S} \to A$ .

 Requirements:

 1. Learned prior should be capable of representing complex multi-modal distributions
 2. Map to generate "useful" actions from noise samples
 3. State conditioned
 4. Should allow for easier learning without hindering the RL agent's ability to attempt novel behaviours.

Normalizing flows can do all of this.

[[density_estimation_using_real_nvp|"Real Valued Non-volume preserving"]] architecture . They allow maximizing exact LL of observed eamples and learning a deterministic invertible mapping that transforms samples from $p_z$ to examples in the training dataset.

$$
p_{\text{prior}}(a|s) = p_z (f^{-1}_{\phi}|\det (\partial f^{-1}_{\phi} (a;s) / \partial a|)
$$


"Affine coupling layer" - several can be composed together to transform noise vectors into samples from complex distributions.

So basically you learn to map from noise to action that was likely in the dataset.

Since the mapping is invertible, for any $a$ you can find a $z$ that generates $z = f^{-1}_{\phi} (a; s)$ 

## Experiments

Questions:
1. Can this accelerate the learning of new tasks?
2. How does PARROT compare with prior works?
3. How does PARROT compare with prior method sthat combine hierarhical imitation with RL?

Domain: 6DoF robotic arm with a 7D action space. Observations are 48x48 images. Objects in the test scenes are novel, so the states are novel, but with sufficient training data might still encode in useful ways.

Dataset $\mathcal{D}$: Scripted interactions with random objects. Keep a trajectroy if it ends with a successful grasp or rearrangement of any one of the objects in the scene.


### Baselines

- [[soft_actor_critic|SAC]]: No previously collected data
- SAC with demonstrations: Do behavioural cloning on $\mathcal{D}$ and fine-tune with SAC (similar to [[awac_accelerating_online_reinforcement_learning_with_offline_datasets]])
- Transfer Learning with Features: Train $\beta$-VAE and use the representations for training (like [[darla_zero_shot_transfer_reinforcement_learning_disentanglement]])
- Trajectory modelling with RL: Model the whole trajectory with a VAE (see [[kyrki_data_efficient_visuomotor_policy_training_using_reinforcement_learning_and_generative_models]])
- Hierarhical imitation Learning: Latent variable models over expert demonstrations and discover options (see [[deep_imitative_models_for_flexible_inference_planning_and_control]] and [[discovering_motor_programs_by_recomposing_demonstrations]])

![[parrot_results.png]]

**Main Results**: see image above

**Dataset size and performance**: Size of prior dataset correlates with performance, but you only need above 10k trajectories total to get good performance, additional data gets you diminishing returns. Even then, 5k trajectories is better than learning from scratch.

**Mismatch between train/test (OOD)**: Deliberately bias the training set so that the training and test tasks are functionally different (eg, involving very different actions). If prior trained on pick-and-place you can still solve downstream grasping tasks. But training on grasping doesn't help much with pick-and-place. Pick-and-place involves an entirely new action unseen in grasping.

## Future Work

Future Directions:
 => Utilizing flow-based models as priors can lead to safer exploration
 => Optimal architecture for the flow based model.
 => Lifelong learning systems

