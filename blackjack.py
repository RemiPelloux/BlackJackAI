import json
import random
from collections import defaultdict

# Import my ia
import BlackPlayer


class Card:
	def __init__(self, suit, value):
		self.suit = suit
		self.value = value


class Deck:
	def __init__(self):
		self.cards = []
		for suit in ['H', 'S', 'D', 'C']:
			for value in range(1, 14):
				self.cards.append(Card(suit, value))

	def shuffle(self):
		random.shuffle(self.cards)

	def draw(self):
		return self.cards.pop()


class Player:
	def __init__(self):
		self.hand = []
		self.value = 0
		self.aces = 0
		# load balance from the file if it exists
		self.balance = 0
		try:
			with open('balance.json', 'r') as f:
				self.balance = json.load(f)
		except FileNotFoundError:
			self.balance = 1000

	def draw(self, card):
		self.hand.append(card)
		self.value += card.value
		if card.value == 1:
			self.aces += 1
		self.adjust_for_ace()

	def adjust_for_ace(self):
		while self.value > 21 and self.aces:
			self.value -= 10
			self.aces -= 1


class BlackjackGame:
	def __init__(self):
		# Define the actions as integers
		self.HIT = 0
		self.STAND = 1
		self.actions = [self.HIT, self.STAND]  # Create a list of actions

		self.player_ia = BlackPlayer.BlackPlayer(states=states, actions=self.actions, alpha=0.1, gamma=0.9, epsilon=0.1)

		self.deck = Deck()
		self.deck.shuffle()
		self.player = Player()
		self.dealer = Player()
		self.bet = 0

	def reward(self, player, dealer, outcome):
		"""Determine the reward for a given game outcome."""
		if outcome == 'player busts':
			return -1
		elif outcome == 'dealer busts':
			return 1
		elif outcome == 'player wins':
			# Return a higher reward if the player's hand value is higher
			return 1 + 0.1 * (player.value - dealer.value)
		elif outcome == 'dealer wins':
			# Return a lower penalty if the dealer's hand value is higher
			return -1 - 0.1 * (dealer.value - player.value)
		else:  # outcome == 'tie'
			return 0

	def update_balance(self, result):
		"""Update the player's balance based on the result of the game."""
		if result == 'win':
			self.player.balance += self.bet
		elif result == 'lose':
			self.player.balance -= self.bet
		else:
			pass

	def save_balance(self, balance=None):
		"""Save the player's balance to a json formatted file. balance : int"""
		if balance:
			self.player.balance = balance
		with open('balance.json', 'w') as f:
			json.dump(self.player.balance, f)

	def load_balance(self):
		"""Load the player's balance from a json formatted file.
		if the file does not exist, create it and set the balance to 1000."""
		try:
			with open('balance.json', 'r') as f:
				self.player.balance = json.load(f)
		except FileNotFoundError:
			self.save_balance(1000)

	def get_state(self):
		pass

	def play(self):
		self.bet = random.randint(10, 50)

		self.player.draw(self.deck.draw())
		self.player.draw(self.deck.draw())
		self.dealer.draw(self.deck.draw())
		self.dealer.draw(self.deck.draw())

		# Print the player's hand and the total value
		print("Player's hand: ")
		for card in self.player.hand:
			print(card.suit, card.value)
		print("Player's total value: ", self.player.value)
		# Print the dealer's hand and the total value
		print("Dealer's hand: ")
		for card in self.dealer.hand:
			print(card.suit, card.value)
		print("Dealer's total value: ", self.dealer.value)

		# Get the initial state of the game
		state = self.get_state()

		while self.player.value < 21:
			# Choose an action using the BlackPlayer's choose_action() method
			action = self.player_ia.choose_action(state)
			if action == self.HIT:
				self.player.draw(self.deck.draw())
				print('Player: {}'.format(self.player.value))
				if self.player.value > 21:
					# Player busts
					outcome = 'player busts'
					break
			else:
				break

		# Determine the reward for the chosen action
		reward = self.reward(self.player, self.dealer, outcome)

		# Update the Q-table using the BlackPlayer's update_q_table() method
		next_state = self.get_state()  # Get the next state
		self.player_ia.update_q_table(state, action, reward, next_state)

		# While the dealer's value is less than 17, keep drawing unless the player has already busted and beat the
		# player's value
		while self.dealer.value < 17 and self.dealer.value < self.player.value:
			self.dealer.draw(self.deck.draw())
			print('Dealer: {}'.format(self.dealer.value))

		if self.dealer.value > 21:
			# Dealer busts
			outcome = 'dealer busts'
		elif self.player.value > self.dealer.value:
			# Player wins
			outcome = 'player wins'
		elif self.player.value < self.dealer.value:
			# Dealer wins
			outcome = 'dealer wins'
		else:  # Tie
			outcome = 'tie'

		# Determine the final reward for the game
		reward = self.reward(self.player, self.dealer, outcome)

		# Update the Q-table using the final reward and the current state
		self.player_ia.update_q_table(state, action, reward, None)

		# Show the player's hand and the total value
		print('Player\'s hand: ')
		for card in self.player.hand:
			print(card.suit, card.value)
		print('Player\'s total value: ', self.player.value)
		# Show the dealer's hand and the total value
		print('Dealer\'s hand: ')
		for card in self.dealer.hand:
			print(card.suit, card.value)
		print('Dealer\'s total value: ', self.dealer.value)

		if outcome == 'player busts':
			print('Player busts!')
		elif outcome == 'dealer busts':
			print('Dealer busts!')
		elif outcome == 'player wins':
			print('Player wins!')
		elif outcome == 'dealer wins':
			print('Dealer wins!')
		else:  # outcome == 'tie'
			print('Tie!')


if __name__ == '__main__':
	game = BlackjackGame()
	game.load_balance()
	game.play()