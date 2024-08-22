import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from os import environ
from time import sleep

import nextcord.ext
import nextcord.ext.commands

load_dotenv("../.env")

async def remove_unwanted_hoi_posts(bot: nextcord.ext.commands.Bot):
    try:
        infamy_channel: nextcord.TextChannel = bot.get_channel(int(environ["HOI_CHANNEL_ID"]))
        messages = [
            msg async for msg in infamy_channel.history(limit=1024)
            if msg.author.id == bot.application_id
        ]
        for message in messages:
            r_emojis = [r.emoji for r in message.reactions]

            if "❌" in r_emojis and message.reactions[r_emojis.index("❌")].count >= int(environ["HOI_REACTION_REMOVAL_THRESH"]):
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

        await self.bot.get_channel(int(environ["HOI_CHANNEL_ID"])).send(
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

        if "❌" in r_emojis and msg.reactions[r_emojis.index("❌")].count >= int(environ["HOI_REACTION_REMOVAL_THRESH"]):
            await msg.delete()