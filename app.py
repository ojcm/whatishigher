from flask import Flask, render_template, request
from random import randint
import hashlib

app = Flask(__name__)

# Class to represent an object that will be compared in the game.
class Higher():
    def __init__(self, name, short_name, height, image):
        self.name = name
        self.short_name = short_name
        self.height = height
        self.image = image
        self.correct = ''

    # Is this object taller than the comparison object
    def isHigher(self, comparison):
        return self.height > comparison.height

# Class to run the game
class Game():

    # The objects that will be compared in the game
    elements = [Higher('Eiffel Tower', 'ET', 324, '/static/images/et.jpeg'),
                Higher('Burj Khalifa', 'BK', 828, '/static/images/bk.jpeg'),
                Higher('One World Trade Center', 'WT', 541, '/static/images/wt.jpeg'),
                Higher('Taipei 101', 'TP', 508, '/static/images/tp.jpeg'),
                Higher('Petronas Towers', 'PT', 452, '/static/images/pt.jpeg'),
                Higher('Empire State Building', 'ES', 381, '/static/images/es.jpeg'),
                Higher('The Shard', 'SH', 310, '/static/images/sh.jpeg'),
                Higher('Eureka Tower', 'EU', 297, '/static/images/eu.jpeg'),
                Higher('Big Ben', 'BB', 96, '/static/images/bb.jpeg'),
                Higher('Statue of Liberty', 'SL', 93, '/static/images/sl.jpeg')]

    # Compare the two options, mark the taller one as correct and vice-versa
    def markCorrect(self, option1, option2):
        if option1.isHigher(option2):
            option1.correct = 'correct'
            option2.correct = 'incorrect'
        else:
            option1.correct = 'incorrect'
            option2.correct = 'correct'

    # UNUSED.  Method to create a hash indicating whether the item is correct or not.
    def getCorrectHash(self, shortname, correct):
        return hashlib.sha256(shortname.encode('utf-8') + b'correct').hexdigest() if correct else hashlib.sha256(shortname.encode('utf-8') + b'incorrect').hexdigest()

    # UNUSED.  Method to add hashes to object to indicate their correctness.
    def markCorrectHash(self, option1, option2):
        option1.correct = self.getCorrectHash(option1.short_name, option1.isHigher(option2))
        option2.correct = self.getCorrectHash(option2.short_name, option2.isHigher(option1))

    # Pick two random objects from elements
    def getChoices(self):
        element_count = len(self.elements)

        # If there is only one element then we get stuck in an infinite
        # while-loop.  Assert to avoid that.
        assert(element_count > 1)

        # Get the two options
        first_option = randint(0, element_count-1)
        second_option = randint(0, element_count-1)
        while second_option == first_option:
            second_option = randint(0, element_count-1)

        # Mark one option correct and one incorrect
        self.markCorrect(self.elements[first_option], self.elements[second_option])
        return [self.elements[first_option], self.elements[second_option]]

    # Run the game
    def runGame(self, answer_text='', **kwargs):
        # Set debug_text if we need to output some debugging info to browser
        debug_text = kwargs['debug'] if 'debug' in kwargs else False

        # Choose two objects
        choices = self.getChoices()

        # Render game
        return render_template('higher.html',
                               debug=debug_text,
                               response=answer_text,
                               a1=choices[0],
                               a2=choices[1])

# A class to represent a response to the user.  Usually 'correct'/True or 'incorrect'/False.
class Response():
    def __init__(self, text, positive):
        self.text = text
        self.positive = positive

# Initial route.  Display the game with no responses.
@app.route('/')
def higher_game():
    return Game().runGame()

# Recurring route. Display result from previous round and new question.
@app.route('/answer', methods=['POST'])
def answer():
    # Check if user pressed the correct button (correct) or correct image (correct.x)
    if 'correct' in request.form or 'correct.x' in request.form:
        response = Response('Correct! :)', True)
    else:
        response = Response('Incorrect. :(', False)

    # start a new game
    return Game().runGame(response)
    # start a new game and display some debugging information
    #return Game().runGame(response, debug=request.form)
