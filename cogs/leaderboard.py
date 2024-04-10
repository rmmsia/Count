import discord
import os
from pymongo import MongoClient
from discord.ext import commands

connection_string = os.environ["CONNECTION"]
cluster = MongoClient(connection_string)

counterData = cluster["discord"]["count data"]

class leaderboard(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(name = "leaderboard", aliases = ["top"])
  async def leaderboard(self, ctx):
    # id = ctx.message.author.id
    # uStats = counterData.find_one({"id": id})
    rankings = counterData.find().sort([("loop", -1), ("count", -1)])

    i = 1
    lbembed = discord.Embed(title="Global Leaderboard")


    for x in rankings: # For each user on the leaderboard
      try:
        user1 = int(x["id"]) # Gets user ID

        user = await self.bot.fetch_user(user1) # Gets username
        userloop = x["loop"]
        usercount = x["count"]

        lbembed.add_field(name=f"{i}. {str(user.name)}", value=f"Loop **{userloop}**, Count = **{usercount}**", inline=False)
        i += 1
      except:
        pass
      
      if i == 11:
        break
    
    await ctx.channel.send(embed=lbembed)
    

async def setup(bot):
  await bot.add_cog(leaderboard(bot))     