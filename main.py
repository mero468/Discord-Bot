
import discord
import os
import requests
import json
import random
from replit import db

# add encouragements to database
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

#delete and update items from encouragements database
def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements)>index :
    del encouragements[index]
    db["encouragements"] = encouragements

#sad words 
sad_word = ['sad','depressing','unhappy','angry','miserable','unhappy','depressed']

#Encouragement word
starter_encouragements=[
  "Cheer up!", "Hang in there",
  "You are a great person / bot!"]

#Processing the token of our bot
my_secret = os.environ['Token']

#gets quote from zen quotes database
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q']+ " -"+json_data[0]['a']
  return(quote)

client= discord.Client()

#Shows us if the bot has started
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

#When a message is sent events like these are started
@client.event
async def on_message(message):
  msg = message.content
  
  if message.author == client.user:
    return

  #$hello command
  if message.content.startswith('$hello'):
    await message.channel.send("Hello!")

  #$quote command
  if message.content.startswith('$quote'):
    quote = get_quote()
    await message.channel.send(quote)
  
  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options + db["encouragements"]

  if message.content.startswith('$new'):
    encouraging_message = msg.split('$new',1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging_message added!")
  
  if message.content.startswith('$del'):
    encouragements = []
    if "encouragements" in db.keys():
      index =int(msg.split('$del',1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)
    else:
      await message.channel.send("Encouraging message couldn't be found")


  #detect sad word
  if any(word in msg for word in sad_word):
    await message.channel.send(random.choice(starter_encouragements))

client.run(my_secret)
