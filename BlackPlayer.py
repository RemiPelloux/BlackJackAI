# The BlackPlayer class is an implementation of a reinforcement learning algorithm known as Sarsa(λ). It is designed
# to be used in a blackjack game, where the IA (artificial intelligence) player will learn to make optimal decisions
# based on its experiences in the game. The class has several methods, including:
#
# init: This method initializes the class with the given states, actions, learning rate alpha, discount factor gamma,
# and exploration rate epsilon. It also creates a Q-table to store the IA's estimates of the expected return for each
# state-action pair, and sets up dictionaries to map states and actions to indices and vice versa. choose_action:
# This method chooses the next action for the IA to take based on the Sarsa(λ) algorithm. With probability ε,
# it will choose a random action, and with probability 1 - ε, it will choose the action that maximizes the Q-value
# for the current state. update_q_table: This method updates the Q-table using the Sarsa(λ) update rule,
# which is q_table[s, a] = q_table[s, a] + α * (r + γ * q_table[s', a'] - q_table[s, a]). It takes in the current
# state s, action a, reward r, next state s', and next action a' as input. save_q_table: This method saves the
# Q-table to a file using np.save, so that the IA can continue learning from its experiences in future games.

import numpy as np
import random


class BlackPlayer:
	def __init__(self, states, actions, alpha, gamma, epsilon):
		# Get the number of states and actions
		num_states = len(states)
		num_actions = len(actions)

		# Initialize the Q-table to all zeros
		self.q_table = np.zeros((num_states, num_actions))
		self.num_actions = num_actions
		self.actions = actions
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon
		self.state_to_idx = {state: i for i, state in enumerate(states)}
		self.idx_to_state = {i: state for i, state in enumerate(states)}
		self.q_table = np.zeros((num_states, num_actions))

	def choose_action(self, state):
		"""Choose an action according to the Sarsa(λ) algorithm."""
		if state in self.state_to_idx:  # Check if state is a valid state
			if random.random() < self.epsilon:
				# Choose a random action with probability ε
				action = random.choice(self.actions)
			else:
				# Choose the action that maximizes Q(s, a) with probability 1 - ε
				state_idx = self.state_to_idx[state]
				action = self.actions[np.argmax(self.q_table[state_idx])]

			# If the AI player has never taken action a in state s, initialize Q(s, a) to a random value
			if self.q_table[self.state_to_idx[state], self.actions.index(action)] == 0:
				self.q_table[self.state_to_idx[state], self.actions.index(action)] = random.uniform(-1, 1)

			return action
		else:
			# If state is not a valid state, return None
			return None

	def update_q_table(self, state, action, reward, next_state, next_action):
		"""Update the Q-table using the Sarsa(λ) update rule."""
		if state not in self.state_to_idx or next_state not in self.state_to_idx:
			# If state or next_state is not a valid state, return None
			return None

		# Get the indices of the state and next_state in the Q-table
		state_idx = self.state_to_idx[state]
		next_state_idx = self.state_to_idx[next_state]

		# Get the indices of the action and next_action in the Q-table
		action_idx = self.actions.index(action)
		next_action_idx = self.actions.index(next_action)

		# Update the Q-table using the Sarsa(λ) update rule
		self.q_table[state_idx, action_idx] = self.q_table[state_idx, action_idx] + self.alpha * (
				reward + self.gamma * self.q_table[next_state_idx, next_action_idx] - self.q_table[state_idx, action_idx])

	def save_q_table(self, filename):
		"""Save the Q-table to a file."""
		np.save(filename, self.q_table)

	def load_q_table(self, filename):
		"""Load the Q-table from a file."""
		self.q_table = np.load(filename)
