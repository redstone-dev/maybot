import nextcord
from nextcord.ext import commands
from random import choice
from .util import Config

conf = Config("./bot-config/bot_settings.json")

class OOCQC(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    
    def setup(self):
        pass

    @nextcord.slash_command()
    async def oocqc(self, interaction: nextcord.Interaction):
        pass

    @oocqc.subcommand(description="gets a specific string from oocqc")
    async def string(self, interaction: nextcord.Interaction, string: str):
        """
        searches for a specific string in oocqc
        """
        with open("oocqc.txt", "rt") as oocqc_file:
            oocqc_strings = oocqc_file.read().split("\n")
            try:
                results = [s for s in oocqc_strings if string.lower() in s.lower()]
                results_formatted = nextcord.Embed(
                    title=f"{len(results)} result{'s' if len(oocqc_strings) != 1 else ''} found for \"{string}\"",
                    description="\n".join(results),
                )
                OOC_EMBED_CHAR_LIMIT = int(conf["OOC_EMBED_CHAR_LIMIT"])
                if len(results_formatted) > OOC_EMBED_CHAR_LIMIT:
                    results_formatted = nextcord.Embed(
                        title=f"{len(results)} result{'s' if len(oocqc_strings) != 1 else ''} found for \"{string}\"",
                        description="\n".join(results)[:OOC_EMBED_CHAR_LIMIT],
                    )
                    await interaction.response.send_message(
                        embed=results_formatted,
                        content=f"only showing first {OOC_EMBED_CHAR_LIMIT} characters",
                    )
                else:
                    await interaction.response.send_message(embed=results_formatted)
            except Exception as e:
                await interaction.response.send_message(
                    f"error. L bozo (probably <@{self.bot.owner_id}>'s fault)",
                )
                print(e)

    @oocqc.subcommand(description="gets a random string from oocqc")
    async def random(self, interaction: nextcord.Interaction):
        with open("oocqc.txt", "rt") as oocqc_file:
            oocqc_strings = oocqc_file.read().split("\n")
            await interaction.response.send_message(choice(oocqc_strings))

    @oocqc.subcommand(description="get the quote in the oocqc file at a specified line")
    async def line(self, interaction: nextcord.Interaction, line: int):
        """
        specific line from oocqc file
        """
        with open("oocqc.txt", "rt") as oocqc_file:
            oocqc_strings = oocqc_file.read().split("\n")
            try:
                assert line < len(oocqc_strings)
            except:
                await interaction.response.send_message("wow that line is out of this world!1!! L bozo", ephemeral=True)
            await interaction.response.send_message(content=oocqc_strings[line - 1])