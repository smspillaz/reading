---
title: Grounding Language to Entities and Dynamics for Generalization in Reinforcement Learning.
venue: ICML
pages: 4051-4062
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/icml/HanjieZN21
ee: http://proceedings.mlr.press/v139/hanjie21a.html
url: https://dblp.org/rec/conf/icml/HanjieZN21
authors: ["Austin W. Hanjie", "Victor Zhong", "Karthik Narasimhan"]
sync_version: 3
cite_key: conf/icml/HanjieZN21
---


# Grounding Language to Entities and Dynamics for Generalization in Reinforcement Learning

Investigate the use of natural language to drive generalization of control policies and introduce a new multi-task environment called "Messenger".

Develop a new model called EMMA which uses an entity-conditioend attention module that allows for selective focus over relevant descriptions in the manual for each entry in the environment.

EMMA is end-to-end differentaible and learns a latent grounding entities and dynamics from text to observations using only environment rewards.

EMMA can get zero-shot generalization to unseen games with new dynamics, with a higher win rate than multiple baselines.


## The Messenger Environment

Multiple game variants with differing dynamics and accompanying text manuals in English.

To succeed in Messenger, the agent must relate entities and dynamics of the environment using only their references in the natural language manual and scalar rewards from the environment. There is no supervision on which entities in the game correspond to words in the instructions.

In this setup, only assume that the text provides high-level guidance without directly describing the correct actions for every game state.

### Grounding Entities

The game is designed such that simple co-occurrence statistics between an entity and text do not completely reveal the mapping from entities to words.

**Multi-Combination**: Every possible combination of entities is observed. For an entity, its symbol in the observation is the only one that *always* appears together with its text references.

**Single-Combination**: Some entities very unlikely to appear together, while otehrs may co-occurr exclusively with each other. For SC games, every text symbol in the manual co-occurrs the same number of times with all entity symbols in the observation. For example, circle and square always appear simtaneously with both "mage" and "sword" so it is impossible to tell from the observation alone which one belongs to which. In these cases the agent must learn to do the symbol grounding via interaction.


### Grounding Dynamics

Multiple copies of the same entity with different roles in Mesenger may exhibit different movement patterns. For example:

 - "The chasing mage is an enemy"
 - "The fleeing mage is a goal"


### Text Descritions

Collected text descriptions of the environments via AMT. Inject synonyms etc.


### Train/test split

Ensure that any assignment of an entity to the roles *message* or *goal* in the evaluation games never appears during trianing. So if that entity is a goal in evaluation, that entity will never be a goal during training.

### Other Environments

 - RTFM
 - BabyAI

## The EMMA Model

"Entity Mapper with Multi-Modal Attention", which employs a soft-attention mechanism over the text descriptions.

1. Generate key and value vectors for their respetive token embeddings using a pretrained language model.
2. Each entity attends to the descriptors via a symbol embedding that acts as a query.
3. Then isntead or epresenting each entity its embedding, use the attention-scaled values as a proxy for the entity.
	1. This means that you learn in terms of the *entity role* as opposed to the entiyt itself.


Text Encoder: Encode using BERT-Base


Entity Representation: Embed the symbol into a query vector and attend to the descriptions, re-weighting by attention.

Action module: Concatenate the outputs of the representation generator from the three most recent observations to obtain $X\ \in R^{H \times W \times 3d}$. Flatten the feature maps and pass through a fully-connected layer.


### Experiments and Baselines

1. Mean bag of Sentences
2. Game ID-Conditioned: No language, just the game ID
3. Bayesian-Attention Module: Does co-occurrence learn the problem? Train an NB classifier: $P(z|e) = \prod_{t \in z} P(t|e) = \prod_{t \in z} \frac{C(t, e)}{\sum_{t'} C(t', e)}$ where $t \in z$ are tokens and $C$ is the co-occurrence count function.
4. Oracle map: A model has access to the descriptor-to-entity map.
5. Text to policy: Similar to RTFM


### Curriculum

stage 1: Three entities corresponding to enemy, message and goal. Go to the message from the correct entity.

Stage 2: Entities are mobile and agent begins without hte message

Stage 3: 5 entities total with 6 descriptions.


## Results

EMMA cannot fit on to S2 without pretrianing on S1. EMMA consistently wins on both MC and SC games in S1 and S2, demonstrating EMMA's ability to ground entities without co-occurrence statistics between entity and text symbols to gudie its grounding. Fitting happened in millions of frames.

Generalization to out-of-distribution test games: G-ID, Mean-BOS and Text2pi all fail to generalize due to overfitting to entity-role assignments. BAM can generalize a little bit. EMMA wins 95\% of test games.

## Analysis of Grounding

Attention wieghts of EMMA are visualized in Figure 6. The attention weights come from the query-key attention between a symbol in the environment and its corresponding word. The attention weights in this case are sparse, indicating that the model has learned groundings for those interactions.

##