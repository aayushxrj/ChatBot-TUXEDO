
import discord
from discord.ext import commands
import openai

import json
with open('token.json','r') as f:
    key = json.load(f)

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.presences = True

client = commands.Bot(command_prefix='!', intents=intents)

openai.api_key = key["openai"]

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return 
    
    prepend="You are a llm powering a discord bot. Your job is to respond to user messages in a helpful and brief way. Example conversation: user:Hello! response:hello there! how can i help you?\n"
    prompt = prepend + "user: " + message.content + " response: "
    print(prompt)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )

    await message.channel.send(response.choices[0].text)

client.run(key["discord"])
