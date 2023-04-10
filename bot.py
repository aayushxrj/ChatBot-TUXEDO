import discord

intents = discord.Intents.all()
# intents.members = True

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

client.run('MTA5NTAwOTQyMTQ2NzMzMjYzOA.GSwAF0.Vo42QN0MEbSDhPNlymO-E_irvDRnjmFp2ZQR5U')
