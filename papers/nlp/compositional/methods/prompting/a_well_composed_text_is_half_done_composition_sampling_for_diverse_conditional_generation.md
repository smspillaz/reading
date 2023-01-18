---
title: "A Well-Composed Text is Half Done! Composition Sampling for Diverse Conditional Generation."
venue: "ACL"
pages: "1319-1339"
year: "2022"
type: "Conference and Workshop Papers"
access: "open"
key: "conf/acl/NarayanSZM00L22"
doi: "10.18653/V1/2022.ACL-LONG.94"
ee: "https://doi.org/10.18653/v1/2022.acl-long.94"
url: "https://dblp.org/rec/conf/acl/NarayanSZM00L22"
authors: ["Shashi Narayan", "Gon\u00e7alo Sim\u00f5es", "Yao Zhao", "Joshua Maynez", "Dipanjan Das", "Michael Collins", "Mirella Lapata"]
sync_version: 3
cite_key: "conf/acl/NarayanSZM00L22"
---

This is about avoiding text degeneration when trying to generate diverse outputs.

You avoid text degeneration by first sampling a composition in the form of an entity chain, then use beam search to generate the best possible text grounded to the entity chain.

You use nucleus sampling to obtain diverse compositions of "entity chains", then you do beam search to generate most likely outputs for each of the entity chains.

What's an entity chain? Its basically a list of entities occurring in the output text. Controls what the text is "about". Its different from a nucleus in the normal sense in that different nuclei may be talking about the same thing.