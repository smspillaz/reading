---
title: "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale."
venue: "CoRR"
volume: "abs/2208.07339"
year: 2022
type: "Informal Publications"
access: "open"
key: "journals/corr/abs-2208-07339"
doi: "10.48550/ARXIV.2208.07339"
ee: "https://doi.org/10.48550/arXiv.2208.07339"
url: "https://dblp.org/rec/journals/corr/abs-2208-07339"
authors: ["Tim Dettmers", "Mike Lewis", "Younes Belkada", "Luke Zettlemoyer"]
sync_version: 3
cite_key: "journals/corr/abs-2208-07339/Dettmers/2022"
---

How to do quantization? Different methods:
-   Absmax: X = 127 * X / max(X) and round
-   Zeropoint: Use the full range of -127 to 127. You have to divide by the minmax range of the tensor. Multiplication becomes tricky because you have to handle negatives. Generally (A + zero point) * (B + zeropoint). The zeropoint is X * min(X).

How much memory does it save?
- Well, basically with 8-bit quantization you can run an 11B parameter model as opposed to a 1.3B one with 16 bit FP. So its a significant increase.

-   Other related work: nuQmm, ZeroQuant: Group-wise quantization

Limitations: Don’t use int8 quantization for attention, though this does actually consume some memory, at least quadratic in the length of the sequence size. Might be able to get away with better pipelining (eg, compute row 1 of attention, multiply with column 1 of values, then throw it out, etc. Also don’t look at training or finetuning. Its hard.