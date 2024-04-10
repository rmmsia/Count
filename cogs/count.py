import discord
import os
from pymongo import MongoClient
from discord.ext import commands

connection_string = os.environ['CONNECTION']
cluster = MongoClient(connection_string)

counterData = cluster["discord"]["count data"]

class count(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.cooldown(1, 2.5, commands.BucketType.user)
  @commands.command(name = "count", aliases = ["c"])
  async def count(self, ctx):
    id = ctx.message.author.id
    uStats = counterData.find_one({"id": id})
    if uStats is None: # creates new user stats for new user
      newuser = {
        "id": id,
        "count": 0,
        "x": 1,
        "a": 0,
        "b": 0,
        "c": 0,
        "d": 1,
        "po2": 1,
        "pts": 0,
        "loop": 0,
        "unlocka": "false",
        "unlockb": "false",
        "unlockc": "false",
        }
      counterData.insert_one(newuser)
      newEmbed = discord.Embed(title=f"Hi {ctx.message.author.name}!", description = "Welcome to Count! Start counting with `.count`!")
      await ctx.send(embed=newEmbed)
    else:
      # Let's get some variables going
      count_now = uStats["count"]
      po2 = uStats["po2"]
      x = uStats["x"]
      a = uStats["a"]

      y = x**a
      b = uStats["b"]

      z = y**b
      c = uStats["c"]

      d = uStats["d"]

      # The counting engine
      increment = ((x**a)*(y**b)*(z**c))**d
      newCount = round(count_now + increment, 3)

      # Update user's count
      counterData.update_one({"id": id}, {"$set":{"count":newCount}})

      # Send in an embed, letting the user now the count has increased. Scientific notation is only applied if count is over 10**10.
      if newCount > 10**6:
        newCountformatted = "{:.2e}".format(newCount)
        embed = discord.Embed(description=f"Count increased to **{newCountformatted}**")
      else:
        embed = discord.Embed(description=f"Count increased to **{newCount}**")

      embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.display_avatar)
      await ctx.send(embed=embed)
      
      # Check if OoM (order of magnitude) increases. Give an upgrade point if true.
      
      
      if newCount >= 2 ** po2:
        newoom = po2 + 1

        counterData.update_one({"id": id}, {"$set":{"po2":newoom}})

        newPts = uStats["pts"] + 1
        counterData.update_one({"id": id}, {"$set":{"pts":newPts}})

        await ctx.channel.send("Your count has increased by one power of 2.")
        await ctx.channel.send("You have gained **1 Upgrade Point.**")
      else:
        pass
      
      # Loop if over 2^63 - 1. Loop increases by 1. d decreases by 0.01
      if newCount > (2**63 - 1):
        newLoop = uStats["loop"] + 1
        if uStats["d"] > 0:
          newDvalue = uStats["d"] - 0.01
        counterData.update_one({"id": id}, {"$set":{"count": 1, "x": 1, "a": 0, "b": 0, "c": 0, "d": newDvalue, "po2": 1, "pts": 0, "unlocka": "false", "unlockb" : "false", "unlockc": "false", "loop":newLoop}})
        loopembed=discord.Embed(title="Congratulations!", description="You have looped as your count exceeded 2⁶³ -1. Count reset to 1.")
        loopembed.set_footer(text=f"You are now on Loop {newLoop}.")
        await ctx.send(embed=loopembed)


  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      coolembed = discord.Embed(description=f'Command on cooldown. You can count again in **{round(error.retry_after, 1)}** seconds.')
      await ctx.send(embed=coolembed)
    
async def setup(bot):
  await bot.add_cog(count(bot))     