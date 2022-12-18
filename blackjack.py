import json
import random
from collections import defaultdict
import BayesianOptimization
# Import my ia
import BlackPlayer

outcomes = {
	"player busts": 0,
	"dealer busts": 0,
	"player wins": 0,
	"dealer wins": 0,
	"player stands": 0,
	"tie": 0,
	"reward": 0
}
total_reward = 0.00


class Card:
	def __init__(self, suit, value):
		self.suit = suit
		self.value = value


class Deck:
	def __init__(self):
		self.cards = []
		for suit in ['H', 'S', 'D', 'C']:  # H=Hearts, S=Spades, D=Diamonds, C=Clubs
			for value in range(1, 14):  # Card values range from 1 (Ace) to 13 (King)
				self.cards.append(Card(suit, value))

	def shuffle(self):
		random.shuffle(self.cards)

	def draw(self):
		return self.cards.pop()

	def reset(self):
		self.cards = []
		for suit in ['H', 'S', 'D', 'C']:
			for value in range(1, 14):
				self.cards.append(Card(suit, value))


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
		if card.value == 1:
			self.aces += 1
		self.adjust_for_ace()
		self.adjust_for_figures(card)
		self.value += card.value
		self.hand.append(card)

	def adjust_for_ace(self):
		# Return if the player has already busted
		if self.value > 21:
			return
		while self.value > 21 and self.aces:
			self.value -= 10
			self.aces -= 1

	def adjust_for_figures(self, card):
		if card.value > 10:
			card.value = 10

	def reset(self):
		self.hand = []
		self.value = 0
		self.aces = 0


class BlackjackGame:
	def __init__(self):
		# Define the actions as integers
		self.HIT = 0
		self.STAND = 1
		self.actions = [self.HIT, self.STAND]

		# Define the possible hand values and visible cards
		hand_values = range(4, 22)
		visible_cards = range(1, 11)

		# Create a list of states as tuples of hand values and visible cards
		states = [(hand_value, visible_card) for hand_value in hand_values for visible_card in visible_cards]

		# Initialize the current state and action
		current_state = random.choice(states)  # Choose a random state
		current_action = random.choice(self.actions)  # Choose a random action

		self.player_ia = BlackPlayer.BlackPlayer(states=states, actions=self.actions, alpha=0.5, gamma=0.8, epsilon=0.3)

		self.deck = Deck()
		self.deck.shuffle()
		self.player = Player()
		self.dealer = Player()
		self.bet = 0

	def reward(self, player, dealer, outcome):
		"""Determine the reward for a given game outcome."""
		if outcome == 'player busts':
			return -5 - 0.1 * (player.value - 21) - 0.01 * (dealer.value - 21)
		elif outcome == 'dealer busts':
			return 1 + 0.1 * (player.value - 21) + 0.01 * (dealer.value - 21)
		elif outcome == 'player wins':
			# Return a higher reward if the player's hand value is close to 21
			return 1 + 0.1 * (player.value - dealer.value) + 0.5 * (21 - player.value)
		elif outcome == 'dealer wins':
			# Return a lower penalty if the dealer's hand value is higher
			return -1 - 0.1 * (dealer.value - player.value) - 0.5 * (dealer.value - 21)
		elif outcome == 'player stands':
			if player.value > dealer.value:
				return 3 + 0.5 * (21 - player.value)
			elif player.value == dealer.value:
				return 0
			else:
				return -1 - 0.5 * (dealer.value - 21)
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

	def update_outcome(self, outcome, reward):
		"""Save the outcome and reward of the game."""
		outcomes[outcome] += 1
		global total_reward
		outcomes['reward'] += reward

	def save_outcome(self):
		"""Save the outcomes to a json formatted file."""
		with open('outcomes.json', 'w') as f:
			json.dump(outcomes, f)

	def load_outcome(self):
		"""Load the outcome of the game from a json formatted file."""
		try:
			with open('outcome.json', 'r') as f:
				return json.load(f)
		except FileNotFoundError:
			return None

	def get_state(self):
		"""Return the current state of the game, which includes the player's hand value, the dealer's hand value,
		and the visible card of the dealer. """
		player_value = self.player.value
		dealer_value = self.dealer.hand[0].value
		return player_value, dealer_value

	def play(self):
		# try to load q_table from file
		try:
			self.player_ia.load_q_table('q_table.npy')
		except FileNotFoundError:
			pass

		self.bet = 1
		outcome = None
		action = None

		# Deal two cards to the player and the dealer
		print()
		print('>/ New game')
		print('> Your balance is ${}'.format(self.player.balance))
		print('> Your bet is ${}'.format(self.bet))

		self.player.draw(self.deck.draw())
		self.player.draw(self.deck.draw())
		self.dealer.draw(self.deck.draw())
		self.dealer.draw(self.deck.draw())

		# Print the player's hand and the total value
		print("> Player's hand: ")
		for card in self.player.hand:
			print(card.suit, card.value)
		print("> Player's total value: ", self.player.value)
		# Print the dealer's hand and the total value
		print("> Dealer's hand: ")
		print(self.dealer.hand[0].suit, self.dealer.hand[0].value)
		print("> Dealer's total value: ", self.dealer.hand[0].value)
		# Get the initial state of the game
		state = self.get_state()

		# if the player's hand value is 21, the player wins
		if self.player.value == 21:
			outcome = 'player wins'
			self.update_balance('win')
			print('> BLAAACKJACK Player wins!')
			self.save_balance()
			return outcome
		else:
			while self.player.value < 21:
				# Choose an action using the BlackPlayer's choose_action() method
				action = self.player_ia.choose_action(state)
				if action == self.HIT:
					self.player.draw(self.deck.draw())
					print('> Player: {}'.format(self.player.value))
					if self.player.value > 21:
						# Player busts
						outcome = 'player busts'
						self.update_balance('lose')
						print('> Player busts!')
						self.save_balance()
						# Determine the final reward for the game
						reward = self.reward(self.player, self.dealer, outcome)
						# Update the Q-table using the final reward and the current state
						self.player_ia.update_q_table(state, action, reward, None, None)
						return outcome
				else:
					outcome = 'player stands'
					break

		# Determine the reward for the chosen action
		reward = self.reward(self.player, self.dealer, outcome)

		# Choose the next action according to the Sarsa(λ) algorithm
		next_state = self.get_state()  # Get the next state
		next_action = self.player_ia.choose_action(next_state)  # Choose the next action

		# Update the Q-table using the BlackPlayer's update_q_table() method
		self.player_ia.update_q_table(state, action, reward, next_state, next_action)

		# While the dealer's value is less than 17, keep drawing unless the player has already busted and beat the
		# player's value
		while self.dealer.value < 17 and self.dealer.value < self.player.value:
			self.dealer.draw(self.deck.draw())
			print('> Dealer: {}'.format(self.dealer.value))

		if self.dealer.value > 21:
			# Dealer busts
			outcome = 'dealer busts'
			self.update_balance('win')
		elif self.player.value > self.dealer.value:
			# Player wins
			outcome = 'player wins'
			self.update_balance('win')
		elif self.player.value < self.dealer.value:
			# Dealer wins
			outcome = 'dealer wins'
			self.update_balance('lose')
		else:  # Tie
			outcome = 'tie'

		# Determine the final reward for the game
		reward = self.reward(self.player, self.dealer, outcome)

		# Update the Q-table using the final reward and the current state
		self.player_ia.update_q_table(state, action, reward, None, None)

		# Show the player's hand and the total value
		print('>> Player\'s hand: ')
		for card in self.player.hand:
			print(card.suit, card.value)
		print('>> Player\'s total value: ', self.player.value)
		# Show the dealer's hand and the total value
		print()
		print('>> Dealer\'s hand: ')
		for card in self.dealer.hand:
			print(card.suit, card.value)
		print('>> Dealer\'s total value: ', self.dealer.value)

		if outcome == 'player busts':
			print('>> Player busts !')
			self.update_balance('lose')
		elif outcome == 'dealer busts':
			print('>> Dealer busts !')
			self.update_balance('win')
		elif outcome == 'player wins':
			print('>> Player wins !')
			self.update_balance('win')
		elif outcome == 'dealer wins':
			print('>> Dealer wins !')
			self.update_balance('lose')
		else:  # outcome == 'tie'
			print('>> Tie !')

		self.save_balance()
		print()
		print('Your balance is ${}'.format(self.player.balance))
		print()
		self.player_ia.save_q_table('q_table.npy')
		self.update_outcome(outcome, reward)

	def reset(self):
		self.deck = Deck()
		self.deck.shuffle()
		self.player = Player()
		self.dealer = Player()


if __name__ == '__main__':
	game = BlackjackGame()
	game.load_balance()
	# play 100 games
	for i in range(100):
		if game.player.balance < 10:
			print('You are out of money!')
			break
		game.play()
		game.reset()
	game.save_balance()
	game.save_outcome()
