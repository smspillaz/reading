# Feasible Hierarhical RL for BabyAI

 - BabyAI
   - Can arbitrarily set up the environment and determine whether or
     not the environment is solveable
   - Observability:
     - Entire environment
     - Just the view of the agent
     - Just the pixels of the agent's view

 - Use the "goal-conditioned self-play" method
   - Need to generate the goals somehow
     - Easier to make a canonical representation when we see the
       entire image environment, but then we're fixed to the entire
       environment
   - Alice' loss function:
     - A combination of how successful Bob is at the task, plus a penalty
       for generating more complex environments
     - This can be based on how long it would take an optimal Bob to solve
       the task, plus some sort of penalty every time you place an object
       in the environment
   - Bob's loss function:
     - How many steps did you take to solve the task?
     - Need some sort of upper bound on steps so that it doens't take
       forever. Have to compute this with the environment somehow(?)

   - Future: Alice encodes the environment somehow, but need to be
             careful with backprop since we don't want to generate
             adversarial encodings (rather we want the encoding
             that is most helpful for bob).
