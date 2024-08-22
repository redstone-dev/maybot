import nextcord
import dotenv
import os.path
from nextcord.ext import commands

description = '''bot for the gay nerds server

literally may from pokemon

she has that name because her creator briefly considered may as a chosen name'''

if os.path.exists("./bot-config/description.txt"):
    with open("./bot-config/description.txt", "rt") as desc:
        description = desc.read() if desc.read() != "" else "custom help description file is empty. L bozo"

intents = nextcord.Intents.default()
intents.message_content = True

dotenv_file = dotenv.dotenv_values()

bot = commands.Bot(command_prefix=dotenv_file["BOT_PREFIX"], description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    bot.load_extension("cogs.hoi")
    bot.load_extension("cogs.misc")
    bot.load_extension("cogs.oocqc")

TOKEN = dotenv_file["BOT_TOKEN"]
bot.run(TOKEN)
