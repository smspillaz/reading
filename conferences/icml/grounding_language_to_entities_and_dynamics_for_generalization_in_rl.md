# Grounding Language to Entities and Dynamics for Generalization in RL

We investigate the use of natural language to drive the generalization of control policies and introduce the new multi-task environment Messenger with free-form text manuals describing the environment dynamics. Unlike previous work, Messenger does not assume prior knowledge connecting text and state observations — the control policy must simultaneously ground the game manual to entity symbols and dynamics in the environment. We develop a new model, EMMA (Entity Mapper with Multi-modal Attention) which uses an entity-conditioned attention module that allows for selective focus over relevant descriptions in the manual for each entity in the environment. EMMA is end-to-end differentiable and learns a latent grounding of entities and dynamics from text to observations using only environment rewards. EMMA achieves successful zero-shot generalization to unseen games with new dynamics, obtaining a 40% higher win rate compared to multiple baselines. However, win rate on the hardest stage of Messenger remains low (10%), demonstrating the need for additional work in this direction.

[[hanjie_emma_grounding_language_to_entities_and_dynamics.pdf]]

https://icml.cc/virtual/2021/spotlight/9966

## The environment - Messenger

Here you have a free-form text manual describing the environment dynamics.

Entity grounding - how do you map between text symbols to images in the problem.

Prior work simplifies or eliminates the entity grounding with either:
 - Lexical overlap
 - Oracle mapping

In contrast, there are no signals connecting them - they are disjoint symbols with no oracles. The agent needs to figure it out.

We want autonomous agents should be able to associate objects with texts by interacting with the world.

Objective: Get the message, bring it to the goal, avoid the enemy.

Agent just consult a manual as the roles can shift.

## Contributions

 - Introducing the environment to evaluate entity grounding
 - Introducing EMMA which outperforms other approaches on Messenger


## EMMA

Typical strategy is to embed each entity using a lookup, encode the text and fuse the two using FiLM.

EMMA: Obtain key-value vectors for each description in the manual. The entity embedding is a query used to select the information from the manual description. Select for relevant descriptions using scaled dot product attention.

Then take output and use it as a proxy for the entity itself.

EMMA allows you to focus on entity roles rather than making decisions based on entity identities.


Biggest difference is seen on the test games.

Attention weights of EMMA - EMMA has successfully learned to ground all the entities - it has learned to match each description to the entity that it describes.




