'''
Created on Dec 30, 2017

@author: Red
'''
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

yes_response = "That sounds like a cool event! I hope you invite me. :heart:"
no_response="Oh, okay. Let's try that again!"
uncertain_response="I'm sorry, can you repeat that for me?"

bot = commands.Bot(command_prefix="!")
    
async def listen(member, channel, bot):
    msg = await bot.wait_for_message(timeout = 600, author = member, channel = channel)
    if (msg.content.lower() == "cancel" or msg == None):
        raise Cancel()
    else:
        return msg
    
class Cancel(Exception):
    pass
