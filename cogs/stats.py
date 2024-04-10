import discord
import os
from pymongo import MongoClient
from discord.ext import commands

connection_string = os.environ["CONNECTION"]
cluster = MongoClient(connection_string)

counterData = cluster["discord"]["count data"]

class stats(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(name = "stats", aliases = ["p"])
  async def stats(self, ctx):
    id = ctx.message.author.id
    uStats = counterData.find_one({"id": id})

    count_now = uStats["count"]
    x = round(uStats["x"], 2)
    a = round(uStats["a"], 2)
    b = round(uStats["b"], 2)
    c = round(uStats["c"], 2)
    d = uStats["d"]
    po2 = uStats["po2"]
    loop = uStats["loop"]

    y = x**a
    z = y**b

    increment = round(((x**a)*(y**b)*(z**c))**d, 3)

    if increment > 10**6:
      increment = "{:.2e}".format(increment)

    embed = discord.Embed(title=f"Stats of {ctx.message.author.name}", description=f"**Increment Equation**: (xᵃ)(yᵇ)(zᶜ)")
    embed.add_field(name="Where:", value="y = xᵃ, z = yᵇ", inline=False)
    if loop > 0:
      embed.add_field(name="Loop", value=f"{loop}", inline=False)
    embed.add_field(name="Current Count", value = f"{count_now}", inline=True)
    embed.add_field(name="Increment", value = f"{increment}", inline=True)
    embed.add_field(name="Next Upgrade", value = f"{2**po2}", inline=True)
    embed.set_footer(text=f"x = {x}, a = {a}, b = {b}, c = {c}")

    await ctx.send(embed=embed)
    
    

async def setup(bot):
  await bot.add_cog(stats(bot))        