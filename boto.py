"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
from random import choice


user_curses = []


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    boto_responses = {"greeting": choice(["Hi There!", "Hello!", "Hey!", "Hola!", "Bonjour!", "Shalom!", "Wazzzzup?"]),
                      "cursing": "Profanity is unappreciated.",
                      "love": "You know what I love? Candy and puppies and motor-oil... I just love love!",
                      "confused": choice(["Does not compute...", "Yo no comprendo :/", "Say again?"]),
                      "bidding farewell": choice(["Bye!", "See ya later!", "Peace out, dude"]),
                      "bored": "Zzzzz... Ooops sorry, I must've dozed off.",
                      "hate": "Keep your head held high, kiddo! Tomorrow's another day :)",
                      "heartbroken": "Please don't leave... I'm so alone in here.",
                      "dance": "BLAST THAT BEYONCE! It's time for a dance break",
                      "secret": choice(["I love secrets!", "Juicy...", "Tell me more!!!"])}
    swear_words = ["fuck", "shit", "crap", "damn", "twat", "cock", "dick", "pussy", "cum", "prick", "cunt", "bitch",
                   "arse", "ass", "wanker", "bullocks", "bastard", "fag", "boner", "slut", "jizz", "whore"]
    jokes = choice(["How do all the oceans say hello to each other? They wave!",
                    "What do you call a bear with no teeth? A gummy bear!",
                    "Where do cows go for entertainment? The moooooo-vies!",
                    "What do you call cheese that isn’t yours? Nacho cheese!"])
    user_message = request.POST.get('msg')
    split_msg = user_message.split(" ")
    for i in range(len(user_message)):
        if i == len(user_message) - 1 and user_message[i] == "?":
            return ends_with_question(user_message)
        elif i == 0 and user_message[i].lower() == "i" or user_message[i].lower() == "i'm":
            return starts_with_i(user_message)
    for word in split_msg:
        if word in swear_words:
            user_curses.append(user_message)
            user_curses_exit()
            return json.dumps({"animation": "afraid", "msg": boto_responses["cursing"]})
        elif word == "hello" or word == "hi" or word == "hey":
            return json.dumps({"animation": "excited", "msg": boto_responses["greeting"]})
        elif word == "love" or word == "lurvvv" or word == "<3":
            return json.dumps({"animation": "inlove", "msg": boto_responses["love"]})
        elif word == "bye" or user_message.lower() == "see ya later":
            return json.dumps({"animation": "takeoff", "msg": boto_responses["bidding farewell"]})
        elif word == "so" or len(user_message) > 50:
            return json.dumps({"animation": "bored", "msg": boto_responses["bored"]})
        elif word == "hate":
            return json.dumps({"animation": "heartbroke", "msg": boto_responses["heartbroken"]})
        elif word == "sad" or word == "upset":
            return json.dumps({"animation": "crying", "msg": boto_responses["cheer up"]})
        elif word == "dance":
            return json.dumps({"animation": "dancing", "msg": boto_responses["dance"]})
        elif word == "shhh" or word == "secret":
            return json.dumps({"animation": "giggling", "msg": boto_responses["secret"]})
        elif user_message.lower() == "tell me a joke":
            return json.dumps({"animation": "laughing", "msg": jokes})
        else:
            return json.dumps({"animation": "confused", "msg": boto_responses["confused"]})


def ends_with_question(user_msg):
    for word in user_msg:
        if user_msg.lower() == "do you have a pet?":
            return json.dumps({"animation": "dog", "msg": "Sparky, my dog! He's the best!"})
        elif word == "do":
            return json.dumps(choice([{"animation": "yes", "msg": "You betcha!"},
                                      {"animation": "confused", "msg": "No way, Jose!"}]))
        elif word == "why":
            return json.dumps({"animation": "money", "msg": "It's all about the money!"})
        elif word == "how" or "what" or "when" or "where":
            return json.dumps({"animation": "giggling", "msg": choice(["You tell me, young grasshopper...",
                                                                       "The answer you seek is right in front of you..."])})


def starts_with_i(user_msg):
    for word in user_msg:
        if word.lower() == "am" or "i'm":
            return json.dumps({"animation": "ok", "msg": "Mmm, fascinating..."})
        else:
            return json.dumps({"animation": "excited", "msg": "Tell me more!"})


def user_curses_exit():
    if len(user_curses) > 3:
        exit()


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
