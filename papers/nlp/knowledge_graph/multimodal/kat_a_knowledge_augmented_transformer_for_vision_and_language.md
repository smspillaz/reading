---
title: "KAT: A Knowledge Augmented Transformer for Vision-and-Language."
venue: "NAACL-HLT"
pages: "956-968"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/naacl/GuiWH0BG22"
ee: "https://aclanthology.org/2022.naacl-main.70"
url: "https://dblp.org/rec/conf/naacl/GuiWH0BG22"
authors: ["Liangke Gui", "Borui Wang", "Qiuyuan Huang", "Alexander Hauptmann", "Yonatan Bisk", "Jianfeng Gao"]
sync_version: 3
cite_key: "conf/naacl/GuiWH0BG22"
---
Proposes a method to leverage explicit knowledgebases in a transformer.

Knowledge-Augmented Transformer: integrates implicit and explicit knowledge in an end-to-end encoder-decoder architecture.

Case study on the "Outside-Knoweldge Visual Question Answering" dataset.

Eg, image of a bird + "what did this organism evolve from?". To answer you need to ground "organism" to the image of the bird, then look up "bird" to answer the question "what did this evolve from".

Contributions:

(1) Knowledge extraction: prompt-engineering to extract information from GPT-3 and for explicit knowledge a contrastive-learning approach for explicit knowledge retrieval using CLIP.
(2) Reasoning module for e2e encoder-decoder transformers.

Builds on:

 - Transformers / Multimodal transformer
 - CLIP / ALIGN
 - Knowledge-based VQA


## Explicit Knowledge Retreival

![[kat_model_architecture.png]]

Generate image patches with a sliding window.

Retrieve k entity descriptions from the knowledgebase using a similarity metric. The entities are already in the knowledgebase, we just have to find the similar ones.

## Implicit Knowledge Retrieval

Generate image bounding boxes, generate captions, ask GPT-3 for a tentative answer candidate.

## Reasoning Part

### Encoder

Concatenate question with each piece of knowledge along with sentinel tokens.

Then average the token embeddings from the last layer to get an embedding matrix of explicit and implicit knowledge. There are $m$ instances of explicit knowledge and $p$ instances of implicit knowledge.

## Reasoning

Take the global representatiosn and concatenate them together. Run it through a big transformer module and decode autoregressively.