# Introductory RL

Rely too much on direct supervision. Acquiring demonstrations is costly.

Underlying data can have a pretty rich structure compared to what sparse rewards can provide us with. Learning from these sparse signals leads to sample inefficiency.

This leads to task specific policies

Self-Supervised Learning:
 - Data itself provides supervision
 - Generative / predictive: Predict directly in the data space itself (past/present, present/future, different views of the same scene. loss measured in the output space)
 - Contrastive: Distinguish between between two different data points. If they are close in time or have the same underlying data point, they should be closing. Time-contrastive networks, CPC, Deep-InfoMax.


Themes at this workshop:
 - Task-agnostic pre-training (learning self-supervised genearl purpose routines for downstream RL)
	 - Disentanglement and RL
	 - Open-ended SSL
	 - Learning generalizable rewards
 - Leveraging structure in MDPs
	 - State abstractions
	 - Equivariances in MDPs
	 - Learning one representation to optimize all rewards
 - Self-Supervised world models
	 - Danijar Hafner
	 - Augmented World Models Facilitate Zero-Shot Dynamics Generalization from a Single Offline Environment


## Irina Higgins: Disentanglement and RL (DeepMind)

Sample Efficiency and Generalization are problems We're not invariant to changes in the environment that are irrelevant. We need too many episodes to make this work.

Transfer: best RL agents are not really able to do this.

"More data + deeper models + better hardware": this is not bulletproof. Works well on simulated game environments but this isn't possible in realistic scenarios. see robotics.

Multi-task learning: We don't know how many tasks we need to solve. Could be arbitrary. We want to learn how to solve these sorts of tasks efficiently as possible.

Hypothesis: If we can capture a disentangled representation, we can get savings in efficiency in the second stage.

What makes a generally good representaton and how do we go about learning it?

 - both tasks and agent are constrained by the physics of our world. Plausible hypothesis: representations should capture and expose the relevant structural laws.
 - what might physics have to say? symmetry is important.
 - symmetry is the way that the world breaks up.


A symmetry: A symmetry is a broader concept than just visual. Things that remain unaltered even under transformations that could change them. Commutative properties - one is a symmetry of the other.

Time translation symmetry: The laws of physics don't change over time. Every symmetry has a corresponding conserved quantity.

Symmetries used to categorize things, unify existing theories, discover new objects.

Symmetries apply in natural tasks: 3D scenes can be transformed by changing scale and translation of object. You can do them in any order. These symmetries point to two conserved quantities.

We only have objects of colors and shapes.

Assume some process b which maps the observations to high level observations. If we assume that they can be expressed as linear transformations. We can represent them using *block-diagonal transformation matrices*.

In order to reflect the symmetry structure of the world, the world should be expressed in terms of independently transformable subspaces. Should have different bases.

![[iclr_symmetry_bases_disentanglement_higgins.png]]

Unsupervised disentangled representation learning: You need an independent subspace for each comoonent.

Majority of approaches based on beta-VAE (or ada-VAE). $\beta$ hyperparameter which implements a capacity constraint - leads to disentangling behaviour. You need to automatically discover a small subset.

$\beta$-VAE is not principled, but they do discover dimensions that are good enough. They are "good enough".
 - Are they though?

![[iclr_monet_slot_based_disentanglement.png]]

In the more recent MOnet work: You have slot attention, disentangle each thing in each slot. Disentanglement happens at multiple levels. You're disentangled from other objects and the background. Moving the cylinder doesn't affect the cone.

Making use of the disentangled representation to drive curiousity driven exploration.

It appears that disentangled representations are very well suited to this task. This allows us to recover a small number of axes that are equivariant. We can split these into bins - we can train different policies that move within the bins (Disentangled Cumulants Help Successor Representations, Grimm)
 - Given z features discretised into $b$ bins, we can learn $zb$ policies and solve $(b + 1)^z$ tasks.

We can solve tasks relatively well easily. At each stage you only need to figure out which combinations are rewareded and then re-use the combinations.

Representation Matters: Improving Perception and Exploration for Robotos, 2020

 - tried this in robotics
 - in both test scenarios, disentangled representations resulted in better data efficiency and performance


Also helps in Model-Based RL scenario:

 - COMA: Data Efficient Model Based RL through Unsupervised Object Discovery and Curiousity Driven Exploration.
 - Evaluated the model in test scenarios outside the training data distributions. You can do orders of magnitude better in terms of data efficiency.

They also help with generalization: by pulling different properties into independent subspaces, you can ignore the subspaces that are irrelevant to the task through masking.

[[darla_zero_shot_transfer_reinforcement_learning_disentanglement|DARLA: Improving Zero-Shot Transfer in Reinforcement Learning (Higgins, 2017)]].

 - Zero-shot transfer with disentangled representation was much better.
 - Learning reacher policy over disentangled representations resulted in significantly better transfer.


Conclusions:
 - Large amoutns of data and huge compute is not always available for RL agents in realistic settings
 - Achieving better data efficiency, generalization and transfer may be facilitated by better representation learning
 - Good representations may be those that reflect the symmetries of the world
 - Current disentangled representation methods already show benefits for data efficiency, transfer and generalization.


Questions:

 - Hey irina-higgins , recent papers ([http://proceedings.mlr.press/v97/locatello19a.html](http://proceedings.mlr.press/v97/locatello19a.html)) show that achieving disentanglement completely unsupervised isn't easy and results do not offer high disentanglement, unless some weak supervision is used. What is your opinion on using unsupervised disentangled representation learning in RL? Do you think the RL objective should be used in combination with the disentanglement objective which could work as this weak supervision? or do you think in order to achieve task-agnostic disentangled representations, it would be better to train the model first completely unsupervised, and try to improve current approaches to achieve better disentanglement?
	 - If you look at the purely unsupervised regime (VAE) where you have a unit Gaussian prior, you can't actually identify whether your representation is disentangled or not if the only thing you have access to is the data.
	 - The reason why VAEs work is because your data has a bias, your model has a bias and the interaction between the two
	 - If you're in RL
		 - Movement of physical objects - these dynamics are the things that have symmetries
		 - Try to unroll the dynamics using the hamiltonian forms - as you unroll the state, you predict the images.
 - Role of disentanglement in generalization: If the decoder never sees a certain subset of your visual space, even if youre representaiton actually encodes this new novel combination of factors correctly, the decoder can never reconstruct it.
	 - Train a separate decoder which sees the full data distribution, splice it on top
	 - Original beta-VAE paper, take a look at this.
 - Are there particular architectures that are better?
	 - We want to learn controllable features of the environment
	 - Hard to generalize beyond small toy environments
	 - Start with disentangled representations, build the policy system on top, successor features, etc.
	 - Flip the thing around, maybe if you impose this architectural constraint - if you recombine things with GPI, that will be enough of a bottleneck that encourages your convnet laters lt learn something that you can control and use.
 - CLIP, DALL-E: Trying to learn a multi-modal representation, it won't be disentangled. Image has much more complex representation than language.
	 - SCAN: You have to do disentanglement then attach language on top.
	 - Would be great to have a way to do it end-to-end but not sure how.
 - Your examples were largely in the visual domain. Does it make sense to seek disentanglement in text/NLP, any tips in that direction?  Perhaps topic models are a simplistic version of this?
	 - Unfortunately text is not very well suited for disentanglement. I am not sure what would be equivalent to symmetries in the text domain, plus the way VAEs currently disentangle rely on overlaps in pixel space when applying small deltas of symmetry transformations (e.g. if you slightly move an object, the two images will overlap in the majority of pixels). Raw text doesn't have that property. Maybe if you try to disentangle text representations (e.g. extracted from a pre-trained language model) then this property will emerge and disentanglement could work...
	-   In terms of other domains, we have a paper at this conference where we successfully disentangle EEG data, so it doesn't just have to be images
	-   Pierre: May I jump in this stimulating discussion ? 🙂 Actually, when a multimodal flow of visual/motor/language data is available to learners, unsupervised learning can make it easier to disentangle each modality by using structure from other modalities, e.g. discovering the basis primitives of visual scenes (objects) and of speech sentences (words, especially when language is perceived directly as raw sound). In the pre-deep learning era, we did a study to show this with non-negative matrix factorization approaches: MCA-NMF: Multimodal Concept Acquisition with Non-Negative Matrix Factorization, [https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0140732](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0140732)
	-   Thanks a lot irina-higgins I can say in return we are following yours with great interest, and your work on beta-VAEs was highly useful and inspirational when we developed MUGL (learning disentangled goal representations for intrinsically motivated exploration, [https://developmentalsystems.org/autonomous\_learning\_of\_disentangled\_goal\_representations](https://developmentalsystems.org/autonomous_learning_of_disentangled_goal_representations))
-   (for example: just giving disentangled representations to a policy-head MLP, this MLP will mix the representations back up again and you don't get good generalization)
	-   So in practice we see that this doesn't necessarily happen (e.g. our DARLA work [https://arxiv.org/abs/1707.08475](https://arxiv.org/abs/1707.08475)) or even the fairness results from Locatello et al [http://proceedings.mlr.press/v119/locatello20a/locatello20a.pdf](http://proceedings.mlr.press/v119/locatello20a/locatello20a.pdf)
	-   Saying this, learning a mask over the disentangled representations when training the policy etc might help make this more robust
-   (Also, if there is time: is there any work on learning a disentangled representation when you don't have access to all combinations of factors? Most of the datasets for learning disentanglement seem to assume that you have access to a dataset with all combinations of factors)
	-   Quite a few papers have tested how correlations in the generative factors affect disentangling. It appears that the VAE-based methods are actually quite robust to that. E.g. see [https://arxiv.org/pdf/1802.04942.pdf](https://arxiv.org/pdf/1802.04942.pdf) Fig. 5 or Fig. 8 in [https://arxiv.org/pdf/1901.07017.pdf](https://arxiv.org/pdf/1901.07017.pdf)


## Autotelic Deep RL agents

Learning to self-supervise for automous development

Are you able to invent your own objectives and self-supervise them.

# Panel Discussion


## What is self-supervised learning in RL?

Ability to discover latent spaces. This is really important for MBRL.

Hafner:
 - Self-Supervised Representation Learning
 - In RL we can do better, ability to collect your own data, expected information gain, self-supervised way of collecting new data
 - Controllability aspect: realised empowerment / skill discovery: making decisions that have an impact on the world


van der Pol:
 - You have to do exploration to get the data, doing good exploration without good representations is hard


"What secondary things you should learn that will help you with the primary thing". Though it doesn't have to be a secondary thing. 

There are tasks where if you don't do any self-supervision, you cannot solve the reward grounding. Extreme example-  you have a 1/10^100 chance of achieving the reward. If you use SSL, you can discover the reward. You can suffer from exponential failures - it can be exponentially harder to optimize rewards directly rather than discovering the latent dynamics.

We want to encode properties into the agent to allow the agent to discover things on its own. How far can we get with the first strategy where we are the ones encoding structure on to our agent.

 - van der Pol: Symmetry, if you don't constrain your network completely, but you have symmetric representations, you can still learn asymmetric representations on top of things. There's a tradeoff - if you have a super-flexible model, you need many samples.
 - Hafner: Language is really limited. Seems more promising to have the agent learn its own representation and map that to language. 


How do we measure progress:
 - Hafner: "Sample efficiency"
	 - Proxy metrics about the environment, eg, a game, achievements that you have unlocked, number of rooms explore , but this is not a part of the reward
 - There's a particular kind of sample complexity that matters:
	 - Sample complexity in environments that don't just have one task.
	 - Different tasks can happen in the same environment
	 - How many times do you need to sample the same task?
	 - Having a latent structure of the world should vastly reduce the number of samples you need per task.
	 - How well can you predict 100 steps in to the future
	 - Are you able to predict on new data that is slightly different from the old data
 - Environments
	 - MuJoCo: Image is being controlled by the parameters of the environment 
	 - If you had to control a humanoid robot based on an actual image, this would be more challenging
	 - Atari games are not very good for representation learning since you can solve them with a lookup table. You will encounter every situation enough that you can know.
	 - If every situation is unique, then you need to generalize.
	 - Meta-world: https://meta-world.github.io/
	 - GridWorld DSprites


It would be pretty cool if we could learn one big world model from YouTube. You want some kind of representation that has memory. These would be nice for downstream tasks. If you want predictive representations, you don't have actions, so you have to figure out what you can control.


What properties should good representations have?
 - It should be predictive of the next latent state given an action
 - Mapping should not be 1-1: We don't want a separate representation for every single thing
 - Once you have some kind of predictive model for training policies, you can generalize much better, you can use the predictive model to learn inside the predictive model.


Dealing with distractors. You still spend a lot of training time on finding out that you don't need to reconstruct pixels that you don't care about. Initially you don't know what you want to learn about and what you don't want to learn about.

There's priors on what a representation should contain and what a representation should not contain.

Do we have to do autoencoders? It may be that we don't need that.

Could SSL help with the problem of catastrophic forgetting. If you're discovering a latent state space, then the structure of that latent state space avoids forgetting - you're encoding information in a different manner than you would with a simple parametric model.

 - This can occurr if you have some structure to how you're learning.
 - If you have a latent state objective, then this decouples the temporal nature.


Trying to make sense of your latent state space means that you're going to keep focusing on the observations that matter.

We don't have to have everything in a parametric representation.

Prior: sparse changes: if I were to encourage sparse changes over time, then I would learn a representation where everything stays in place but only the orientation of my head changes. Then automatically I'm not erasing the information I can't see anymore.

What is the next big milestone?
 - When you have an RL task - you want to ask if there's a natural latent state space? If no, then SSL probably won't be useful. If yes, then maybe it can be useful.