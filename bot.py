import discord

import json
with open('token.json','r') as f:
    key = json.load(f)


intents = discord.Intents.all()


bot = discord.bot(intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

bot.run(key["discord"])

