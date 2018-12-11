from .exceptions import *
import random

list_of_words = ['Python', 'Hello', 'rmotr']

class GuessAttempt(object):
    def __init__(self, guess, hit=None, miss=None):
        self.guess = guess.lower()
        self.hit = hit
        self.miss = miss
        if hit and miss:
            raise InvalidGuessAttempt('Cannot have both hit and miss')
        
        
    def is_hit(self):
        if self.hit:
            return True
        return False
        
    
    def is_miss(self):
        if self.miss:
            return True
        return False


class GuessWord(object):
    
    def __init__(self, answer):
        self.answer = answer.lower()
        self.masked = '*' * len(answer) 
        
        if answer == '':
            raise InvalidWordException
    
    def perform_attempt(self, guess):
        self.guess = guess.lower()
        if len(guess) > 1:
            raise InvalidGuessedLetterException
            
        new_word = ''
        if self.guess in self.answer:
            for answer_char, masked_char in zip(self.answer, self.masked):
                if answer_char == self.guess:
                    new_word += answer_char.lower()
                else:
                    new_word += masked_char.lower()

            self.masked = new_word

            return GuessAttempt(guess, hit=True)
        return GuessAttempt(guess, miss=True)


class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=None, number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
        self.word = GuessWord(self.select_random_word(word_list)) ### Why does word have be a part of GuessWord class? is it because we want to use the perform_attempt method? ###

        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        
    def is_won(self):
        return self.word.masked == self.word.answer
            
    def is_lost(self):
        return self.remaining_misses == 0
    
    def is_finished(self):
        return self.is_won() or self.is_lost()       
        
        
    def guess(self, guess):
        if self.is_finished():
            raise GameFinishedException 
        
        guess = guess.lower()     #### Why doesn't self.guess work in this case? #####
        self.previous_guesses.append(guess)
        attempt = self.word.perform_attempt(guess)
        
        if attempt.is_miss():
            self.remaining_misses -= 1
            

            
        if self.is_won():
            raise GameWonException
        
        if self.is_lost():
            raise GameLostException
            
        
            
        return attempt
    

    
    
    @classmethod
    def select_random_word(cls, word_list): ### Why does this have to be a class method? ###
        if word_list == []:
            raise InvalidListOfWordsException
        return random.choice(word_list)
