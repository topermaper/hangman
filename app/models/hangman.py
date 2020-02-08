from random import choice
from app.models.game import Game
from app import app
from collections import OrderedDict

class Hangman(Game):

    @property
    def user_guess_set(self):
        return set(self.user_guess)
    
    @property
    def user_guess_list(self):
        return list(self.user_guess)

    def __init__(self, user_id):
        super().__init__(user_id)

    # Accepts either a single guess character or full list with all guesses
    def get_valid_user_guess(self, new_user_guess):

        # It's a list, we extract to new guess character using sets
        if isinstance(new_user_guess, list):
            new_set = set(new_user_guess)
            diff = new_set.difference(self.user_guess_set)

            if not (new_set.issuperset(self.user_guess_set) and len(diff) == 1):
                return None

            new_user_guess = diff.pop()

        elif isinstance(new_user_guess, str):
            # Guess already attempted
            if new_user_guess in self.user_guess_set:
                return None

        # The new user guess should be a single character
        if len(new_user_guess) != 1:
            return None

        return new_user_guess

    # Main method, new_user_guess. Accepts either list or string
    def set_user_guess(self, new_user_guess):

        guess_character = self.get_valid_user_guess(new_user_guess)

        # new_user_guess is not valid, cancel the operation
        if guess_character == None:
            return False

        # Guess is valid, add guess character
        self.user_guess += guess_character

        if guess_character not in self.secret_word:
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

    def get_word_mask(self):
        word_mask = []
        for i in range(len(self.secret_word)):
            if self.secret_word[i] not in self.user_guess:
                word_mask.append(i)

        return word_mask