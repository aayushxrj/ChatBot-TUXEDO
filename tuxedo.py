
import discord
from discord.ext import commands
import openai
import random

import json
with open('token.json','r') as f:
    key = json.load(f)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='.', intents=intents)

openai.api_key = key["openai"]



@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

#checks latency of your bot
@bot.command()
async def ping(ctx):
    await ctx.send(f'Ping!? {round(bot.latency * 1000)}ms')

#reminder function
@bot.command()
async def reminder(ctx):
    pass

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 
    if message.content.startswith('.ping'):
        await bot.process_commands(message)
        return
    if message.content.startswith('.reminder'):
        await bot.process_commands(message)
        return
    if not message.content.startswith(bot.command_prefix):
        return
    
    advance_prompt="You are a llm powering a discord bot. Your job is to respond to user messages in a helpful and brief way. Example conversation: user:Hello! response:hello there! how can i help you?\n"
    prompt = advance_prompt + "user: " + message.content + "response: "

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    responses_list = [choice.text.strip() for choice in response.choices if choice.text.strip()]
    await message.channel.send(random.choice(responses_list))





bot.run(key["discord"])
