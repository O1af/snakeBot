import json
import discord
from discord.ext import commands
from datetime import datetime
import asyncio

token = open('token.txt', 'r')
botToken = token.read()
token.close()

f = open('data.json', 'r+')
data = json.loads(f.read())
bot = commands.Bot(command_prefix="sb/")

LoggedMessages = {}

@bot.event
async def on_ready():
    print("Bot is Online")
    await CheckMsgTimestamps()

@bot.event
async def on_raw_reaction_add(payload):

    if (payload.message_id in LoggedMessages and payload.emoji.name == '🐍'):

        info = LoggedMessages[payload.message_id]
        target = info[0]
        msg = info[1].message

        for i in msg.reactions:

            if (i.emoji == '🐍' and i.count == 2):

                if(str(target.name) not in data):
                    data[target.name] = 1
                else:
                    data[target.name] = int(data[target.name]) + 1
                        
                with open('data.json', 'w') as storage:
                    json.dump(data, storage)
                    
                await info[1].send(target.name + " has been found guilty of snakery")

                break

@bot.command()
async def snake(ctx, target : discord.Member):
    await ctx.send(target.name + "'s snakery has been noted")
    LoggedMessages[ctx.message.id] = (target, ctx, datetime.now())


@ bot.command(aliases=["snakecount", "Snakecount", "SnakeCount"])
async def getSnakeCount(ctx, target: discord.Member):
    await ctx.send(target.name + " has snaked people " + str(data[target.name]) + " times")


@bot.command()
async def leaderboard(ctx):
    snakes = {}
    order = data.copy()
    while len(order) > 0:
        my_biggest_key = max(order, key=order.get)
        snakes[my_biggest_key] = order[my_biggest_key]
        order.pop(my_biggest_key)
    leaderboard_str = ""
    for key, value in snakes.items():
        leaderboard_str += key + ": " + \
            str(value) + " snakes" + "\n"
    await ctx.send(leaderboard_str)

@bot.command()
async def setsnake(ctx, target: discord.Member, snakecount):
    if (ctx.author.guild_permissions.administrator):
        data[target.name] = snakecount
        await ctx.send("Snake set")

@ bot.command()
async def stop(ctx, target: discord.Member):
    if (ctx.id == 363396359841251328):
        await ctx.send("Cya")
        f.write(json.dumps(data))
        f.close()
        bot.close()
        exit()

async def CheckMsgTimestamps():
    while True:

        rmv = []
        for key in LoggedMessages:
        
            TimePassed = datetime.now() - LoggedMessages[key][2]
            if (TimePassed.seconds > 3600 or TimePassed.days > 1):
                rmv.append(key)
        
        for i in rmv:
            LoggedMessages.pop(i)

        await asyncio.sleep(300)
        
bot.run(botToken)
