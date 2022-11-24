---
title: "Natural Language Communication with Robots."
venue: "HLT-NAACL"
pages: "751-761"
year: 2016
type: "Conference and Workshop Papers"
access: "open"
key: "conf/naacl/BiskYM16"
doi: "10.18653/V1/N16-1089"
ee: "https://doi.org/10.18653/v1/n16-1089"
url: "https://dblp.org/rec/conf/naacl/BiskYM16"
authors: ["Yonatan Bisk", "Deniz Yuret", "Daniel Marcu"]
sync_version: 3
cite_key: "conf/naacl/BiskYM16"
---

Proposes to ue an "intellectual framework" that has the same ingredients that have "transformed the field of computer science" - appealing problem definitions, publicly avaialble datasets and easily computable and objective evaluation metrics.

Proposes a novel Human-Robot communicaiton problem that is testable empircally and provides publicly avaialble datasets and evaluation metrics.

## Framework for Human-Robot Natural Language Communicaiton Research

1. Problem-solution sequences: High and low-level descriptions of actions that are in service of the goal, they are sequences of images that encode what a robot might see as it goes about accomplishing a goal. Eg, a list of instructions that you need to do.
2. Imple instruction/command understanding: Given the state of the world, we would like to infer the target world tht a robot should construct if it understood $C$, the language statement.

The dataset is basically a block-world arranged into MNIST images (or rather, trajectories that arrange into MNIST images). Then humans annotate the trajectories with descriptions of what is going on. The blocks have logos on them.

## Problems of Interest

1. Entity grounding: Many ways to refer to a given object in speech. These are context pecific and depend on the perceived ambiguity of hte scene. For example, the decoration of blocks with logos allows for easy indexing (nvidia block)., but you could also describe "texaco" as "the star block" or "Mercedes" as "three lines in a circle".
2. Spatial Relation Grounding: "Use block 2 as a bridge to complete the diagonal line formed by blocks 17, 8 6 4 and 1"


## Baseline Models

1-hot word vectors to FFN or RNN for encoding. Semantic represnetation extracted (green)