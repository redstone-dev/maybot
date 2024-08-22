import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from os import environ
from os.path import exists

load_dotenv()


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    def setup(self):
        pass

    @commands.command(name="sync-tree")
    @commands.is_owner()
    async def sync_tree(self, ctx: commands.Context):
        """globally syncs the command tree"""
        await self.bot.sync_all_application_commands()
        ctx.reply("done :thumbs_up:")

    @sync_tree.error
    async def _sync_tree_err(self, ctx: commands.Context, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("wait, you're not the owner. L bozo")

    @nextcord.slash_command(description="get line from rules.txt")
    async def rule(self, interaction: nextcord.Interaction, line: int):
        if not exists("./bot-config/rules.txt"):
            await interaction.response.send_message(
                "you dont have a `rules.txt` file. L bozo"
            )

        with open("./bot-config/rules.txt", "rt") as rules:
            rules_list = rules.split("\n")
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
