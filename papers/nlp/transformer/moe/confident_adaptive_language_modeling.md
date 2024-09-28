---
title: "Confident Adaptive Language Modeling."
venue: "NeurIPS"
volume: "35"
year: "2022"
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2207-07061"
doi: "10.48550/ARXIV.2207.07061"
ee: "https://doi.org/10.48550/arXiv.2207.07061"
url: "http://papers.nips.cc/paper_files/paper/2022/hash/6fac9e316a4ae75ea244ddcef1982c71-Abstract-Conference.html"
authors: ["Tal Schuster", "Adam Fisch", "Jai Prakash Gupta", "Mostafa Dehghani", "Dara Bahri", "Vinh Q. Tran", "Yi Tay", "Donald Metzler"]
sync_version: 3
cite_key: "conf/nips/SchusterFG0B0TM22"
---


At each timestep, exit at the first layer for which the confidence exceeds some calibrated threshold. Eg, if there is some poiny where token output entropy is very low, you're unlikely to change all that much. You can also predict the entropy directly.