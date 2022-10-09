---
title: "Vision-and-Language Navigation - Interpreting visually-grounded navigation instructions in real environments."
venue: "CoRR"
year: 2018
type: "Informal Publications"
access: "open"
key: "conf/cvpr/AndersonWTB0S0G18"
ee: "http://arxiv.org/abs/1711.07280"
url: "https://dblp.org/rec/conf/cvpr/AndersonWTB0S0G18"
authors: ["Peter Anderson", "Qi Wu", "Damien Teney", "Jake Bruce", "Mark Johnson", "Niko S\u00fcnderhauf", "Ian D. Reid", "Stephen Gould", "Anton van den Hengel"]
sync_version: 3
cite_key: "conf/cvpr/AndersonWTB0S0G18"
tags: ["DeepMind"]
---

To enable and encourage the application of vision and language methods to the problem of interpreting visually grounded navigation instructions, present the Matterport3D simulator.

This is an RL environment based on real imagery.

One of the primary requirements for robots is to understand natural language is unstructured previously unseen environments.

Previous approaches neglected the visual information processing aspects of the problem. Eg, using rendered rather than real images

R2R datasets: 21567 open vocabulary crowed-sourced navigation instructions with an average length of 29 words. Each instructions describes a trajectory.

This builds on other navigation based simulators like VizDoom, DM Lab, AI2-THOR, HoME, House3D, MINOS, CHALET, Gibson Env.

Use of RL for language based navigations studied in:

 - [[gated_attention_architectures_for_task_oriented_language_grounding]]
 - [[mapping_instructions_and_visual_observations_to_actions_with_reinforcement_learning]]

Action space of the simulator are reachable viewportings. Agent must select a new viewpoint and nominated camera heading. The environment tells you where it is possible to go. Imagine a sort of navigational graph.

The task is that you get a full description of exactly what you have to do in "natural language" and then execute a series of actions with each action leading to a new pose and generating a new observation.

To approach the problem, use a sequence-to-sequence model, encoding the language instructions as a sequence, and predicting actions using an attention mechanism.

To train, use teacher forcing/student forcing. Use cross-entropy loss at every step to maximize the likelihood o the ground-truth target action given teh previous state-action sequence.

Compare against random baseline and shortest path baseline.

Also studies generalization to unseen environments (val unseen / test in table 1). Success rate on seen datasets is 52.9% when suing stduent forcing. On the unseen datasets its 21.8%. Not bad but a drop.