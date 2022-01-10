# Parrot

 => How can we pre-train RL agents?
 => Pre-training behavioural priors captures complex IO relationships observed in successful trials from a wide range of previously seen tasks.
 => Can be used to rapidly learn new tasks without impeding exploration.
 
 
 Typically you utilize random exploration, learning to slow learning.
 
 Quite different from how people acquire new skills - learning to play tennis, you'd re-use skills you had already.
 
 Dominant paradigm: Meta-RL: Trained to maximize reward over a distribution of environments. When given a new task, maximize reward for new tasks as quickly as possible. Running large scale RL experiments take a fair bit of effort.
 
 What if we have access to offline datasets from previously seen tasks?
 
 Kind of common in CV and NLP but not RL.
 
 Requirements for pre-training an RL agent are different because you need to capture rich input-output relationships. Contrast to CV/NLP where you just learn good representations.
 
 PARROT: Prior AccelRated ReinfOrcemenT.
 
 use the behavioural prior to explore effectively. Maximize reward for task of interest. Priors should execute meaningful behaviours.
 
 How can we learn a prior from data? Use generative models. Eg GPT3, autocomplete.
 
 ![[parrot.png]]
 
 Prior: Takes observatons and outputs an action that makes sense in that context. Also take noise which allows you to generate several possible valid actions. Allow you to sample from a simple distribution and transfer to a complex multimodal one.
 
 ![[parrot_flow.png]]
 
 Parameterize our prior using flow-based generative models.
 
 The models are also invertible - for any action, there exists some input which allows to see the situations to which applies.
 
 Sampling trajectories from the prior is much more effective.
 
 Transforms the MDP into an easier one since random actions are transformed into ones that are likely to lead to rewards.

May be several possible useful tasks - prior may not maximize the reward for the task at hand.

![[parrot_rl_policy_input_to_prior.png]]

We have a new RL policy that produces the latent $z$ used by the prior. The invertibility property of the prior guarantees that there exists some $z$ that generates the action. So basically the RL policy generates "observations" for the prior.

Transfer the learned prior to new environments with new objects. Compare against VAE based approach in our experiments. PARROT outperforms BC + RL and prior works in hierarhical imitation and RL.

Future Directions:
 => Utilizing flow-based models as priors can lead to safer exploration
 => Optimal architecture for the flow based model.
 => Lifelong learning systems
 
 
