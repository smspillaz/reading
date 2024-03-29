---
title: "VTNet: Visual Transformer Network for Object Goal Navigation."
venue: "ICLR"
year: 2021
type: "Conference and Workshop Papers"
access: "open"
key: "conf/iclr/DuY021"
ee: "https://openreview.net/forum?id=DILxQP08O3B"
url: "https://dblp.org/rec/conf/iclr/DuY021"
authors: ["Heming Du", "Xin Yu", "Liang Zheng"]
sync_version: 3
cite_key: "conf/iclr/DuY021"
---
# VTNet: Visual Transformer Network for Object-Goal Visual Navigation

tl;dr: Object-goal visual navigation aims to steer an agent towards a target object based on observatons of the agent.

VTNet: Relationships among all object instances in the scene are exploited. Spatial locations of objects and image regons are emphasized so that directional navigation signals can be learned.

Pre-training scheme to associate visual representatons with navigation signals and thus facilitate navigation policy learning.

![[vtnet_architecture.png]]

VTNet encodes relationships between objects in a scene. Spatial locations are emphasized so that directional navigation systems can be learned.

Spatial Enhanced local descriptors = take advantange of all detected objects for exploration.

Positional Global Descriptor.

Directly training VTNet with navigation policy network fails to converge due to training difficulty of transformer. We have a pre-training scheme. We imitate expert trajectories.