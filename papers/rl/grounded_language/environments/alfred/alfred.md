---
title: "ALFRED - A Benchmark for Interpreting Grounded Instructions for Everyday Tasks."
venue: "CVPR"
pages: "10737-10746"
year: 2020
type: "Conference and Workshop Papers"
access: "open"
key: "conf/cvpr/ShridharTGBHMZF20"
doi: "10.1109/CVPR42600.2020.01075"
ee: "https://openaccess.thecvf.com/content_CVPR_2020/html/Shridhar_ALFRED_A_Benchmark_for_Interpreting_Grounded_Instructions_for_Everyday_Tasks_CVPR_2020_paper.html"
url: "https://dblp.org/rec/conf/cvpr/ShridharTGBHMZF20"
authors: ["Mohit Shridhar", "Jesse Thomason", "Daniel Gordon", "Yonatan Bisk", "Winson Han", "Roozbeh Mottaghi", "Luke Zettlemoyer", "Dieter Fox"]
sync_version: 3
cite_key: "conf/cvpr/ShridharTGBHMZF20"
---
ALFRED - Action Learning from Realistic Environments and Directives. Benchmark for learning a mapping from NL instructions and ego-centric vision of the world.

Includes long compositional tasks with non-reversible state changes.

Expert demonstrations for 25k natural language directives which include high-level goals like "rinse a mug and place it in the coffee maker" and "walk to the coffee maker on the right" (low level). For each of the 2685 combinations of task parameters, there are three expert demonstrations per parameter set. Generating expert demonstrations is also more difficult than just path planning, since there are state changes as well. The language directions come from AMT and have the "long tail" of language.

What is unique about ALFRED is the the "high visual quality", 25k+ human annotations, presence of movable objects, state changes and egocentric viewpoint.

# How does a Seq2Seq model do?

Model definition: Convolutional encoder of the inputs, then re-weighting the instructions based on what is relevant. Pass that to an LSTM cell and produce the current hidden state, then the hidden state gives you the action.

How to encode the language? Bidirectional LSTM.

Baseline models perform poorly on ALFRED and this suggests that there is significant room for improvement.

There are 13 actions:

 1. MoveAhead
 2. RotateRight
 3. RotateLeft
 4. LookUp
 5. LookDown
 6. Pickup
 7. Put
 8. Open
 9. Close
 10. ToggleOn
 11. ToggleOff
 12. Slice
 13. Stop

## Auxiliary losses

Since the tasks require reasoning over long sequences of images and instruction words, two auxiliary losses are proposed.

1. Internal estimate of progress towards the goal. Akin to learning the value function. See [[self_monitoring_navigation_agent_via_auxiliary_progress_estimation]] . In effect, $p_t = \sigma(W_p [h_t; u_t])$ with supervision on the timesteps for expert demonstrations.
3. Also predict hte number of sub-goals completed so far, $c_t$. $c_t = \sigma(W_c [h_t; u_t])$