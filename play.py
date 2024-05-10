#!/usr/bin/env python3

import random
from collections import deque


def beats(one, two):
    """Return True if move one beats move two in rock-paper-scissors."""
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Player:
    """Base class for a player in rock-paper-scissors game."""
    def __init__(self):
        """Initialize player with an empty deque for storing moves."""
        self.past_moves = deque(maxlen=1)

    def move(self):
        """Default move for a player. Override in subclasses."""
        return 'rock'

    def learn(self, my_move, their_move):
        """Learn from moves played in the round."""
        self.past_moves.append((my_move, their_move))


class RandomPlayer(Player):
    """A player that chooses its move randomly."""
    def move(self):
        """Return a random move."""
        return random.choice(['rock', 'paper', 'scissors'])


class HumanPlayer(Player):
    """A player that prompts human user for a move."""
    def move(self):
        """Prompt the user for a move and validate input."""
        while True:
            choice = input("rock, paper or scissors?").lower()
            if choice in ['rock', 'paper', 'scissors']:
                return choice
            print("Please enter a valid choice.")


class ReflectPlayer(Player):
    """A player that mirrors the opponent's last move."""
    def move(self):
        """Return the opponent's last move, default to 'rock'."""
        if self.past_moves:
            return self.past_moves[-1][1]
        return 'rock'


class CyclePlayer(Player):
    """A player that cycles through the moves based on the last move."""
    def move(self):
        """Determine next move based on a cycle strategy."""
        cycle_strategy = {
            'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
        if self.past_moves:
            last_move = self.past_moves[-1][0]
            return cycle_strategy[last_move]
        return 'rock'


class Game:
    """Manage a rock-paper-scissors game between two players."""
    def __init__(self, p1, p2):
        """Initialize game with two players."""
        self.p1 = p1
        self.p2 = p2
        self.scores = {p1: 0, p2: 0}

    def update_scores(self, move1, move2):
        """Update scores based on moves."""
        if beats(move1, move2):
            self.scores[self.p1] += 1
        elif beats(move2, move1):
            self.scores[self.p2] += 1

    def get_scores(self):
        """Get current scores in a formatted string."""
        return (f"Player 1: {self.scores[self.p1]}  Player 2: "
                f"{self.scores[self.p2]}")

    def play_round(self):
        """Play one round of rock-paper-scissors."""
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"Player 1: {move1}  Player 2: {move2}")
        self.update_scores(move1, move2)
        print(self.get_scores())
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    def play_game(self):
        """Play a three-round game."""
        print("Game start!")
        for round in range(3):
            print(f"Round {round + 1}:")
            self.play_round()
        print("Game over!")
        winner = max(self.scores, key=self.scores.get)
        print(f"The winner is {'Player 1' if winner == self.p1
                               else 'Player 2'}.")


if __name__ == '__main__':
    game = Game(RandomPlayer(), HumanPlayer())
    game.play_game()
