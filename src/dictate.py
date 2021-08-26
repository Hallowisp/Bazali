'''
Created on Dec 30, 2017

@author: Red
'''
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from general import listen
from general import Cancel

bot = commands.Bot(command_prefix="!")

yes_response = "That sounds like a cool event! I hope you invite me. :heart:"
no_response="Oh, okay. Let's try that again!"
uncertain_response="I'm sorry, can you repeat that for me?"

async def dictateCall(ctx, bot):
    member = ctx.message.author
    
    try:
        print ("!dictate - " + member.display_name + " - " + ctx.message.channel.name)
        if ctx.message.channel.name != "testing":
            return
    except TypeError:
        return
    
    message = await bot.send_message(member, "You want me to send a message? I can do that!")
    channel = message.channel
        
    await bot.send_message(member, 'Type "Cancel" if you want to quit at any point.')
    await bot.send_message(member, "What channel would you like to send your message to?")
    channels = discord.Embed(title="Channels", description="Choose 1 through 9") #, url="http://freefolk.enjin.com/forum/m/6548766/viewthread/10886143-event-colour-guide")
    channels.add_field(name = "testing", value = "1")
    channels.add_field(name = "general-chat", value = "2")
    channels.add_field(name = "rolls", value = "3")
    channels.add_field(name = "art", value = "4")
    channels.add_field(name = "media", value = "5")
    channels.add_field(name = "nsfw", value = "6")
    channels.add_field(name = "photos", value = "7")
    channels.add_field(name = "announcements", value = "8")
    channels.add_field(name = "eso-general", value = "9")
    await bot.send_message(member, embed = channels)
    
    try:
        msg = await listen(member, channel, bot)
        answer = msg.content
        while answer not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            await bot.send_message(member, uncertain_response)
            msg = await listen(member, channel, bot)
            answer = msg.content
            
    except Cancel:
        message = await bot.send_message(member, "Cancelling your dictation, " + member.display_name + "!")
    
    if answer in ["1"]:
        dictateChannel = "411940462098907137" #testing
        channelName = "testing"
            
    if answer in ["2"]:
        dictateChannel = "496714544421404682" #general-chat
        channelName = "general-chat"
        
    if answer in ["3"]:
        dictateChannel = "463149472910802944" #rolls
        channelName = "rolls"
            
    if answer in ["4"]:
        dictateChannel = "515975505787224104" #art
        channelName = "art"
            
    if answer in ["5"]:
        dictateChannel = "511982313001713664" #media
        channelName = "media"
        
    if answer in ["6"]:
        dictateChannel = "515975052991135754" #nsfw
        channelName = "nsfw"
        
    if answer in ["7"]:
        dictateChannel = "511982347051073537" #photos
        channelName = "photos"
    
    if answer in ["8"]:
        dictateChannel = "333064282839318530" #announcements
        channelName = "announcements"
        
    if answer in ["9"]:
        dictateChannel = "488167465574989824" #eso-general
        channelName = "eso-general"
        
    await bot.send_message(member, "All right, dictating for you in " + channelName + '! Begin typing when ready! Type "Cancel" to end dictation.')
    
    while True:
        try:
            msg = await listen(member, channel, bot)
            await bot.send_message(discord.Object(dictateChannel), msg.content)
        except Cancel:
            await bot.send_message(member, "Cancelling your dictation.")
            break
