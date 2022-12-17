Blackjack Game with IA - WIP - Learning project
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
