####################################
##  -------  Encourage!  -------  ##
####################################
#  - Imports
import discord
import os
import requests
import json
import random as rand
from replit import db
from keep_alive import keep_alive

client = discord.Client()

###  ====== ARRAYS ====== ###

sad_words = [
    'sad', 'depression', 'unhappy', 'angry', 'miserable', 'depressing',
    'upset', 'cant take it', 'limit', 'edge', 'never', 'T-T', 'T_T',
    'feeling down'
]

starter_encouragements = [
    'Cheer Up!',
    'Hang in there.',
    'You are a good person',
    'Try to relax. Its gonna be OK',
    'It gets better! ',
    'You are doing very well today, and I am glad you are alive.',
    'Things may suck now, but that doesnt mean theyll suck forever',
    'I cant say things will get better, but youre not going through this alone',
    'Ill be holding your hand as you fight',
    'Sometimes the demons just. . . win'
    'Heroes usually get defeated first before theyre declared victors later. Im proud of you, good job.',
    'Nobody is perfect. Its alright to feel this way.',
]
#### --- CREDIT TO wheeze#6191 FOR ENCOURAGEMENT HELP!! --- ####

if "responding" not in db.keys():
    db["responding"] = True

# -- Standard Greetings -- #
greetings = [
    'Hi',
    'Hello',
    'hello',
    'Greetings',
    'greetings',
    'Sup',
    'sup',
    'wassup',
    'Wassup',
    'Ayo',
    'ayo',
]

# -- 8 ball Answers. -- #
answers = [
    'It is certain', 'It is decidedly so', 'Without a doubt',
    'Yes – definitely', 'You may rely on it', 'As I see it, yes',
    'Most likely', 'Outlook good', 'Yes Signs point to yes', 'Reply hazy',
    'try again', 'Ask again later', 'Better not tell you now',
    'Cannot predict now', 'Concentrate and ask again', 'Dont count on it',
    'My reply is no', 'My sources say no', 'Outlook not so good',
    'Very doubtful'
]


#### --- Ready Message --- ####
@client.event
async def on_ready():  # This will print whent the bot is online
    print('Im ready to love as {0.user}'.format(client))


#Positivity Quote
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragements(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


### --- USER Input-Controlled --- ###


# User message activated responses
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # shortening common args make it easier to code! ^-^ #
    msg = message.content
    mch = message.channel

    if msg.startswith('$help'):
        await mch.send("$inpire for a quote, " + "$8ball for answers, " +
                       "$d20 to roll for luck, " +
                       "$add to my encouragements list!"
                       "T_T Shut me up ig with $responding")
        await mch.send("What you do want to do? ")

    # - Minus the $help command most of these are using the earlier arrays - #
    # - to either detect or give an answer! - #

    if msg.startswith('$inspire'):
        quote = get_quote()
        await mch.send(quote)

    if msg.startswith('$8ball'):
        await mch.send(rand.choice(answers))

    if msg.startswith('$d20'):  # - I forgot async existed =_= - #
        await mch.send(rand.randrange(1, 20))

    if db["responding"]:
        options = starter_encouragements
        # Combines the standard plus user input
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        if msg.startswith("$new"):
            encouraging_message = msg.split("$new ", 1)[1]
            update_encouragements(encouraging_message)
            await mch.send("New encouraging message added! Thank you!")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del ", 1)[1])
            delete_encouragements(index)
            encouragements = db["encouragements"]
        await mch.send(encouragements)

    if any(word in msg for word in sad_words):
        await mch.send(rand.choice(options))

    if any(word in msg for word in greetings):
        await mch.send(rand.choice(greetings))

    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await mch.send(encouragements)

    if msg.startswith("$responding"):
        value = msg.split("$responding", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await mch.send("Responding is on! :D")
        else:
            db["responding"] = True
            await mch.send("Responding is off! :(")

    # -- Ill Make an array for this soon! -- #
    #     -- Or not who knows -- #
    if msg.startswith('Good morning'):
        await mch.send('Good morning! Have a lovely day!')


# - TOKEN is hidden in an .env file, and keep_alive() consistently pings web server - #
keep_alive()
client.run(os.getenv('TOKEN'))
