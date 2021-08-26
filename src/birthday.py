'''
Created on Mar 26, 2019

@author: ericg
'''
import discord
import asyncio
from dateutil.parser import parse
from datetime import *
from general import listen
from general import Cancel
import json

uncertain_response="I'm sorry, can you repeat that for me?"

async def birthday(bot):
    
    channel = "411940462098907137" #testing channel
    #channel = "496714544421404682" #general-chat channel
    
    while not bot.is_closed:
        now = datetime.now()
        if int(now.strftime("%H")) > 9:
            with open('Birthdays.txt', "r+") as json_file:
                data = json.load(json_file)
                
                for p in data['birthdays']:
                    # print("User: " + p['User'])
                    # print("Year: " + str(p['Year']))
                    # print("Month: " + str(p['Month']))
                    # print("Day: " + str(p['Day']))
                    # print('')
                    
                    birthday = date(p['Year'],p['Month'],p['Day'])
                    
                    if birthday == date.today():
                        userInfo = p["User"].split("#",1)
                        user = discord.utils.get(bot.get_all_members(), name = userInfo[0], discriminator = userInfo[1])
                        #print (user)
                        await bot.send_message(discord.Object(channel), "Everyone wish " + user.mention + " a happy birthday!!!")
                        p["Year"] = p["Year"]+1 #Iterate the number of years
                
                json_file.seek(0)  # rewind
                json.dump(data, json_file)
                json_file.truncate()
                    
        await asyncio.sleep(10)


async def setBirthdayCall(ctx, bot):
    member = ctx.message.author
    print ("!setBirthday - " + member.display_name)
    
    with open('Birthdays.txt', "r+") as json_file:
        data = json.load(json_file)
        
        foundFlag = False
        
        # Search for the user's existing birthday
        for p in data['birthdays']:
            
            if (member.name + "#" + member.discriminator) == str(p['User']):
                foundFlag = True
                birthday = date(p['Year'],p['Month'],p['Day'])
                birthdayString = birthday.strftime("%A, %B %d, %Y")
                
                message = await bot.send_message(member, "Your birthday has already been set! It will occur next on " + birthdayString + "!") 
                channel = message.channel           
                await bot.send_message(member, "Do you want to update it? Enter your updated birthdate or type 'Cancel' to quit.")
                
                cancelString = "Keeping your birthday on " + birthdayString + ", " + member.display_name + "!"
                newBirthday = await setUserBirthday(ctx, bot, member, channel, cancelString)
                
                p['Year'] = newBirthday.year
                p['Month'] = newBirthday.month
                p['Day'] = newBirthday.day
        
        # Didn't find the user - create a new birthday
        if foundFlag == False:
            message = await bot.send_message(member, "Let's get your birthday on file!") 
            channel = message.channel           
            await bot.send_message(member, "Enter your birthdate or type 'Cancel' to quit.")
            
            cancelString = "Okay - we won't set your birthday right now."
            newBirthday = await setUserBirthday(ctx, bot, member, channel, cancelString)
           
            newBirthdayDict = {'User': member.name + "#" + member.discriminator,'Year': newBirthday.year, 'Month': newBirthday.month, 'Day':newBirthday.day}
            data['birthdays'].append(newBirthdayDict)
                
        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()

async def setUserBirthday(ctx, bot, member, channel, cancelString):
    while True:
        try:
            msg = await listen(member, channel, bot)
            newBirthday = parse(msg.content)
        except ValueError or OverflowError:
            await bot.send_message(member, uncertain_response)
            msg = await listen(member, channel, bot)
        except Cancel:
            await bot.send_message(member, cancelString)
            return 
        else:
            break
    
    newBirthday = newBirthday.date()
    newBirthday = newBirthday.replace(year=date.today().year)
    if newBirthday < date.today():
        newBirthday = newBirthday.replace(year=(date.today().year + 1))
                                          
    await bot.send_message(member, "Great! We'll celebrate next on " + newBirthday.strftime("%A, %B %d, %Y") + "!")
    
    return newBirthday

        #try:
        #    event_name = await setEventName(member, embed, channel, bot)

        #except Cancel:
        #    message = await bot.send_message(member, "Cancelling your birthday addition, " + member.display_name + "!")
        #    return
        
        #await listen(member, message.channel, bot)