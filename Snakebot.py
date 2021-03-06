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

            if (i.emoji == '🐍' and i.count == 4):

                if(str(target.name) not in data):
                    data[target.name] = 1
                else:
                    data[target.name] = int(data[target.name]) + 1

                with open('data.json', 'w') as storage:
                    json.dump(data, storage)

                await info[1].send(target.name + " has been found guilty of snakery")
                del LoggedMessages[payload.message_id]

                break
    elif (payload.message_id in LoggedMessages and payload.emoji.name == '🦡'):

        info = LoggedMessages[payload.message_id]
        target = info[0]
        msg = info[1].message

        for i in msg.reactions:

            if (i.emoji == '🦡' and i.count == 5):

                if(str(target.name) not in data):
                    data[target.name] = -1
                else:
                    data[target.name] = int(data[target.name]) - 1

                with open('data.json', 'w') as storage:
                    json.dump(data, storage)

                await info[1].send(target.name + " has been found innocent of snakery")
                del LoggedMessages[payload.message_id]

                break


@bot.command()
async def snake(ctx, target: discord.Member):
    await ctx.send(target.name + "'s snakery has been noted")
    await ctx.message.add_reaction('🐍')
    LoggedMessages[ctx.message.id] = (target, ctx, datetime.now())


@bot.command()
async def mongoose(ctx, target: discord.Member):
    await ctx.send(target.name + "'s mongoosery has been noted")
    await ctx.message.add_reaction('🦡')
    LoggedMessages[ctx.message.id] = (target, ctx, datetime.now())


@ bot.command(aliases=["snakecount", "Snakecount", "SnakeCount"])
async def getSnakeCount(ctx, target: discord.Member):
    await ctx.send(target.name + " has snaked people " + str(data[target.name]) + " times")


@bot.command()
async def leaderboard(ctx):
    snakes = {}
    order = data.copy()
    while len(order) > 0:
        my_biggest_key = max(order, key=lambda key: order[key])
        snakes[my_biggest_key] = order[my_biggest_key]
        order.pop(my_biggest_key)
    leaderboard_str = ""
    for key, value in snakes.items():
        leaderboard_str += key + ": " + \
            str(value) + " snakes" + "\n"
    await ctx.send(leaderboard_str)


@bot.command(aliases=['sb/lb'])
async def setsnake(ctx, target: discord.Member, snakecount):
    if (ctx.author.guild_permissions.administrator or ctx.author.id == 363396359841251328 or ctx.author.id == 233753795220209665):
        data[target.name] = int(snakecount)

        with open('data.json', 'w') as storage:
            json.dump(data, storage)

        await ctx.send("Snake set")


@ bot.command()
async def stop(ctx):
    if (ctx.author.id == 363396359841251328 or ctx.author.id == 233753795220209665):
        await ctx.send("Cya")

        with open('data.json', 'w') as storage:
            json.dump(data, storage)

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
