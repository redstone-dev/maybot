import nextcord
from nextcord.ext import commands
from random import choice
from .util import global_conf



class Starboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: nextcord.RawReactionActionEvent):
        global_conf.reload_config()
        
        msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        r_emojis = [r.emoji for r in msg.reactions]

        if global_conf["starboard"]["reactions"]["allowed_emojis"] in r_emojis and msg.reactions[r_emojis.index(global_conf["starboard"]["reactions"]["allowed_emojis"])].count == global_conf["starboard"]["reactions"]["add_thresh"]:
            embed = nextcord.Embed()
            
            embed.title = f"#{msg.channel.name}"
            
            embed.author.icon_url = msg.author.display_avatar.url
            embed.author.name = msg.author.display_name

            embed.description = msg.content

            embed.image.url = msg.attachments[0].url if len(msg.attachments) > 0 else None

            await self.bot.get_channel(int(global_conf["starboard"]["channel_id"])) \
                .send(embed=embed, content=f"-# [jump to message]({msg.jump_url}) | {global_conf['starboard']['reactions']['allowed_emojis']}{msg.reactions[r_emojis.index(global_conf['starboard']['reactions']['allowed_emojis'])].count}")
