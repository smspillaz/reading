---
title: "Zero-shot Sonnet Generation with Discourse-level Planning and Aesthetics Features."
venue: "NAACL-HLT"
pages: "3587-3597"
year: "2022"
type: "Conference and Workshop Papers"
access: "open"
key: "conf/naacl/TianP22"
doi: "10.18653/V1/2022.NAACL-MAIN.262"
ee: "https://doi.org/10.18653/v1/2022.naacl-main.262"
url: "https://dblp.org/rec/conf/naacl/TianP22"
authors: ["Yufei Tian", "Nanyun Peng"]
sync_version: 3
cite_key: "conf/naacl/TianP22"
---

Does not require training on poems. They design a framework which plans the poem sketch before decoding.

 - Content planning model obtains discourse level coherence
 - Rhyme module generates rhyme words
 - Polishing module introduces imagery and similes for aesthetic purposes.
 - Constrainted decdoing algorithm to impose meter-and-rhyme consraint of generated sonnets.

How do you control the text formatting? Use MASK tokens as placeholders for the keywords.


At each decoding step we apply rhythm control, so only those tokens that satisfy the iambic-pentameter and its two variations are kept in the beams. They use a very wide beam, eg, beam size of 50. Recursively generate next token until 10 or 11 syllables are generated and make up a metric line where all the context words are incorporated.