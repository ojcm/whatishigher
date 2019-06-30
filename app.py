from flask import Flask, render_template, request
import hashlib
import random

app = Flask(__name__)

# Class to represent an object that will be compared in the game.
class Higher():
    def __init__(self, name, short_name, height, image):
        self.name = name
        self.short_name = short_name
        self.height = height
        self.image = image

    # Is this object taller than the comparison object
    def isHigher(self, comparison):
        return self.height > comparison.height

# Class to run the game
class Game():

    # The objects that will be compared in the game
    elements = {'ET': Higher('Eiffel Tower', 'ET', 324, '/static/images/et.jpeg'),
                'BK': Higher('Burj Khalifa', 'BK', 828, '/static/images/bk.jpeg'),
                'WT': Higher('One World Trade Center', 'WT', 541, '/static/images/wt.jpeg'),
                'TP': Higher('Taipei 101', 'TP', 508, '/static/images/tp.jpeg'),
                'PT': Higher('Petronas Towers', 'PT', 452, '/static/images/pt.jpeg'),
                'ES': Higher('Empire State Building', 'ES', 381, '/static/images/es.jpeg'),
                'SH': Higher('The Shard', 'SH', 310, '/static/images/sh.jpeg'),
                'EU': Higher('Eureka Tower', 'EU', 297, '/static/images/eu.jpeg'),
                'BB': Higher('Big Ben', 'BB', 96, '/static/images/bb.jpeg'),
                'SL': Higher('Statue of Liberty', 'SL', 93, '/static/images/sl.jpeg')}

    # Compare the two options, mark the taller one as correct and vice-versa
    def markCorrect(self, option1, option2):
        if option1.isHigher(option2):
            option1.correct = 'correct'
            option2.correct = 'incorrect'
        else:
            option1.correct = 'incorrect'
            option2.correct = 'correct'

    # Pick two random objects from elements
    def getChoices(self):

        # If there is only one element then we get stuck in an infinite
        # while-loop.  Assert to avoid that.
        assert(len(self.elements) > 1)

        # Get the two options
        first_option = random.choice(list(self.elements.keys()))
        second_option = random.choice(list(self.elements.keys()))
        while second_option == first_option:
            second_option = random.choice(list(self.elements.keys()))

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
@app.route('/answer', methods=['POST', 'GET'])
def answer():
    game = Game()
    answer = request.args.get('answer', None)
    other = request.args.get('other', None)

    if game.elements[answer].isHigher(game.elements[other]):
        response = Response('Correct! :)', True)
    else:
        response = Response('Incorrect. :(', False)

    # start a new game
    return game.runGame(response)
    # start a new game and display some debugging information
    #return Game().runGame(response, debug=request.form)

