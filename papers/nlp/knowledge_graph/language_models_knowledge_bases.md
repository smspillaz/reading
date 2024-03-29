---
title: "Language Models as Knowledge Bases?"
venue: "EMNLP/IJCNLP"
pages: "2463-2473"
year: 2019
type: "Conference and Workshop Papers"
access: "open"
key: "conf/emnlp/PetroniRRLBWM19"
doi: "10.18653/V1/D19-1250"
ee: "https://doi.org/10.18653/v1/D19-1250"
url: "https://dblp.org/rec/conf/emnlp/PetroniRRLBWM19"
authors: ["Fabio Petroni", "Tim Rockt\u00e4schel", "Sebastian Riedel", "Patrick S. H. Lewis", "Anton Bakhtin", "Yuxiang Wu", "Alexander H. Miller"]
sync_version: 3
cite_key: "conf/emnlp/PetroniRRLBWM19"
---
# Language Models as Knowledge Bases?

General idea: While learning linguistic knowledge, maybe you're also learning relational
data as well.

How much is already there off-the-shelf in ELMo and BERT?

If we can figure out what's there, maybe we can figure out a better unsupervised
way to train such that we get this relational data.

## LAMA - Language Model Analysis

Basic Idea: Represent knowledge as three-tuples (subject, relation, object). We say
that an LM captures that if you can predict the masked objects in sentences like
"Dante was born in ___" expressing that fact.

Test for relations between entities in Wikidata, common sense relations from
ConceptNet, SQuAD.

BERT does pretty well and in general predicts objects of the correct type even
if the object itself is not correct.