import nextcord
from nextcord.ext import commands
from nextcord.ext import application_checks
from .util import global_conf

class ConfigCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @application_checks.has_permissions(manage_channels=True)
    @nextcord.slash_command(name="guild-config")
    async def config(self, interaction: nextcord.Interaction):
        pass
    
    @application_checks.has_permissions(manage_channels=True)
    @config.subcommand(name="hoi-channel", description="set which channel ID to use for the hall of infamy")
    async def _cfg_set_hoi(self, interaction: nextcord.Interaction, id: str):
        if not id.isnumeric():
            await interaction.response.send_message("wait, that's not a valid number. L bozo")
            return
        global_conf["guild:" + str(interaction.guild_id)]["hoi"]["channel_id"] = int(id)
        await interaction.response.send_message("done :thumbs_up:", ephemeral=True)

    @application_checks.has_permissions(manage_channels=True)
    @config.subcommand(name="starboard-channel", description="set which channel ID to use for the starboard")
    async def _cfg_set_stb(self, interaction: nextcord.Interaction, id: str):
        if not id.isnumeric():
            await interaction.response.send_message("wait, that's not a valid number. L bozo")
            return
        global_conf["guild:" + str(interaction.guild_id)]["starboard"]["channel_id"] = id
        await interaction.response.send_message("done :thumbs_up:", ephemeral=True)

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: nextcord.Interaction, error: Exception):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.response.send_message("wait, you don't have permissions for that. L bozo")
            return
        