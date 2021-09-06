Curiousity turns sparse reward into dense rewards. Three main families:
 - Prediction error (visit states where your predictions are wrong)
 - visit counts (bonus for visiting states that you've never seen before)
 - goal-generation (propose "reachable" goals that are not easy, see [[selfplay]]).

Prediction-error-bonus: "couch potato" problem: You get stuck just doing useless actions and don't explore the world. You do things that are inherently hard but you don't gain anything by doing them.

Instead of asking how hard it is to predict the next state, ask how probable it is to reach the next state given the previous knowledge.


![[curiousity_family_reachability_network.png]]


Compare pairs of observations, classify is $s_{t + n}$ reachable from $s_{t}$

Curiousity bonus from reachability metric. Assign bonus to reward which is higher for stats that are hardly reachable and lower for those that are not.