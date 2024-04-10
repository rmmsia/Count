import discord
import os
from pymongo import MongoClient
from discord.ext import commands

connection_string = os.environ['CONNECTION']
cluster = MongoClient(connection_string)

counterData = cluster["discord"]["count data"]

class shop(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(name = "shop", aliases = ["s"])
  async def shop(self, ctx):
    id = ctx.message.author.id
    uStats = counterData.find_one({"id": id})
    x = round(uStats["x"], 2)
    a = round(uStats["a"], 2)
    b = round(uStats["b"], 2)
    c = round(uStats["c"], 2)

    astatus = uStats["unlocka"]
    bstatus = uStats["unlockb"]
    cstatus = uStats["unlockc"]

    pts = uStats["pts"]

    embed = discord.Embed(title="The Shop", description="Upgrade your increment equation using **Upgrade Points**. Use `.buy <item>`. Unlock exponent variables with `.buy unlock<letter>` (without spaces).")
    embed.add_field(name="Upgrade Points", value=pts, inline=False)
    embed.add_field(name="x", value=x, inline=True)
    if astatus == 'false':
      embed.add_field(name="a", value="locked", inline=True)
    elif astatus == 'true':
      embed.add_field(name="a", value=a, inline=True)
    if bstatus == 'false':
      embed.add_field(name="b", value="locked", inline=True)
    elif bstatus == 'true':
      embed.add_field(name="b", value=b, inline=True)
    if cstatus == 'false':
      embed.add_field(name="c", value="locked", inline=True)
    elif cstatus == 'true':
      embed.add_field(name="c", value=c, inline=True)
    await ctx.send(embed=embed)

  @commands.command(name = "buy", aliases=["b"])
  async def buy(self, ctx, item):
    id = ctx.message.author.id
    uStats = counterData.find_one({"id": id})

    astatus = uStats["unlocka"]
    bstatus = uStats["unlockb"]
    cstatus = uStats["unlockc"]

    if uStats["pts"] != 0:
      if str(item) == 'x':
        if uStats["x"] >= 1.9:
          embed=discord.Embed(description="You have maxed out **x**!")
          await ctx.send(embed=embed)
        elif uStats["x"] < 1.9:
          newPts = uStats["pts"] - 1
          newVar = round(uStats["x"] + 0.1, 1)
          counterData.update_one({"id": id}, {"$set":{"pts":newPts, "x" : newVar}})
          embed=discord.Embed(title="Purchase successful", description=f"**x** value increased to {newVar}!")
          await ctx.send(embed=embed)
      
      if str(item) == 'unlocka':
        if astatus == 'true':
          embed=discord.Embed(description="You have already unlocked **a**.")
          await ctx.send(embed=embed)
        elif bstatus == 'false':
          newPts = uStats["pts"] - 1
          counterData.update_one({"id": id}, {"$set":{"pts":newPts, "unlocka" : "true", "a" : 1}})
          await ctx.send("**a** unlocked")

      if str(item) == 'unlockb':
        if bstatus == 'true':
          embed=discord.Embed(description="You have already unlocked **b**.")
          await ctx.send(embed=embed)
        elif bstatus == 'false':
          newPts = uStats["pts"] - 1
          counterData.update_one({"id": id}, {"$set":{"pts":newPts, "unlockb" : "true", "b" : 1}})
          await ctx.send("**b** unlocked")

      if str(item) == 'unlockc':
        if cstatus == 'true':
          embed=discord.Embed(description="You have already unlocked **c**.")
          await ctx.send(embed=embed)
        elif cstatus == 'false':
          newPts = uStats["pts"] - 1
          counterData.update_one({"id": id}, {"$set":{"pts":newPts, "unlockc" : "true", "c" : 1}})
          await ctx.send("**c** unlocked")
      
      if str(item) == 'a':
        if astatus == 'false':
          embed=discord.Embed(description="You have not unlocked **a** yet!")
          await ctx.send(embed=embed)
        elif astatus == 'true':
          if uStats["a"] >= 5:
            embed=discord.Embed(description="You have maxed out **a**!")
            await ctx.send(embed=embed)
          elif uStats["a"] < 5:
            newPts = uStats["pts"] - 1
            newVar = round(uStats["a"] + 0.5, 1)
            counterData.update_one({"id": id}, {"$set":{"pts":newPts, "a" : newVar}})
            embed=discord.Embed(title="Purchase successful", description=f"**a** value increased to {newVar}!")
            await ctx.send(embed=embed)
      
      if str(item) == 'b':
        if bstatus == 'false':
          embed=discord.Embed(description="You have not unlocked **b** yet!")
          await ctx.send(embed=embed)
        elif bstatus == 'true':
          if uStats["b"] >= 5:
            embed=discord.Embed(description="You have maxed out **b**!")
            await ctx.send(embed=embed)
          elif uStats["b"] < 5:
            newPts = uStats["pts"] - 1
            newVar = round(uStats["b"] + 0.5, 1)
            counterData.update_one({"id": id}, {"$set":{"pts":newPts, "b" : newVar}})
            embed=discord.Embed(title="Purchase successful", description=f"**b** value increased to {newVar}!")
            await ctx.send(embed=embed)
      
      if str(item) == 'c':
        if cstatus == 'false':
          embed=discord.Embed(description="You have not unlocked **c** yet!")
          await ctx.send(embed=embed)
        elif cstatus == 'true':
          if uStats["c"] >= 1.5:
            embed=discord.Embed(description="You have maxed out **b**!")
            await ctx.send(embed=embed)
          elif uStats["c"] < 1.5:
            newPts = uStats["pts"] - 1
            newVar = round(uStats["c"] + 0.1, 1)
            counterData.update_one({"id": id}, {"$set":{"pts":newPts, "c" : newVar}})
            embed=discord.Embed(title="Purchase successful", description=f"**c** value increased to {newVar}!")
            await ctx.send(embed=embed)

    else:
      embed=discord.Embed(description=f"You don't have enough upgrade points.")
      await ctx.send(embed=embed)
      
      

async def setup(bot):
  await bot.add_cog(shop(bot))        