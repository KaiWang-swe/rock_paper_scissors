#!/usr/bin/env python3

import random
from collections import deque

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

moves = ['rock', 'paper', 'scissors']

"""The Player class is the parent class for all of the Players
in this game"""



class Player:

    def __init__(self) -> None:
        # Use a deque with a limited length to store past moves for enhanced performance.
        # Currently set to remember only the last move, but can be expanded for complex pattern recognition in future developments.
        self.past_moves = deque(maxlen=1)

    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        # Store each pair of my move and their move as a tuple in past_moves.
        self.past_moves.append((my_move, their_move))
        

# I plan to use composition instead of inheritance in future developments.
# Due to time constraints, I will maintain the current implementation for now.
class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
    
    def move(self):
        return random.choice(moves)
    
class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self):
        return validated_input()

class ReflectPlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self):
        # return opponent's last move
        return self.past_moves[-1][1]

class CyclePlayer(Player):
    def __init__(self):
        super().__init__()
    
    def move(self):    
        # I use a hashmap to store the corresponding move
        cycle_strategy = {'rock':'paper', 'paper':'scissors', 'scissors':'rock'}
        # Remembers what move it played last round, and cycles through the different moves.
        return cycle_strategy[self.past_moves[-1][0]]



def validated_input():
    """
    Prompts the user to enter a choice from 'rock', 'paper', or 'scissors'.

    This function ensures that the user inputs a valid choice. If the input is not valid,
    the user is prompted repeatedly until a valid choice is entered. The function
    converts all inputs to lowercase to ensure case insensitivity.

    Returns:
        str: The validated choice input by the user, converted to lowercase.
    """
    choice = input("rock, paper or scissors?").lower()
    if not choice in moves:
        print("Please enter a valid choice.")
        validated_input()
    else:
        return choice


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.scores = {self.p1:0, self.p2:0}

    def update_scores(self,move1,move2):
        if beats(move1,move2):
            self.scores[self.p1]+=1
        elif beats(move2,move1):
            self.scores[self.p2]+=1
    

    def get_scores(self):
        return f"Player 1: {self.scores[self.p1]}  Player 2: {self.scores[self.p2]}"

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"Player 1: {move1}  Player 2: {move2}")
        self.update_scores(move1,move2)
        print(self.get_scores())
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    def play_game(self):
        print("Game start!")
        for round in range(3):
            print(f"Round {round}:")
            self.play_round()
        print("Game over!")
        winner = max(self.scores, key=lambda k: self.scores[k])
        print(f"The winner is {winner}!".replace(self.p1,"Player1").replace(self.p2,"Player2"))


if __name__ == '__main__':
    game = Game(RandomPlayer(), HumanPlayer())
    game.play_game()

