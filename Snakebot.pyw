import json
import discord
from discord import message
from discord.ext import commands
from datetime import datetime
import asyncio

token = open('token.txt', 'r')
botToken = token.read()
token.close()

f = open('data.json', 'r+')
data = json.loads(f.read())
bot = commands.Bot(command_prefix="sb/")

banList = open('ban.json', 'r+')
bans = json.loads(banList.read())
LoggedMessages = {}


def check_if_banned(user):
    banList = open('ban.json', 'r+')
    bans = json.loads(banList.read())
    for i in bans:
        if i == user.id:
            return True
        else:
            return False


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

            if (i.emoji == '🐍' and i.count == 6):

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

            if (i.emoji == '🦡' and i.count == 6):

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
    if (check_if_banned(ctx.author)):
        await ctx.send("You are banned from using this command")
    else:
        await ctx.send(target.name + "'s snakery has been noted")
        await ctx.message.add_reaction('🐍')
        LoggedMessages[ctx.message.id] = (target, ctx, datetime.now())


@bot.command(aliases=["say"])
async def echo(ctx, *, content: str):

    if (ctx.author.id == 363396359841251328 or ctx.author.id == 233753795220209665):
        # This delete an message in the channel
        await ctx.message.delete()
        await ctx.send(content)  # This the echo


@bot.command()
async def intro(ctx):
    if (check_if_banned(ctx.author)):
        await ctx.send("You are banned from using this command")
    else:
        if (ctx.author.id == 363396359841251328 or ctx.author.id == 233753795220209665):
            await ctx.message.delete()
            await ctx.send("I have returned @everyone")


@bot.command()
async def mongoose(ctx, target: discord.Member):
    await ctx.send(target.name + "'s mongoosery has been noted")
    await ctx.message.add_reaction('🦡')
    LoggedMessages[ctx.message.id] = (target, ctx, datetime.now())


@ bot.command(aliases=["snakecount", "Snakecount", "SnakeCount"])
async def getSnakeCount(ctx, target: discord.Member):
    await ctx.send(target.name + " has snaked people " + str(data[target.name]) + " times")


@bot.command(aliases=["lb"])
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


@bot.command(aliases=[''])
async def setsnake(ctx, target: discord.Member, snakecount):
    if (ctx.author.id == 363396359841251328 or ctx.author.id == 233753795220209665):
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


@bot.command()
async def ban(ctx, user: discord.Member):
    if (ctx.author.id == 363396359841251328 or ctx.author.id == 233753795220209665):
        if (user.id not in bans):
            bans.append(user.id)
            print(bans)
            await ctx.send("User has been banned")
        else:
            await ctx.send("User is already banned")
        with open('ban.json', 'w') as storage:
            json.dump(bans, storage)


@bot.command(aliases=['pardon', 'Pardon', 'Unban'])
async def unban(ctx, user: discord.Member):
    if (ctx.author.id == 363396359841251328 or ctx.author.id == 233753795220209665):
        if (user.id in bans):
            bans.remove(user.id)
            await ctx.send("User has been unbanned")
        else:
            await ctx.send("User is not banned")
            with open('ban.json', 'w') as storage:
                json.dump(bans, storage)


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
