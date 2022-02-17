---
title: Grounding &apos;Grounding&apos; in NLP.
venue: ACL/IJCNLP
pages: 4283-4305
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/acl/ChanduBB21
doi: 10.18653/V1/2021.FINDINGS-ACL.375
ee: https://doi.org/10.18653/v1/2021.findings-acl.375
url: https://dblp.org/rec/conf/acl/ChanduBB21
authors: ["Khyathi Raghavi Chandu", "Yonatan Bisk", "Alan W. Black"]
sync_version: 3
cite_key: conf/acl/ChanduBB21
---

The term "grounding" is used to denote "any" linking of text with a non-textual modality in NLP.

But the term is much more concrete in cognitive sciences (eg, the process of establishing mutual information required for successful communication between two interlocutors).

Seeks to answer two questions:
 1. What aspects of grounding are missing from NLP tasks
 2. How is the term "grounding" used in current research?
 3. How can we advance our current definition to bridge the gap?


## Dimensions of Grounding

### Coordination

Static vs Dynamic Grounding.

In static grounding, you assume evidence for the common ground or gold truth. You have access to the ground truth in some way, you just need to query it correctly.

In dynamic grounding, common ground is built via interactions and clarifications.

 1. Requesting and provdiing clarification
 2. Acknowledging or confirming the clarifications
 3. Enacting or demonstrating to receive confirmations

You have to construct the common ground from mutually shared information with respect to the human.


### Purviews of Grounding

1. Localization: Localization of the concept either in physical or mental contexts. Need to understand each of the concepts individually ("blue" and "sweater") and then locate the composition of the whole unit
2. External knowledge: Ensure consistency of the concept with existing knowledge.
3. Common sense: Concept should be reasoned based on that particular context. Eg, "I'm cold, can you get me a coat" means a sweater and not a formal coat.
4. Personalized consensus: Meaning personalizes over time.


### Constraints of Grounding

1. Copresence: Agent and human share the same physical environment
2. Visibility: The data is visible to the agent or human
3. Audibility: Can speak about the data
4. Cotemporaility: Agent and human receive the data at roughly the same time
5. Simultaneity: Agent and human can send and receive at once simultaneously.
6. Reviewability: Agent reviews the common ground to the human to adapt to imperfect human memories
7. Revisability: Can correct errors in human instruction.


### Domains of Grounding

1. Textual modality: Comprising plain text, entities, events, knowledge bases and knowledge grpahs
2. Non-textual modalities: images, speech, images and speech, videos

### Manipulation of Representations

Grounding concepts often involves multiple modalities that are linked. Three major methods:

1. Fusion/concatenation: For text, concatenate
2. Alignment: Temporal alignment in videos, phrase localization in images
3. Projecting into a common space: Cross-lingual NER

