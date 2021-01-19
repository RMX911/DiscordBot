import discord
import os
import requests
import json
import random
from replit import db


client = discord.Client()

sad_words = ["sucks","sad", "depressed", "unhappy", "angry", "depressing"]

starter_encouragements = ["LOL", "hahaha!", "wow lol"]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")

    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "\n -" + json_data[0]['a']

    return quote

def add_new_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db['encouragements'] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def reomve_encouragements(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements



@client.event
async def on_ready():
    print(f"We are live @ {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello! Welcome to the Matrix!')

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
      options = starter_encouragements
      if "encouragements" in db.keys():
        options = options + db["encouragements"]
        
      if any(word in message.content for word in sad_words):
          await message.channel.send(random.choice(options))
    
    if message.content.startswith('$add'):
      encouraging_message = message.content.split("$add ",1)[1]
      add_new_encouragements(encouraging_message)
      await message.channel.send("YO! thanks for adding.")
    
    if message.content.startswith("$del"):
      encouragements =[]
      if "encouragements" in db.keys():
        index = int(message.content.split("$del",1)[1])
        reomve_encouragements(index)
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)
    
    if message.content.startswith('$list'):
      encouragements =[]
      if "encouragements" in db.keys():
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)
    
    if message.content.startswith('$response'):
      flag = message.content.split("$response ",1)[1]

      if flag.lower() == 'true':
        db["responding"] = True
        await message.channel.send("Response Mode ON")
      else:
        db["responding"] = False
        await message.channel.send("Response Mode OFF")


client.run(os.getenv('TOKEN'))
