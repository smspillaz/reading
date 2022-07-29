# Visual Commonsense in Pretrained Unimodal and Multimodal Models

Lots of commonsense knowledge grounded in the visual modality. Visually grounded common sense.

For example - what is the color of a penguin - usually black and white. We can develop a distribution oer teh color of a penguin. Also about the shape of a penguin etc also the material

Evaluate text-only models on those relation types to evaluate how well they capture such visually grounded concepts. 

ViComTe: Visual Commonsese Tests - 5 relations. Color shape materail visaul co-occurrence. All of the data takes the form of a subject mapped to a distribution over objects.

Color: (sub) can be of color (obj)

(subj) -> "sky" should be (sky, blue), but also sometimes pink yellow black

Material (sub) can be made of (obj) -> (sofa, cloth)

Evaluation metrics:
 - spearman's rank order correlation
 - top-1 accurracy

Dataset evaluation:
  - CoDa dataset vs CiComTe
  - Measure reporting bias by data grouping
	  - SINGLE: Color of snow is almost always white
	  - MULTI: Can be one of many things, but not all
	  - ANY: Can by any of them

Models:
 - LML BERT, RoBERTa, ALBERT
 - VLM:  Oscar, VisualBert, CLIP, Vokenization
 - Distilled: Student BERT from Teacher Oscar
 - CaptionBERT: BERT model trained on Oscar's caption-based text data

Experiment:
 - Zeors-hot prediction of masked tokens
 - In all relations color material coocurrence, Oscar outperforms BERT. CaptionBert outperformance BERT -> text domain difference matters. Knowledge Distillation helps.

CLIP is not trained on MLM. put logistic regression head on top of hte crozen encoder output to predict the target object.

# Few-shot subgoal planning
[[few_shot_subgoal_planning_with_language_models]]

Text-instruction following agents require many things.

As humans we approach these tasks by planning at an abstract level. Use plans to guide actions =.

Languge Priors for Planning

Subgoal planning problem.
 - Given a high level task, the goal is to break this down into a sequence of options.
 - Modualr poloikcy that takes these subgoals in the environment

Contributions
 - LLMS can help plan
 - Ranking strategies to improve model preidctions
 - Interaction and feedback from the agent's environment.

Create goals using in-context learning. Eg, "Place tennis racket on bed = pick up tennis tacket, place in bed".

ALFRED benchmark: Sequence-to-object interactions. Each instruction can be annotated with subgoals from a planner. 7 action types, 80 object types.

"Place a martini glass on with a fork on it on the table."

 - Ranking hypotheses - If "sink" does not appear in the training demonstration, popularity bias.
 - Tendency for model to repeat things in their context.
 - Language model probabilities are poorly calibrated

To address calibration issues - mutual information ranking - weighted version of PMI.

A mesure of how well the subgoal sequence explains the instruction.

Recent approaches:
 - MOCA
 - FILM [[film_following_instructions_in_language_with_modular_methods]]
 - HLSM

Conclusions:
 - LLMs for planning in real-world tasks
 - Mutual information inspired metrisc for re-ranking
 - Interaction and feedback improve predictions

Confusion matrix for object prediction accurracy


# Disentangling Categorization in Multi-agent Emergent Communication

Agents with co-operate in a certain way and have a certain architecture have a property called language emergence.

Analogical reasoning - the representations between people will be different. We know that language is what can mediate differences in representaitons. We don't have to assume that the sender and receiver have the same perception.

Consider two agents playing a signalling game. They have to send some signalling to pick out the correcti mage.

How to ground the image and the sentence?

What technigues can we use:
 - Disentangled representaions
 - Concept whitening

Three types of agents: 
- Traditional ConvNets
- ProtoPNet
- Concept Whitening

Latent You can visualize the categorization at certain timesteps.

# CoSIM: Commonsense Reasoning for Counterfactual Scene Imagination

Hyounghun Kim

[[cosim_commonsense_reasoning_for_counterfactual_scene_recognition]]

Scene Imagination via language - humans can imagine what is told and superimpose it on to the real scene.

New dataset called CoSIM: Three components, initial question and response requiring commonsense reasoning to handle. Scene change is a contextual description which modifies the condition on the image, the new response should be different.

Model outputs - split changes into sub-parts and compute scores for each part ot see on which part the model focuses to answer the question.