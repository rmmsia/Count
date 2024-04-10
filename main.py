import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=".", intents=intents)

# Startup things...
@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(name=".count"))
  await load()
  print("Count Online. {0.user}".format(bot))

async def load():
  cogs_list = ['count', 'leaderboard', 'shop', 'stats']
  for cog in cogs_list:
    await bot.load_extension(f'cogs.{cog}')
'''
# Cog loading
initial_extensions = []

for filename in os.listdir("./cogs"): # Look through files in cogs folder, then add to initial_extensions list if ending with .py
  print(filename)
  if filename.endswith('.py'):
    initial_extensions.append("cogs." + filename[:-3]) # Take out .py so it'll work.
'''
if __name__ == '__main__':
  '''
  for extension in initial_extensions:
    bot.load_extension(extension)
'''

keep_alive()

bot.run(os.environ["TOKEN"])