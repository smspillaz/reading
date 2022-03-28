---
title: ALFWorld: Aligning Text and Embodied Environments for Interactive Learning.
venue: ICLR
year: 2021
type: Conference and Workshop Papers
access: open
key: conf/iclr/ShridharYCBTH21
ee: https://openreview.net/forum?id=0IOX0YcCdTn
url: https://dblp.org/rec/conf/iclr/ShridharYCBTH21
authors: ["Mohit Shridhar", "Xingdi Yuan", "Marc-Alexandre C\u00f4t\u00e9", "Yonatan Bisk", "Adam Trischler", "Matthew J. Hausknecht"]
sync_version: 3
cite_key: conf/iclr/ShridharYCBTH21
---

Given a simple request like "put a washed apple in the kitchen fridge", humans can reason in purely abstract terms.

Existing work does not yet provide the infrastructure necessary to do reasoning abstractly and executing concretely. Introduces ALFWorld, a simulator that enables agents to learn abstract text-based policies in TextWorld and then execute goals from the ALFRED benchmark.

Basically its embodied TextWorld.

Aligned parallel environments like ALFWorld offer a distinct advantage: They allow agents to explore, interact and learn in the abstract environment of language before encountering the complexities of the embodied environment.

Introduces the BUTLER model (Building Undertanding in Textworld via Language for Embodied Reasoning). First learn to perform abstract tasks in TextWorld with IL and transfers those policies into ALFRED.

Trainingin the abstract text-based environment is 7x faster and also yields better performance than training from scratch in the embodied world.

They also show that BULTER trained in the abstract text doamin generalizes better to unseen embodied settings than agents trained from corpora of demonstrations or from scratch in the embodied world.


## The BUTLER agent

The text agent takes the initial/current obserations and ga goal to generate a textual action token-by-token.

At test time, agents must operate purely from visual input. The vision module functions as a captioning module that translates visual observations int otextual descriptions. Uses Mask R-CNN to identify objects.

The controller translates a high-level text action int oa sequence of low-level physical actions that are executable in the embodied environment.

The BUTLER agent can do a little better in unseen environments than a Seq2Seq baseline, possibly because solving problems in the text domain first and then transferring over to the visual domain is a form of sparsification and discretization.