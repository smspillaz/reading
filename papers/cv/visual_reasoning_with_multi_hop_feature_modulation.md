---
title: "Visual Reasoning with Multi-hop Feature Modulation."
venue: "ECCV"
pages: "808-831"
year: 2018
type: "Conference and Workshop Papers"
access: "closed"
key: "conf/eccv/StrubSPVMPCP18"
doi: "10.1007/978-3-030-01228-1_48"
ee: "https://doi.org/10.1007/978-3-030-01228-1_48"
url: "https://dblp.org/rec/conf/eccv/StrubSPVMPCP18"
authors: ["Florian Strub", "Mathieu Seurin", "Ethan Perez", "Harm de Vries", "J\u00e9r\u00e9mie Mary", "Philippe Preux", "Aaron C. Courville", "Olivier Pietquin"]
sync_version: 3
cite_key: "conf/eccv/StrubSPVMPCP18"
---
Generate the parameters fo the FiLM layers in a "multi-hop" fashion rather than all at once. This can scale to longer input sequences such as dialogue.

Prior work generates the FiLM parameters all at once. Eg, encode the language from one end to another and then generates a single embedding by which the image is processed.


![[multi_hop_film.png]]

In multi-hop FiLM you have a parallel network which refines the conditioning vector at each stage by taking the attention-weighted average over each of the encoded language statements.