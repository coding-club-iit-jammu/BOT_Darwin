#BOT TOKEN
f = open("token.txt","r")
botToken = f.read()
f.close()

#DISCORD CHANNELS
channels={}
channels["#general"] = "664156473944834082" 
channels["#core"] = "664156536821776384"  
channels["#bot_testing"] = "690605490123571320"
channels["#bot-functionalities"] = "690616698675527782"

author = "690599381304606741" #this id can be obtained from DM channel link
#link to upcoming events file
upcoming_events = "https://raw.githubusercontent.com/abhishek0220/BOT_Darwin/master/Support/upcoming_events.csv"

#libraries
import discord
import time
import urllib.request
import codecs
import csv
import requests 
from discord.ext import commands

bot = commands.Bot(command_prefix='$Darwin ', description='Coding Club IIT Jammu Discord BOT')
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def greet(ctx):   #basic command to greet
    await ctx.send(":smiley: :wave: Hello, I am Darwin")

@bot.command()
async def about(ctx):   #About command
    msg = "I am **Darwin v1.0** Coding Club IIT Jammu`s Discord BOT created by **Abhishek Chaudhary** you may report any bug directly to him.\n $Darwin member abc : to get details of members name starting with abc.\n $Darwin post <channel> <msg> : to post message as bot in specified channel.\n $Darwin events : To find details about upcoming events.\n Currently Supported Command"
    await ctx.send(msg)

@bot.command()
async def post(ctx, a : str , b: str):  #command to post to specific channel
    channelspermited = [channels["#core"], channels["#bot_testing"]]
    #in case developer needs to communicate directely
    if(str(ctx.message.channel.id) == author):
        if(a in channels):
            channel = bot.get_channel(int(channels[a]))
            await channel.send(b)
            print("Msg posted from author")
    elif(str(ctx.message.channel.id) in channelspermited):
        ch_code = a[2:-1]
        channel = bot.get_channel(int(ch_code))
        await channel.send(b)
        print("Msg posted from coreteam")
    else:
        await ctx.send("Sorry you can`t use this command:rolling_eyes:.")

@bot.command()
async def member(ctx, a: str):
    channelspermited = [author, channels["#core"], channels["#bot_testing"], channels["#bot-functionalities"]]
    if(str(ctx.message.channel.id) not in channelspermited):
        await ctx.send("Sorry you can`t use this command:rolling_eyes:.")
        return
    if(len(a)<3):
        await ctx.send("Oops:confused: pls send minimum 3 letters.")
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
@bot.command()
async def Corona(ctx):
    URL = "https://corona.lmao.ninja/v2/countries/India"
    r = requests.get(url = URL) 
    data = r.json() 
    da = ['country','cases','todayCases','deaths','todayDeaths','recovered','active','critical','casesPerOneMillion','testsPerOneMillion']
    out = ""
    for i in da:
        out = out + i + " : " + str(data[i])+"\n"
    time_got = int(data['updated'])//1000 + 19800
    curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_got))
    last_updated = "\nLast Updated : " + curr_time
    out = out + last_updated
    out = out + "\nSource: NovelCOVID API"
    await ctx.send(out)

bot.run(botToken)