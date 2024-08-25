import nextcord
from nextcord.ext import commands
from os.path import exists
from .util import global_conf



class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command(name="sync-tree")
    @commands.is_owner()
    async def sync_tree(self, ctx: commands.Context):
        """globally syncs the command tree"""
        await self.bot.sync_all_application_commands()
        await ctx.reply("done :thumbs_up:")

    @commands.command(name="stats")
    async def stats(self, ctx: commands.Context):
        """shows various stats"""
        embed = nextcord.Embed() \
            .add_field(name="latency", 
                       value=f"{int(self.bot.latency * 1000)}ms",
                       inline=True) 

        await ctx.reply(embed=embed)
    
    @commands.is_owner()
    @commands.command(name="reload-defaults")
    async def reload_config(self, ctx: commands.Context):
        global_conf.reload_config()
        await ctx.reply("done :thumbs_up:")

    @reload_config.error
    @sync_tree.error
    @stats.error
    async def _not_admin_err(self, ctx: commands.Context, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("wait, you're not the owner. L bozo")

    @nextcord.slash_command(description="get line from rules.txt")
    async def rule(self, interaction: nextcord.Interaction, line: int):
        if not exists("./data/config/rules.txt"):
            await interaction.response.send_message(
                "you dont have a `rules.txt` file. L bozo"
            )

        with open("./data/config/rules.txt", "rt") as rules:
            rules_list = rules.read().split("\n")
            if line < 1:
                await interaction.response.send_message(
                    "you can't have negative or zero rules wtf? L bozo"
                )
                return
            if line > len(rules_list):
                await interaction.response.send_message(
                    "that's more rules than there are in rules.txt!! what is this, 1984? L bozo"
                )
                return
            
            await interaction.response.send_message(rules_list[line - 1])