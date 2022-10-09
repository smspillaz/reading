---
title: "Improving Out-of-Distribution Robustness via Selective Augmentation."
venue: "ICML"
pages: "25407-25437"
year: 2022
type: "Conference and Workshop Papers"
access: "open"
key: "conf/icml/Yao0LZL0F22"
ee: "https://proceedings.mlr.press/v162/yao22b.html"
url: "https://dblp.org/rec/conf/icml/Yao0LZL0F22"
authors: ["Huaxiu Yao", "Yu Wang", "Sai Li", "Linjun Zhang", "Weixin Liang", "James Zou", "Chelsea Finn"]
sync_version: 3
cite_key: "conf/icml/Yao0LZL0F22"
---

In this paper they consider the problem of a subpopulation shift (imbalanced data) and domain shifts.

They try to learn invariant predictors without resitrctiong model representations or predictors.

Selective augmentation called LISA - which interpolates samples with either the same labels but different domain or with the same domain but with different labels.

Intra-label LISA (LISA-L)

Interpolates samples with the same label but in different domains

Intra-domain LISA (LISA-D)

Interpolates samples with the same domain but different labels.

LISA is effectively doing sample mixup between either labels or subpopluations.