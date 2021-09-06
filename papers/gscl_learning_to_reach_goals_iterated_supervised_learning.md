# Learning to reach goals via iterated supervised learning

- Goal-reaching is hard
- Learn goal-reaching policies without demonstrations
- Re-label and imitate trajectories that an agent generated to progressively learn goal-reaching behaviours from scratch


We want to learn useful policies but we have to do it through a feedback loop.

 - Value based methods: Bootstrap their value estimate, but this is a highly nonstationary regression problem
 - Policy gradient methods: Don't correspond to a prediction problem at all, forced to use data only from the most recent policy


Instead of needing to learn through feedback, you have access to a human expert - you imitate the expert.

When we have access to a dateset of optimal trajecctories, then imitating it leads to a good policy.

Can we do the same in RL?
 - We can't imitate our own trajectories
 - Try to make the trajectory optimal, at which point imitating it makes sense. Supposing that we had access to a device that made the trajectory optimal.
 - No way to implement this mechanism without having additional external information.


For goal reaching problems, this method can be efficiently implemented.

Basically hindsight. It also achieved all the intermediate states - you can re-label any of the intermediate states.

Connection to HER: HER relabels transitions - we construct a new fictitious transition pretending that the goal was something else. Value based method can estimate the value for any other goal in the environment.

GSCL only relabels the goal to be one of the achieved goal states later in the trajectory. We don't need a fictitious transition to estimate the value function, we can use it to estimate optimal behaviour.

GSCL uses it to directly learn a policy.

When data collection and optimization is iterated, then GCSL optimizes a lower bound on the true RL objective. Under certain conditions on the environment, we have a performance guarantee.

