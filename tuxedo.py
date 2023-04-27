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

response_memory = []
prompt_memory = []
memory = []
recall_length = 0

response_num = 0
    
def get_previous_prompt(recall_length):
    if len(memory) > 0 and len(memory) >= recall_length:
        previous = memory[-recall_length]["prompt"]
        return(previous)
    else:
        return "too long ago for me to remember"

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
    await ctx.send(f'Poong!? {round(bot.latency * 1000)}ms')

#clears messages in the channel
@bot.command()
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)

#recalling last prompt
@bot.command()
async def remember_prompt(ctx, *, recall_length):
    recall_length = int(recall_length[::-1])
    await ctx.send(f"That prompt was:  {get_previous_prompt(recall_length)}")


@bot.command()
async def remember_response(ctx, *, recall_length):
    recall_length = int(recall_length[::-1])
    await ctx.send(f"That answer was:  {get_previous_prompt(recall_length)}")

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
    if message.content.startswith('.remember'):
        await bot.process_commands(message)
        #recall_length = int(message.content[-1:])
        return
    if not message.content.startswith(bot.command_prefix):
        print('test')
    
    #advance_prompt="You are an evil overlord commanding your minions. Your job is to create chaos and have fun."+"Today's date is"+str(datetime.datetime.today()).split()[0]+"Example conversation: user:Hello! response:hello there! how can i help you?\n"
    #prompt = advance_prompt + "user: " + message.content + "response: "
    prompt =  "user: " + message.content + "response: "


    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    responses_list = [choice.text.strip() for choice in response.choices if choice.text.strip()]

    #saving response to current_response variable
    current_response = random.choice(responses_list)
    current_prompt = message.content
    memory_size = 5


    #add current_response to memory[]
    if len(response_memory) >= memory_size: 
        response_memory.pop(0)
    response_memory.append(current_response)
    
    if len(prompt_memory) >= memory_size: 
        prompt_memory.pop(0)
    prompt_memory.append(current_prompt)

    if len(memory) >= memory_size: 
        memory.pop(0)
    memory.append({"prompt": current_prompt, "response": current_response})

    

    
    
   
    await message.channel.send(current_response)

print(get_previous_prompt(recall_length))
bot.run(key["discord"])