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
    elements = [Higher('Eiffel Tower', 'ET', 324, 'https://images.unsplash.com/photo-1431274172761-fca41d930114'),
                Higher('Burg Khalifa', 'BK', 828, 'https://images.unsplash.com/photo-1538230947319-933cfa9486ea'),
                Higher('One World Trade Center', 'WT', 541, 'https://images.unsplash.com/photo-1541867391205-ea609f8c8750'),
                Higher('Taipei 101', 'TP', 508, 'https://images.unsplash.com/photo-1548859432-e64efebfdc00'),
                Higher('Petronas Towers', 'PT', 452, 'https://images.unsplash.com/photo-1472017053394-b29fded587cd'),
                Higher('Empire State Building', 'ES', 381, 'https://images.unsplash.com/photo-1550837725-bdcb030d1e54'),
                Higher('The Shard', 'SH', 310, 'https://images.unsplash.com/photo-1545153487-b8c2876736f8'),
                Higher('Eureka Tower', 'ES', 297, 'https://images.unsplash.com/photo-1551048950-35fd9d7524f8'),
                Higher('Big Ben', 'BB', 96, 'https://images.unsplash.com/photo-1454793147212-9e7e57e89a4f'),
                Higher('Statue of Liberty', 'SL', 93, 'https://images.unsplash.com/photo-1462567713043-5f2b089df2d1')]

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
