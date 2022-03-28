---
title: Reinforced Cross-Modal Matching and Self-Supervised Imitation Learning for Vision-Language Navigation.
venue: CVPR
pages: 6629-6638
year: 2019
type: Conference and Workshop Papers
access: open
key: conf/cvpr/WangHcGSWWZ19
doi: 10.1109/CVPR.2019.00679
ee: http://openaccess.thecvf.com/content_CVPR_2019/html/Wang_Reinforced_Cross-Modal_Matching_and_Self-Supervised_Imitation_Learning_for_Vision-Language_Navigation_CVPR_2019_paper.html
url: https://dblp.org/rec/conf/cvpr/WangHcGSWWZ19
authors: ["Xin Wang", "Qiuyuan Huang", "Asli Celikyilmaz", "Jianfeng Gao", "Dinghan Shen", "Yuan-Fang Wang", "William Yang Wang", "Lei Zhang"]
sync_version: 3
cite_key: conf/cvpr/WangHcGSWWZ19
---

Study how to address three critical challenges for this task:

1. Cross-modal matching
2. Ill-posed feedback
3. Generalization problems

Proposes a novel "Reinforced Cross-Modal Matching" approach that enforces cross-modal grounding both locally and globally via RL.

Matching critic is used to provide an intrinsic reward to encourage global matching between instructions and trajectories and a reasoning navigator used to perform cross-modal grounding in the local visaul scene. The point of hte matching critic is that it evaluates an executed path by the probability of reconstructing the original instruction from it, eg, the cycle reconstruction reward.

VLN has some challenges

1. Reasoning over visual images and NL instructions is difficult
2. Feedback is rather coarse, you only get success at the end and this ignores whether you followed the given instructions or if you followed a random path. Good trajectories are also labelled as failures if they stop a little bit before the goal.
3. Generalization problems

# Reinforced Cross-Modal Matching

## Reasoning navigator (the policy)

![[reinforced_cross_modal_matching_navigator.png]]

Maps the input instruction $X$ on to a sequence of actions. Get a state $s$ and ground the textual instruction into the local visual scene.

Cross-modal reasoning navigator that leans the trajectory history and the focus of hte textual instruciton and the local visual attention in order.

History done through an LSTM.

Then you do attention over the visual features.

Further learn the textual context conditioned ont he history context. Let the language encoder LSTM encode the language instruction into a set of textual features (eg, one LSTM output for every text input), then do attention over those LSTM tokens conditioned on the history context.

Then to predict actions, take the concatenated history vector, attended text vector and visual features and compute the probability of each action embedding using attention over the actions.

## Critic

Derive an intrinsic reward $R_{\text{intr}}$ provided by the matching critic $V_{\beta}$ to encourage glboal matching between the language instruction and the navigator's trajectory.

Adopt an attention-based sequence-to-sequence language model as the matching critic $V_{\beta}$ which encodes the trajectory with a trajectory encoder and produces a probabiliyt distribution of generating each word of the instruction $X$ with a language decoder. Basically, similar to [[learning_to_interpret_natural_language_navigation_instructions_from_observations]] except using a neural network to estimate the probability.

# Learning

Reward is $\mathcal{D}_{\text{target}}(s_t) - \mathcal{D}_{\text{target}}(s_{t + 1})$ - eg, you get a reward for having a reduced distance to the target. You also get a reward for success.


