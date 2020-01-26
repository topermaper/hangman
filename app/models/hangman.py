from random import choice
from app.models.game import Game
from app import app
from collections import OrderedDict

class Hangman(Game):

    def __init__(self, user_id):
        super().__init__(user_id)

    def validate_user_guess(self, new_user_guess):
        # This only accepts the same string plus one character
        if new_user_guess[:-1] != self.get_user_guess():
            return False

        # Last character is the last guess, check if already there
        if new_user_guess[-1] in self.get_user_guess():
            return False

        return True

    # Main method, new_user_guess has to be a list
    def set_user_guess(self, new_user_guess):

        if not self.validate_user_guess(new_user_guess):
            return False

        self.user_guess = ''.join(new_user_guess)

        if new_user_guess[-1] not in self.secret_word:
            self.misses += 1
            self.update_user_score(False)
        else:
            self.update_user_score(True)
 
        # Update the game status
        self.update_game_status()

        return True

    def update_user_score(self,user_guessed):
        # User guessed
        if user_guessed:
            # Add 1 to the score
            self.score += 1
            # Multiply score per multiplier
            self.score = self.score * self.multiplier
            # Increase multiplier
            self.multiplier += 1
        # User did not guess
        else:
            # Reset multiplier
            self.multiplier = 1

    def update_game_status(self):
        # User LOST the game
        if self.misses > app.config['ALLOWED_MISSES']:
            self.status = 'LOST'
        # All the characters in the user guess list, user WON
        elif all(c in self.user_guess for c in self.secret_word):
            self.status = 'WON'
        # Game is still ACTIVE
        else:
            self.status = 'ACTIVE'

    def get_user_guess(self):
        return list(self.user_guess)

    def get_word_mask(self):
        word_mask = []
        for i in range(len(self.secret_word)):
            if self.secret_word[i] not in self.user_guess:
                word_mask.append(i)

        return word_mask