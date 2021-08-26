'''
Created on Dec 30, 2017

@author: Red
'''
import discord
from discord.ext import commands
import asyncio
from event import eventCall
from dictate import dictateCall
from birthday import birthday, setBirthdayCall
#from warble import warbleCall
from roll import rollCall
from random import randint
from setuptools.command.rotate import rotate
from builtins import type

bot = commands.Bot(command_prefix="!")
client = discord.Client()

@bot.event
async def on_ready():
    print ("Booting up your system")
    print ("I am running on " + bot.user.name)
    print ("With the ID: " + bot.user.id)
   
    client.loop.create_task(birthday(bot))
    client.loop.create_task(rotate())
   
  
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    
    if ("penis" in message.content.lower()) or ("wang" in message.content.lower()) or ("willy" in message.content.lower()) or ("dick" in message.content.lower()) or ("peen" in message.content.lower()) or ("weiner" in message.content.lower()):
        await react(message, "🍆", 20) #eggplant
        
    if ("orange son" in message.content.lower()) or ("good son" in message.content.lower()):
        await react(message, "🍼") #baby_bottle
        
    if ("chua" in message.content.lower()):
        await react(message, "💣", 50) #bomb
        
    if ("vixenz" in message.content.lower()):
        await react(message, "💋", 80) #kiss
        
    if ("slickened hol" in message.content.lower()) or ("butts" in message.content.lower()):
        await react(message, "🍑") #peach

    if ("thank you, eve" in message.content.lower()) or ("thank you eve" in message.content.lower()) or ("thanks, eve" in message.content.lower()) or ("thanks eve" in message.content.lower()):
        await react(message, "😀") #smiley        
    
    if ("i love eve" in message.content.lower()) or ("i love you eve" in message.content.lower()):
        await react(message, "💗") #heart 
        
    if ("taco" in message.content.lower()):
        await react(message, "🌮", 60) #taco 
        
    if (" erp" in message.content.lower()):
        await react(message, "😳", 30) #blush 
    
    if ("jesse payne" in message.content.lower()):
        await react(message, "🤠", 50) #cowboy 
        
    if (" birthday" in message.content.lower()):
        await react(message, "🎂") #cake
        
    if ("doofs" in message.content.lower()):
        await react(message, "🤡") #clown
        
    if ("rofl" in message.content.lower()):
        await react(message, "🤣") #rofl
                
    if ("xd" in message.content.lower()):
        await react(message, "😆") #xd
    
    channel = message.channel
    member = message.author
    attachments = message.attachments
    for attach in attachments:
        if ("genji_and_pachimari" in attach.get("filename")):
            await asyncio.sleep(3)
            await bot.delete_message(message)
            filepath = r"C:\Users\ericg\eclipse-workspace\EVE\EVE\Genji_Censored.jpg"
            await bot.send_file(channel, filepath, content=("The following image from " + member.display_name  + " has been censored. A modified version has been submitted instead."))

@bot.event
async def on_member_join(member):
    print ("joined server - " + member.display_name)
    #channel = "411940462098907137" #testing channel
    channel = "496714544421404682" #general-chat channel
    await bot.send_message(discord.Object(channel), "Everyone say hi to " + member.display_name + "!")
    role = discord.utils.get(member.server.roles, name="Circle Member")
    await bot.add_roles(member, role)
    
    await bot.send_message(member, "Welcome to Emma's Valley! I'm EVE, Fantastic Enterprise's personal robotic assistant!")
    await asyncio.sleep(3)
    await bot.send_message(member, "Feel free to ask me any questions you might have! A lot of good information can be found in the 'resources' channel as well - check it out!")
    await asyncio.sleep(3)
    await bot.send_message(member, "You can also check out upcoming events in the 'announcements' channel! Just don't forget to RSVP!")
    await asyncio.sleep(3)
    await bot.send_message(member, "We hope you enjoy your stay in Emma's Valley! :grin: :tropical_drink: :peach:")  
    
@bot.event
async def on_reaction_add(reaction, user):
    msg = reaction.message
    
    if isinstance(reaction.emoji, discord.Emoji):
        name = reaction.emoji.name
    elif isinstance(reaction.emoji, str):
        name = reaction.emoji
    else:
        raise ValueError("Unknown emoji of type:", type(reaction.emoji))
    
    appropriate_emote = [":thumbsup:", ":thumbsup:", "👍", "👎"]
    if (msg.channel.id == "333064282839318530" and (msg.author.id == "411942211262087169") and (name not in appropriate_emote)): #Announcements and EVE
        print ("on_reaction_add - " + user.name)
        await asyncio.sleep(1)
        await bot.remove_reaction(msg, reaction.emoji, user)
        await bot.send_message(user, "That isn't a :thumbsup: or :thumbsdown:, " + user.display_name + "!")

@bot.event        
async def react(message, emoji, chance=100):
    if randint(0,99) < chance:
        await asyncio.sleep(3)
        await bot.add_reaction(message, emoji)
    

async def rotate():
    # Rotating status updates
    status_updates = ["!event for new events", "Dan's Dancer Evolution", "3.5D Chess", "!roll to roll a d12", "Super Fringe Racers", "Jesse Payne", "Age of Kings: Online"]
    while not bot.is_closed:
        for item in status_updates:
            await asyncio.sleep(10)
            await bot.change_presence(game = discord.Game(name = item))

@bot.command(pass_context=True)
async def event(ctx):
    await eventCall(ctx, bot)

@bot.command(pass_context=True)
async def dictate(ctx):
    await dictateCall(ctx, bot)
    
@bot.command(pass_context=True)
async def setBirthday(ctx):
    await setBirthdayCall(ctx, bot)
    
#@bot.command(pass_context=True)
#async def warble(ctx):
#    await warbleCall(ctx, bot)
    
@bot.command(pass_context=True)
async def roll(ctx, val = '12'):
    await rollCall(ctx, bot, val)
   
bot.run("NDExOTQyMjExMjYyMDg3MTY5.DWDd-w.YVCx-jwhW8EuAuKy8hkIPUvO75E")   
