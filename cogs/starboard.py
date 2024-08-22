import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from os import environ
from random import choice

load_dotenv("../.env")


class Starboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: nextcord.RawReactionActionEvent):
        msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        r_emojis = [r.emoji for r in msg.reactions]

        if environ["STB_REACTION_EMOJIS"] in r_emojis and msg.reactions[r_emojis.index(environ["STB_REACTION_EMOJIS"])].count >= int(environ["STB_REACTION_ADD_THRESH"]):
            embed = nextcord.Embed()
            
            embed.title = f"#{msg.channel.name}"
            
            embed.author.icon_url = msg.author.display_avatar.url
            embed.author.name = msg.author.display_name

            embed.description = msg.content

            embed.image.url = msg.attachments[0].url if len(msg.attachments) > 0 and msg.attachments[0].content_type.startswith("image") else None

            await self.bot.get_channel(int(environ["STB_CHANNEL_ID"])) \
                .send(embed=embed, content=f"-# [jump to message]({msg.jump_url}) | {msg.reactions[r_emojis.index(environ["STB_REACTION_EMOJIS"])].count}")
