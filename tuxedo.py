
import discord
from discord.ext import commands
import openai
import random
import datetime 
import asyncio

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

#hello function
@bot.command()
async def hello(ctx):
    author = ctx.author.name
    await ctx.send(f"Hello {author}!")

#checks latency of your bot
@bot.command()
async def ping(ctx):
    await ctx.send(f'Ping!? {round(bot.latency * 1000)}ms')

#clears messages in the channel
@bot.command()
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)

#reminder function
@bot.command()
async def reminder(ctx,*,reminder_str):                    # * is splat operator (Helps to store the string passes in reminder_str)
    try:
        time_str, date_str = reminder_str.split(" ")
        time = datetime.datetime.strptime(time_str, "%H:%M")
        date = datetime.datetime.strptime(date_str, "%d/%m/%Y")

        #logic
        now = datetime.datetime.now()
        delay = (datetime.datetime.combine(date, time.time()) - now).total_seconds()
        if(delay<0):
            await ctx.send("Can't set a reminder for past ;)")
        else:
            await ctx.send("Reminder Successfull.")
            await asyncio.sleep(delay)
            await ctx.send(f"{ctx.author.mention}, you have a reminder!")
    
    except:
        await ctx.send('Reminder unsuccessfull - Wrong format.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 
    if message.content.startswith('.ping'):
        await bot.process_commands(message)
        return
    if message.content.startswith('.hello'):
        await bot.process_commands(message)
        return
    if message.content.startswith('.clear'):
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
