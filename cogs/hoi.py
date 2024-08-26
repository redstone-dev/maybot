import nextcord
from nextcord.ext import commands
from time import sleep
from .util import global_conf

import nextcord.ext



async def remove_unwanted_hoi_posts(bot: nextcord.ext.commands.Bot):
    try:
        infamy_channel: nextcord.TextChannel = bot.get_channel(global_conf["hoi"]["channel_id"])
        messages = [
            msg async for msg in infamy_channel.history(limit=1024)
            if msg.author.id == bot.application_id
        ]
        for message in messages:
            r_emojis = [r.emoji for r in message.reactions]

            if "❌" in r_emojis and message.reactions[r_emojis.index("❌")].count >= global_conf["hoi"]["reaction_removal_thresh"]:
                await message.delete()
    except Exception as e:
        print(e)

class HallOfInfamy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    
    async def send_to_hoi(self, og_msg: nextcord.Message, user: nextcord.User, /, spoiler: bool):
        embed_img = None
        if len(og_msg.attachments) > 0:
            embed_img = og_msg.attachments[0]

        embed = nextcord.Embed(
            title="#" + og_msg.channel.name,
            description=f"{'||' if spoiler else ''}{og_msg.content}{'||' if spoiler else ''}",
        ) 
        embed.set_author(name=og_msg.author.display_name, icon_url=og_msg.author.display_avatar.url)
        embed.set_image(url=embed_img) if embed_img is not None else None

        guild_conf = global_conf["guild:" + str(og_msg.guild.id)]
        await self.bot.get_channel(guild_conf["hoi"]["channel_id"]).send(
            content=f"-# [jump to original message](<{og_msg.jump_url}>) | inducted by {user.mention}", 
            embed=embed)
    
    @nextcord.message_command(name="Send to Hall of Infamy")
    async def hoi_context_menu(self, interaction: nextcord.Interaction, message: nextcord.Message):
        await self.send_to_hoi(message, interaction.user, spoiler=False)
        await interaction.response.send_message("sent :thumbs_up:", ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: nextcord.RawReactionActionEvent):
        msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        r_emojis = [r.emoji for r in msg.reactions]

        guild_conf = global_conf["guild:" + str(payload.guild_id)]

        if "❌" in r_emojis and msg.reactions[r_emojis.index("❌")].count >= int(guild_conf["hoi"]["reaction_removal_thresh"]):
            await msg.delete()