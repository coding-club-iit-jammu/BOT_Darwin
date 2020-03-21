f = open("token.txt","r")
botToken = f.read()
f.close()

channels={}
channels["#general"] = "664156473944834082"
channels["#core"] = "664156536821776384"
channels["#bot_testing"] = "690605490123571320"
channels["#bot-functionalities"] = "690616698675527782"
author = "690599381304606741"
upcoming_events = "https://raw.githubusercontent.com/abhishek0220/BOT_Darwin/master/Support/upcoming_events.csv"

import discord
import urllib.request
import codecs
import csv
from discord.ext import commands

bot = commands.Bot(command_prefix='$Darwin ', description='A bot that greets the user back.')
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hello, I am Darwin")

@bot.command()
async def about(ctx):
    msg = "I am **Darwin v1.0** Coding Club IIT Jammu`s Discord BOT created by **Abhishek Chaudhary** you may report any bug directly to him.\n $Darwin member abc : to get details of members name starting with abc.\n $Darwin post <channel> <msg> : to post message as bot in specified channel.\n $Darwin events : To find details about upcoming events.\n Currently Supported Command"
    await ctx.send(msg)

@bot.command()
async def post(ctx, a : str , b: str):
    if(str(ctx.message.channel.id) == author):
        if(a in channels):
            channel = bot.get_channel(int(channels[a]))
            await channel.send(b)
            print("Msg posted from author")
    elif(str(ctx.message.channel.id) == channels["#core"] or str(ctx.message.channel.id) == channels["#bot_testing"]):
        ch_code = a[2:-1]
        channel = bot.get_channel(int(ch_code))
        await channel.send(b)
        print("Msg posted from coreteam")


    

@bot.command()
async def member(ctx, a: str):
    if(len(a)<3 or (str(ctx.message.channel.id) != channels["#core"] and str(ctx.message.channel.id) != author and str(ctx.message.channel.id) != channels["#bot_testing"] and str(ctx.message.channel.id) != channels["#bot-functionalities"])):
        return
    match = a.upper()
    found = set()
    with open('members.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            name = row[0]
            name = name[0:len(match)]
            if(name.upper() == match):
                tem = (row[0], row[1].lower(), row[3])
                found.add(tem)
    output = "Found "+str(len(found))+" Students\n\n"
    for i in found:
        na = "**Name** : "+i[0]
        em = "**Email** : "+i[1]
        opt = "**Deparment** : "+i[2]
        tem = na+"\n"+em+"\n"+opt+"\n"
        output = output + tem + "\n"
    await ctx.send(output)

@bot.command()
async def events(ctx):
    event_list = []
    ftpstream = urllib.request.urlopen(upcoming_events)
    csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
    i = 0
    for line in csvfile:
        if(i == 0):
            header = line
            i +=1
            continue
        event_list.append(line)
    output = "Found "+str(len(event_list))+" Events\n\n"
    for i in event_list:
        tem = ""
        for j in range(len(header)):
            tem = tem + "**" + header[j] + "** : " + i[j] + "\n"
        output = output + tem + "\n"
    await ctx.send(output)
bot.run(botToken)