import json
import discord
from discord.ext import commands

f = open('data.json', 'r+')
data = json.loads(f.read())
bot = commands.Bot(command_prefix="sb/")


@bot.command()
async def snake(ctx, target: discord.Member):
    if(str(target.name) not in data):
        data[target.name] = 1
    else:
        data[target.name] = int(data[target.name]) + 1
    await ctx.send(target.name + "'s snakery has been noted")
    with open('data.json', 'w') as storage:
        json.dump(data, storage)


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
    await ctx.send(snakes)


@ bot.command()
async def stop(ctx, target: discord.Member):
    if (ctx.id == 363396359841251328):
        await ctx.send("Cya")
        f.write(json.dumps(data))
        f.close()
        bot.close()
        exit()
token = open('token.txt', 'r')
botToken = token.read()
bot.run(botToken)
