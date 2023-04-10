import discord

import json
with open('token.json','r') as f:
    key = json.load(f)


intents = discord.Intents.all()


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

client.run(key["discord"])

