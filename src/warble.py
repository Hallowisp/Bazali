'''
Created on May 21, 2018

@author: Red
'''

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import gspread
import os

async def warbleCall(ctx, bot):
    
  #  wks = gc.open("FE Warbler").sheet1
  #  val = wks.acell('A1').value
  #  print(val)