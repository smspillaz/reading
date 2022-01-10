# Graph Learning based Generation of Abstractiosn for RL

[[graph_based_generation_of_abstractions.pdf]]

 - Combinatorial explosion in state space
 - One way to tackle problems is with *abstraction*
 - Abstract Markov Decsiion Processes
 - Argument: state aggregation for reward shaping should be based on properties of *topological* and *value function* similarity
 - Ground level states belonging to same abstract state should be topologically close and should appear more frequently together in high-reward paths.
 - If two states are in the same abstract state, then long term value function should also be similar.


New approach:
 - (1) extract latent representation of states encoding similarity among states in terms of topological and reward structure.
 - Closer them to generate the AMDP


Contributions:
 - Construct abstract states to preserve properties of topological and value function proxmitiy among ground level states
 - Reward shaping with construct AMDP results in 6.5x improvement in convergence speed and sample efficiency and 3x in runtime of RL algorithm
 - Qualitative analysis showing that our approach can preserve topological and reward structure of ground level MDP.


Prior work:
 - Automated discovery of options
 - Clustering algorithms applied on MDP model or gaph estiamted from states trajectories to identify abstract states or bottlenecks


Some problems:
 - Given a state-transition history, no unique way to construct a corresponding graph
 - Therefore it is inevitable that some information will be lost.


Our approach:
 - Learn low-dimensional latent state representations from state transitions
 - Cluster them together to generate abstract states
 - Then use graph representaiton learning to embed the nodes such that the topological structure is preserved.


Requirements:
 - Proximity:
	 - Topological proxmimity
	 - Value function proximity
 - Any two states in an abstract state should have similar value functions.


Maximize:

 - $\sum_{s \ in V} \sum_{s' \ in N(s)} (\log (\sigma(phi(s)) \cdot \oemga(s')) + \sum^K_{k = 1} \E_{s'' \in P} \log(\sigma(-\phi(s) \cdot \omega(s''))))$
 - Where $\sigam$ is sigmopid and $P$ is a random distribution ove rthe node set. 