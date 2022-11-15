---
title: "A Generalist Agent."
venue: "CoRR"
volume: "abs/2205.06175"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2205-06175"
doi: "10.48550/ARXIV.2205.06175"
ee: "https://doi.org/10.48550/arXiv.2205.06175"
url: "https://dblp.org/rec/journals/corr/abs-2205-06175"
authors: ["Scott E. Reed", "Konrad Zolna", "Emilio Parisotto", "Sergio Gomez Colmenarejo", "Alexander Novikov", "Gabriel Barth-Maron", "Mai Gimenez", "Yury Sulsky", "Jackie Kay", "Jost Tobias Springenberg", "Tom Eccles", "Jake Bruce", "Ali Razavi", "Ashley Edwards", "Nicolas Heess", "Yutian Chen", "Raia Hadsell", "Oriol Vinyals", "Mahyar Bordbar", "Nando de Freitas"]
sync_version: 3
cite_key: "journals/corr/abs-2205-06175/Reed/2022"
tags: ["DeepMind"]
---

Gato is a multi-modal, multi-task, multi-embodiment generalist policy. The same network can play Atari, caption images, chat, stack blocks and muhc more.

Different tasks from different modalities get serialized into a flat sequence of tokens and processed by a big transformer.

The hypothesis they test is having an agent which is good at a large number of tasks and can be adapted with a small amount of extra data.

Gato was trained fully offline.

## Tokenization
 - SentencePiece for text
 - Images: ViT style
 - Discrete values: Flattened into sequences of integers in row-major order
 - Continuous values: flattened into sequences of floating point values in row-major order. Encoded into range -1 to 1 and discretized into bins and embedded.
 - Learnable position encodings.

## Training

One giant sequence model.

## Identifying the task

Instead of having one-hot task identifiers, instead use prompt conditioning. Usually goal conditioning, eg, showing the end of the episode. Done on 25% of tasks.

## Datasets

 - DMLab,
 - Atari
 - Sokoban
 - BabyAI
 - DMCS
 - Meta-world
 - RGB Stacking
 - MassiveText
 - ALIGN
 - OKVQA


# Experiments

Figure 5: If you change the "threshold" for being better than an expert, they show how many tasks Gato beats the expert according to that threshold.

Generalization: Can you handle previously unseen shapes? Its comparable to a comparable baseline.

# OOD Tasks

Hold out:

 - cartpole.swingup
 - assembly-v2
 - orders_of_apples_forage_simple
 - boxing

Ideally we'd want to condition on prompts, but this is really hard to do on current accelerator architectures due to self-attention limitations.

Ablations over several pretraining scenarios before finetuning:
 - Same domain data only
 - No control data (text, images)
 - From scratch

So to test his, they test in the *fine-tuning* setting. Its OK. Basically pretraining on everything boosts your initial scores in some tasks, though is only marginally bettter than "same domain data" in metaworld assembly and DMLab order of apples. Doesn't happen on boxing.