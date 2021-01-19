import discord
import os
import requests
import json
import random

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "depressing"]

starter_encouragements = ["LOL", "hahaha!", "wow lol"]


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")

    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "\n -" + json_data[0]['a']

    return quote


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

    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))


client.run(os.getenv('TOKEN'))
