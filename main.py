
import discord
import os
import requests
import json
import random
from replit import db



def update_Encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(encouraging_message):









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

  if message.content.startswith('$hello'):
    await message.channel.send("Hello!")
  
  if message.content.startswith('$quote'):
    quote = get_quote()
    await message.channel.send(quote)

  if any(word in msg for word in sad_word):
    await message.channel.send(random.choice(starter_encouragements))
client.run(my_secret)
