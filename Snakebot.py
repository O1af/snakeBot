import json
import discord
from discord.ext import commands

f = open('data.json', 'r+')
data = json.loads(f.read())
bot = commands.Bot(command_prefix = "sb/")


@bot.command()
async def snake(ctx, target : discord.Member):
    if(target.id not in data):
        data[target.id] = 1
    else:
        data[target.id] = data[target.id] + 1

    await ctx.send(target.name + "'s snakery has been noted")

@bot.command(aliases = ["snakecount", "Snakecount", "SnakeCount"])
async def getSnakeCount(ctx, target : discord.Member):
    await ctx.send(target.name + " has snaked people [" + data[target.name] + "]")

@bot.command()
async def stop(ctx, target : discord.Member):
    if (ctx.id == 363396359841251328):
        await ctx.send("Cya")
        f.write(json.dumps(data))
        f.close()
        bot.close()
        exit()

bot.run("ODEzMjE5NzU2Mzc5MjA5NzUw.YDMH6g.28B7F3kXly69LRn_q5QB_jl4KyA")
