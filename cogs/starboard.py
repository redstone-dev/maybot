import nextcord
from nextcord.ext import commands
from random import choice
from .util import global_conf

class Starboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: nextcord.RawReactionActionEvent):
        msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        r_emojis = [r.emoji for r in msg.reactions]

        guild_conf = global_conf["guild:" + str(payload.guild_id)]
        guild_allowed_emojis = guild_conf["starboard"]["reactions"]["allowed_emojis"]
        reaction_count = msg.reactions[r_emojis.index(guild_allowed_emojis)].count

        if guild_allowed_emojis in r_emojis \
        and reaction_count == guild_conf["starboard"]["reactions"]["add_thresh"]:
            embed = nextcord.Embed()
            
            embed.title = f"#{msg.channel.name}"
            
            embed.author.icon_url = msg.author.display_avatar.url
            embed.author.name = msg.author.display_name

            embed.description = msg.content

            embed.set_image(msg.attachments[0].url if len(msg.attachments) > 0 else None)

            await self.bot.get_channel(int(guild_conf["starboard"]["channel_id"])) \
                .send(embed=embed, content=f"-# [jump to message]({msg.jump_url}) | {guild_allowed_emojis}{reaction_count}")