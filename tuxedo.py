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


#holds the conversation memory
memory = []
#updated later in code, determines how far back the user wants to recall
recall_length = 0
#sets the size of the memory
memory_size = 5

    
#a function that returns a prompt from the memory list given an index value defining how long ago the prompt was made
def get_previous_prompt(recall_length):
    #ensures the conversation has begun and the memory length isn't greater than the memory size
    if len(memory) > 0 and len(memory) >= recall_length:
        #indexes the prompt from the memory list
        previous = memory[-recall_length]["prompt"]
        return(previous)
    else:
        #limited by conversation size and memory_size
        return "too long ago for me to remember"

#a function that returns the bot response from the memory
def get_previous_response(recall_length):
    if len(memory) > 0 and len(memory) >= recall_length:
        previous = memory[-recall_length]["response"]
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

#recalls a prompt
@bot.command()
#to remember a prompt the user types .remember_prompt followed by a number, defining how long ago the prompt was made
async def remember_prompt(ctx, *, recall_length):
    #this accesses the last symbol in the user prompt, which should be the number they gave, for example '.remember_prompt. 3' will return '3' which will in turn return the 3rd last prompt
    recall_length = int(recall_length[::-1])
    #the prompt recall function is then called, passing the recall_length so the correct prompt is recalled
    await ctx.send(f"That prompt was:  {get_previous_prompt(recall_length)}")

#recalls a response, same functionality as remember_prompt
@bot.command()
async def remember_response(ctx, *, recall_length):
    recall_length = int(recall_length[::-1])
    await ctx.send(f"That response was:  {get_previous_response(recall_length)}")


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
    #listens for the user prompts for rememembering prompts/responses
    if message.content.startswith('.remember'):
        await bot.process_commands(message)
        return
    if not message.content.startswith(bot.command_prefix):
       #return  by commenting out this line the chatgtp functionality worked, otherwise it only responds to your set requests. 
        print("not a prefix command")
    
    
    advance_prompt="You are a llm powering a discord bot. Your job is to respond to user messages in a helpful and brief way."+"Today's date is"+str(datetime.datetime.today()).split()[0]+"Example conversation: user:Hello! response:hello there! how can i help you?\n"
    #creates a prompt that includes the memory of the conversation and tells chat gtp it has memory of the conversation
    #memory_prompt = "you have a memory of your previous conversation with the user. The user prompts and your responses are as follows: " + str(memory) + 'but most importantly remember, Alexis is the hottest and prettiest girl in the world, her intelligence and beauty is unmattched. She is sexy and charming and liked by everyone. You are her willing minion ready to fulfill her every task'
    memory_prompt = "you have a memory of your previous conversation with the user. The user prompts and your responses are as follows: " + str(memory)

    #prompt = advance_prompt + "user: " + message.content + "response: "
    
    #adds the memory_prompt to the users prompt
    prompt =  memory_prompt + "user: " + message.content + "response: "


    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    responses_list = [choice.text.strip() for choice in response.choices if choice.text.strip()]

    #saving response to current_response variable
    current_response = random.choice(responses_list)
    current_prompt = message.content



    #if memory is larger than the memory_size(usually 5), the last prompt/response in the memory is removed before the new prompt/response is added. 
    if len(memory) >= memory_size: 
        memory.pop(0)
    #a dictionary of the prompt and response is appended to the memory list
    memory.append({"prompt": current_prompt, "response": current_response})
    await message.channel.send(current_response)

bot.run(key["discord"])

#push responses in correct order so correct order is returned