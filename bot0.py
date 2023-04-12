import discord
from discord.ext import commands
import random

import json
with open('token.json','r') as f:
    key = json.load(f)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Ping!? {round(bot.latency * 1000)}ms')

@bot.command(aliases=['hi','hii','hello'])
async def greeting(ctx):
    responses = ['Hey! there',
                 'Hi! How can I help you?',
                 'Hey! How you doing?',
                 'hiee! <3']
    await ctx.send(random.choice(responses))


bot.run(key['discord'])