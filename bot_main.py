import nextcord
import os.path
from os import listdir
from nextcord.ext import commands
from dotenv import dotenv_values

import cogs
from cogs import hoi, config, starboard, misc

from cogs.util import global_conf

description = '''bot for the gay nerds server

literally may from pokemon

she has that name because her creator briefly considered may as a chosen name'''

if os.path.exists("./data/config/description.txt"):
    with open("./data/config/description.txt", "rt") as desc:
        description = desc.read() if desc.read() != "" else "custom help description file is empty. L bozo"

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

dotenv_file = dotenv_values()

bot = commands.Bot(command_prefix=global_conf["general"]["prefix"], description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    bot.add_cog(hoi.HallOfInfamy(bot))
    bot.add_cog(misc.Misc(bot))
    bot.add_cog(starboard.Starboard(bot))
    bot.add_cog(config.ConfigCommands(bot))
    print("Added all cogs")
    #await cogs.hoi.remove_unwanted_hoi_posts(bot)
    if not os.path.exists("./data/extensions"):
        return
    
    for ext in listdir("./data/extensions"):
        bot.load_extension(f"data.extensions.{ext}.ext")

@bot.event
async def on_command_error(ctx: commands.Context, err: commands.CommandError):
    if isinstance(err, commands.CommandNotFound):
        return
    
    if isinstance(err, commands.CheckFailure):
        return

    embed = nextcord.Embed()

    embed.colour = nextcord.Colour.red()
    embed \
        .add_field(name="guild", 
                    value=ctx.guild.name, 
                    inline=True) \
        .add_field(name="command", 
                    value=f"{ctx.command.name}\n([jump]({ctx.message.jump_url}))", 
                    inline=True) \
        .add_field(name="error",
                    value=err)

    await bot.get_user(bot.owner_id) \
        .send("well dumbass you fucked up again!! here's the shit that needs fixing:",
                embed=embed)

TOKEN = dotenv_file["BOT_TOKEN"]
bot.run(TOKEN)
