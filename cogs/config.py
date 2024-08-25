import nextcord
from nextcord.ext import commands
from .util import global_conf

class ConfigCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @nextcord.slash_command()
    async def config(self, interaction: nextcord.Interaction):
        pass

    @config.subcommand(description="set which channel ID to use for the hall of infamy")
    async def _cfg_set_hoi(self, interaction: nextcord.Interaction, id: int):
        global_conf["guild:" + interaction.guild_id]["hoi"]["channel_id"] = id

    @config.subcommand(description="set which channel ID to use for the starboard")
    async def _cfg_set_stb(self, interaction: nextcord.Interaction, id: int):
        global_conf["guild:" + interaction.guild_id]["starboard"]["channel_id"] = id