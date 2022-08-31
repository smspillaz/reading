---
title: CtrlFormer: Learning Transferable State Representation for Visual Control via Transformer.
venue: ICML
pages: 16043-16061
year: 2022
type: Conference and Workshop Papers
access: open
key: conf/icml/MuCDCCL22
ee: https://proceedings.mlr.press/v162/mu22a.html
url: https://dblp.org/rec/conf/icml/MuCDCCL22
authors: ["Yao Mark Mu", "Shoufa Chen", "Mingyu Ding", "Jianyu Chen", "Runjian Chen", "Ping Luo"]
sync_version: 3
cite_key: conf/icml/MuCDCCL22
---
In Visual Control, learning transferrable state representations that can transfer between different control takss is important to reduce the training sample size.

The paper proposes CtrlFormer, which jointly learns self-attention between visual tokens and policy tokens among different control tasks, where a multitask representatio ncan be learned without catastrophic forgetting. The paper also proposes a contrastive reinfrocement learning paradigm to train CtrlFormer with high sample efficiency.

The idea behind CtrlFormer is to learn state representations in one task and transfer them in another (eg, cartpole swingup dense to cartpole swingup sparse). What you want is that *after* the transfer you don't forget how to do the original task (called *maintainability*). You also want the representations learned on the original to help you out on the new task (called *transferrability*).

How does CtrlFormer work? You get given an input and a "policy token" corresponding to the task that you are currently doing. Then you have to predict the action distribution.

It seems that you get all the image tokens and policy tokens as well as a "contrastive token" all at once. The point is that you don't actually know which policy will be in use, you only get the input image and then all policies have to make a prediction.

To train the CtrlFormer, you take the "policy token" from the output sequence corresponding to the task at hand and regress the policy/Q networks. The idea is that all policy tokens are updated at the same time regardless what the task is due to self-attention.

The "contrastive token" is trained by having a teacher-student architecture, where the teacher is an EMA of the student and gets augmented observations, similar to SimCLR (note: unclear why you don't get representation collapse by doing it this way). This apparently helps with sample efficiency according to their ablation study.