---
title: "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments."
venue: "NIPS"
pages: "6379-6390"
year: 2017
type: "Conference and Workshop Papers"
access: "open"
key: "conf/nips/LoweWTHAM17"
ee: "https://proceedings.neurips.cc/paper/2017/hash/68a9750337a418a86fe06c1991a1d64c-Abstract.html"
url: "https://dblp.org/rec/conf/nips/LoweWTHAM17"
authors: ["Ryan Lowe", "Yi Wu", "Aviv Tamar", "Jean Harb", "Pieter Abbeel", "Igor Mordatch"]
sync_version: 3
cite_key: "conf/nips/LoweWTHAM17"
tags: ["DeepMind"]
---
# Multi-Agent Actor-Critic for Mixed Co-operative and Competitive Environments

Basically in this paper you have local actors which have access only
to local information and a centralized critic which has access to
what all the managers are doing.

In this work:

 (1) Learn a critic for each agent
 (2) Consider environments with differeing reward functions
 (3) Combine recurrent policies with feed-forward critics
 (4) Learn continuous policies vs learning discrete policies

If we know the actiosn taken by all agents, then the environment is
stationary even as policies change.

## Experiments

Co-operative communication: Speaker/listener.

 - Listener must navigate to a landmark of a given color
 - Listener gets the observations of the environment
 - Speaker knows which landmark you need to go to but
   can only say which landmark the listener should go to
   -> Listener must learn to pay attention to the speaker
   -> Speaker must learn to output the correct landmark color

Traditional RL methods completely fail at this. Listener ignores the
speaker and simply moves to the middle of all observed landmarks.

 - Why does this fail? speaker utters the correct symbol while the
   listener moves in the wrong direction -> speaker penalized.
 - Speaker utters the incorrect symbol while the listener moves in
   the right direction -> speaker rewarded
 - MADDPG can learn co-ordinated behaviour beacuse they have access
   to a centralized critic.