'''
Created on Dec 30, 2017

@author: Red
'''
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from dateutil.parser import *
from dateutil import tz
from datetime import *
from dateutil import days
import pytz
from general import listen
from general import Cancel

yes_response = "That sounds like a cool event! I hope you invite me. :heart:"
no_response="Oh, okay. Let's try that again!"
uncertain_response="I'm sorry, can you repeat that for me?"

bot = commands.Bot(command_prefix="!")

async def eventCall(ctx, bot):
    
    member = ctx.message.author
    print ("!event - " + member.display_name)
    message = await bot.send_message(member, "Hi " + member.display_name + "!")
    channel = message.channel
    
    await bot.send_message(member, "You want to create an event? :calendar: I can help with that!")
    await bot.send_message(member, 'Type "Cancel" if you want to quit at any point.')
    
    embed = discord.Embed(title = "Event Name", description = "Your description")
    embed.set_author(name = ("Created by: " + member.display_name), icon_url = member.avatar_url)
    
    try:
        event_name = await setEventName(member, embed, channel, bot)
        event_description = await setEventDescription(member, embed, channel, bot)
        event_date = await setEventDate(member, embed, channel, bot)
        event_start = await setEventStartTime(member, embed, channel, bot)
        #event_end = await setEventEndTime(member, embed, channel, bot)
        event_location = await setEventLocation(member, embed, channel, bot)
        event_category = await setEventCategory(member, embed, channel, bot)
    except Cancel:
        message = await bot.send_message(member, "Cancelling your event request, " + member.display_name + "!")
        return
        
    embed.add_field(name = "RSVP", value = "Use :thumbsup: to indicate you'll attend. Use :thumbsdown: to indicate you can't.")
    
    await bot.send_message(member, embed=embed)
    
    #Announcements Channel
    await bot.send_message(discord.Object("333064282839318530"), embed = embed)
    #Testing Channel
    await bot.send_message(discord.Object("411940462098907137"), embed = embed)
    
#    sh = gc.open("FE Events").sheet1
#    events = sh.col_values(1)
#    event_cnt = len(events) + 1
    
#    sh.update_cell(event_cnt, 1, ctx.message.id)
#    sh.update_cell(event_cnt, 2, event_name)
#    sh.update_cell(event_cnt, 3, event_description)
#    sh.update_cell(event_cnt, 4, event_date.strftime("%A, %B %d"))
#    sh.update_cell(event_cnt, 5, event_start.strftime("%I:%M %p"))
#   sh.update_cell(event_cnt, 6, event_end.strftime("%I:%M %p"))
#    sh.update_cell(event_cnt, 6, event_location)
#    sh.update_cell(event_cnt, 7, event_category)

async def setEventName(member, embed, channel, bot):
    await bot.send_message(member, "What is the name of your event?")
    msg = await listen(member, channel, bot)
    
    embed.description = msg.content
    
    await bot.send_message(member, embed = embed)
    await confirmResponse(member, embed, setEventName, channel, bot)
    
    return msg.content

async def setEventDescription(member, embed, channel, bot):
    await bot.send_message(member, "How would you describe your event?")
    msg = await listen(member, channel, bot)
    
    await manageEmbedFields(embed, "Description", msg.content, False, 0)
        
    await bot.send_message(member, embed = embed)
    await confirmResponse(member, embed, setEventDescription, channel, bot)
    
    return msg.content

async def setEventDate(member, embed, channel, bot):
    await bot.send_message(member, "What day will your event take place?")
    msg = await listen(member, channel, bot)
    
    while True:
        try:
            event_date = parse(msg.content)
        except ValueError or OverflowError:
            await bot.send_message(member, uncertain_response)
            msg = await listen(member, channel, bot)
        else:
            break
    
    #await manageEmbedFields(embed, "Date", str(event_date.month) + "/" + str(event_date.day) + "/" + str(event_date.year), False, 1)
    await manageEmbedFields(embed, "Date", event_date.strftime("%A, %B %d"), False, 1)
        
    await bot.send_message(member, embed=embed)
    await confirmResponse(member, embed, setEventDate, channel, bot)
    
    return event_date
  
async def setEventStartTime(member, embed, channel, bot):
    now = getNowEST()
    
    await bot.send_message(member, "When will your event start in EST? For reference, it is now " + now.strftime("%I:%M %p"))
    msg = await listen(member, channel, bot)
    
    while True:
        try:
            event_time = parse(msg.content)
        except ValueError or OverflowError:
            await bot.send_message(member, uncertain_response)
            msg = await listen(member, channel, bot)
        else:
            break
    
    await manageEmbedFields(embed, "Start Time", event_time.strftime("%I:%M %p") + " EST", True, 2)
        
    await bot.send_message(member, embed=embed)
    await confirmResponse(member, embed, setEventStartTime, channel, bot)
    
    return event_time
    
# async def setEventEndTime(member, embed, channel, bot):
#     now = getNowEST()
#     
#     await bot.send_message(member, "When will your event end in EST? For reference, it is now " + now.strftime("%I:%M %p"))
#     msg = await listen(member, channel, bot)
#     
#     while True:
#         try:
#             event_time = parse(msg.content)
#         except ValueError or OverflowError:
#             await bot.send_message(member, uncertain_response)
#             msg = await listen(member, channel, bot)
#         else:
#             break
#     
#     await manageEmbedFields(embed, "End Time", event_time.strftime("%I:%M %p") + " EST", True, 3)
#         
#     await bot.send_message(member, embed=embed)
#     await confirmResponse(member, embed, setEventEndTime, channel, bot)
#     
#     return event_time

async def setEventLocation(member, embed, channel, bot):
    await bot.send_message(member, "Where will your event begin?")
    msg = await listen(member, channel, bot)
    
    await manageEmbedFields(embed, "Location", msg.content, False, 3)
        
    await bot.send_message(member, embed = embed)
    await confirmResponse(member, embed, setEventLocation, channel, bot)

    return msg.content

async def setEventCategory(member, embed, channel, bot):
    await bot.send_message(member, "Almost done! How should your event be categorized?")
    colors = discord.Embed(title="Colors", description="Guide to color categories") #, url="http://freefolk.enjin.com/forum/m/6548766/viewthread/10886143-event-colour-guide")
    colors.add_field(name = "Grey", value = "Fluffy, fun one-shot events. Good for parties, character birthdays, weddings, etc.")
    colors.add_field(name = "Brown", value = "Primarily domestic events, such as Flipside. Good for recurring events.")
    colors.add_field(name = "Green", value = '"In the field" events", i.e. those that take roleplay out into the wilds or to less frequented areas of Nexus.')
    colors.add_field(name = "Blue", value = "Multi-event mini-plots with a developed narrative that pulls the individual events together.")
    colors.add_field(name = "Purple", value = "Out of character events, such as levelling, deeding, meetings, or planning sessions.")
    colors.add_field(name = "Red", value = "Larger scale or epic ongoing plots that cover more distance and scope.")
    await bot.send_message(member, embed = colors)
    
    msg = await listen(member, channel, bot)
    answer = msg.content
    while answer not in ["Grey", "GREY", "grey", "Gray", "GRAY", "gray", "Brown", "BROWN", "brown", "Green", "GREEN", "green", "Blue", "BLUE", "blue", "Purple", "PURPLE", "purple", "Red", "RED", "red"]:
        await bot.send_message(member, uncertain_response)
        msg = await listen(member, channel, bot)
        answer = msg.content
    
    if answer in ["Grey", "GREY", "grey", "Gray", "GRAY", "gray"]:
        await bot.send_message(member, "Grey it is then!")
        embed.color = 0x808080
            
    if answer in ["Brown", "BROWN", "brown"]:
        await bot.send_message(member, "Brown it is then!")
        embed.color = 0x4E2F19
        
    if answer in ["Green", "GREEN", "green"]:
        await bot.send_message(member, "Green it is then!")
        embed.color = 0x0B5C40
            
    if answer in ["Blue", "BLUE", "blue"]:
        await bot.send_message(member, "Blue it is then!")
        embed.color = 0x3CADE5
            
    if answer in ["Purple", "PURPLE", "purple"]:
        await bot.send_message(member, "Purple it is then!")
        embed.color = 0x8824c1
        
    if answer in ["Red", "RED", "red"]:
        await bot.send_message(member, "Red it is then!")
        embed.color = 0xcc0000

    await bot.send_message(member, embed = embed)
    
    yes_response = "Tweeting out your event now!"
    await confirmResponse(member, embed, setEventCategory, channel, bot, yes_response = yes_response)
    
    return answer
    
async def confirmResponse(member, embed, method_to_run, channel, bot, yes_response=yes_response, no_response=no_response, uncertain_response=uncertain_response):
    
    await bot.send_message(member, 'Is that correct? Answer "Yes" or "No"!')
    
    msg = await listen(member, channel, bot)
    answer = msg.content
    while answer not in ["Yes", "yes", "YES", "y", "Y", "YEs", "No", "NO", "no", "N", "n"]:
        await bot.send_message(member, uncertain_response)
        msg = await listen(member, channel, bot)
        answer = msg.content
    
    if answer in ["Yes", "yes", "YES", "y", "Y", "YEs"]:
        await bot.send_message(member, yes_response)
    
    else: 
        await bot.send_message(member, no_response)
        msg = await method_to_run(member, embed, channel, bot)

async def manageEmbedFields(embed, name, value, inline, index):
    list = embed.fields
    if list.__len__() <= index:
        embed.add_field(name = name, value = value, inline = inline)
        
    else:
        embed.set_field_at(index, name = name, value = value)

def getNowEST():
    now = datetime.now()
    old_timezone = pytz.timezone("US/Central")
    new_timezone = pytz.timezone("US/Eastern")
    return old_timezone.localize(now).astimezone(new_timezone)
