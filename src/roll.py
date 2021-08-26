'''
Created on Jul 1, 2018

@author: Red
'''
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from general import listen
from general import Cancel
from random import randint

bot = commands.Bot(command_prefix="!")

async def rollCall(ctx, bot, val):
    member = ctx.message.author
    #channel = "411940462098907137" #testing channel
    channel = "463149472910802944" #rolls channel
    try:
        max = int(float(val))
        await bot.send_message(discord.Object(channel), member.display_name + " rolled " + str(randint(1,max)) + "! (d" + str(max) + ")")
    except:
        await bot.send_message(discord.Object(channel), "I'm sorry " + member.display_name + ". I can't let you do that.")
        '''
Created on Mar 13, 2019

@author: ericg
'''
