Blackjack Game with RL - WIP 
======================

This is an implementation of the game of blackjack with an IA player that uses reinforcement learning to make optimal decisions.

Requirements
------------

-   Python 3
-   numpy
-   random

How to play
-----------

To play the game, run the `main.py` file. The game will start with an initial balance of 1000, and you will be prompted to enter your bet for the round. Then you will be given the option to hit or stand. The IA player will also make its decisions according to the Sarsa(λ) algorithm. The game will continue until either the player or the dealer busts or the player stands. The outcome of the game will be displayed and the player's balance will be updated accordingly.

How the IA learns
-----------------

The IA player uses a Q-table to store its estimates of the expected return for each state-action pair. The Q-table is initialized to all zeros, and is updated using the Sarsa(λ) update rule: q_table[s, a] = q_table[s, a] + α * (r + γ * q_table[s', a'] - q_table[s, a]). The learning rate α, the discount factor γ, and the exploration rate ε are all adjustable parameters that can be set in the `BlackPlayer` class.

Additional features
-------------------

-   The player's balance is saved to a file in JSON format, so that it can be carried over to future games.
-   The IA player's Q-table is saved to a file using numpy's `save` function, so that it can continue learning from its experiences in future games.


RoadMap
---------

1. Import the necessary libraries, such as **`numpy`** for working with arrays and **`random`** for generating random numbers.
2. Define a set of states that the IA can be in. A state could be the current hand value and the visible card of the dealer. For example, a state could be "player hand value: 18, dealer hand value: 5". You could represent this state as a tuple, such as (18, 5).
3. Define a set of actions that the IA can take. These could be "hit" or "stand". You could represent these actions as integers, with 0 representing "hit" and 1 representing "stand".
4. Initialize a Q-table with the states as rows and the actions as columns. The Q-table will be used to store the IA's estimates of the expected return for each state-action pair. You can initialize the Q-table to all zeros using **`q_table = np.zeros((num_states, num_actions))`**, where **`num_states`** is the number of states and **`num_actions`** is the number of actions.
5. Define a learning rate α and a discount factor γ. These will be used to update the Q-table as the IA learns from its experiences. You can set these values to any reasonable values, such as α = 0.1 and γ = 0.9.
6. Before the game starts, initialize the current state s and the current action a. You can choose the initial state and action randomly.
7. While the game is in progress, have the IA choose its next action according to the Sarsa(λ) algorithm:
8. If the IA has never taken action a in state s, initialize Q(s, a) to a random value. You can generate a random value using **`random.uniform(-1, 1)`**.
9. With probability ε, choose a random action a'. With probability 1 - ε, choose the action that maximizes Q(s, a). You can use the **`random.random()`** function to generate a random number between 0 and 1, and use this to determine whether to choose a random action or the action that maximizes Q(s, a).
10. Take action a and observe the reward r and the new state s'.
11. Choose the next action a' according to the Sarsa(λ) algorithm (as described in step 2).
12. Update the Q-table using the Sarsa(λ) update rule: **`q_table[s, a] = q_table[s, a] + alpha * (r + gamma * q_table[s', a'] - q_table[s, a])`**.
13. Set the current state to s' and the current action to a'.
14. After the game is over, save the Q-table to a file using **`np.save('q_table.npy', q_table)`** so that the IA can continue learning from its experiences in future games.
