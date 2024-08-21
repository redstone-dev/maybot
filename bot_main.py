import sys
import discord
import dotenv
import time
import os.path
# This example requires the 'members' and 'message_content' privileged intents to function.

from discord.ext import commands
import random

description = '''bot for the gay nerds server

literally may from pokemon

she has that name because her creator briefly considered may as a chosen name'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=':', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.tree.sync()
    await remove_unwanted_hoi_posts()

# @bot.command()
# async def add(ctx, left: int, right: int):    
    # """Adds two numbers together."""
    # await ctx.send(left + right)

@bot.hybrid_group(name="oocqc")
async def oocqc(ctx):
    return

@oocqc.command(name="random")
async def ooc_random(ctx):
    with open("oocqc.txt", "rt") as oocqc_file:
            oocqc_strings = oocqc_file.read().split("\n")
            if ctx.invoked_subcommand is None:  
                await ctx.reply(random.choice(oocqc_strings))   

@oocqc.command(name="line")
async def _oocqc_line(ctx, line: int):      
    with open("oocqc.txt", "rt") as oocqc_file:
        oocqc_strings = oocqc_file.read().split("\n")
        try:
            assert line < len(oocqc_strings)
        except:
            await ctx.reply()
        await ctx.reply(oocqc_strings[line - 1])

@oocqc.command(name="string")
async def _oocqc_string(ctx, string: str):
    with open("oocqc.txt", "rt") as oocqc_file:
        oocqc_strings = oocqc_file.read().split("\n")
        try:
            results = [s for s in oocqc_strings if string.lower() in s.lower()]
            results_formatted = discord.Embed(
                title=f"{len(results)} result{"s" if len(oocqc_strings) != 1 else ""} found for \"{string}\"", 
                description="\n".join(results)
                )
            if len(results_formatted) > 4096:
                await ctx.reply("only showing first 4096 characters")
                results_formatted = discord.Embed(
                    title=f"{len(results)} result{"s" if len(oocqc_strings) != 1 else ""} found for \"{string}\"", 
                    description="\n".join(results)[:4096]
                )
                await ctx.reply(embed=results_formatted)
            else:
                await ctx.reply(embed=results_formatted)
        except Exception as e:
            await ctx.reply(f"error. L bozo (probably <@807361784087707669>'s fault)\n```({e})```")
            print(e)

HOI_CHANNEL_ID = dotenv.dotenv_values()["HOI_CHANNEL_ID"]

@bot.group(name="infamy", aliases=["pin"])
async def hall_of_infamy(ctx: discord.Message, spoiler: bool | None):
    """
    only works with non-slash commands    
    """

    if ctx.invoked_subcommand is not None:
        return

    try:
        infamy_channel = bot.get_channel(int(HOI_CHANNEL_ID))

        og_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        embed_img = None
        if len(og_msg.attachments) > 0:
            embed_img = og_msg.attachments[0]

        embed = discord.Embed(
            title="#" + og_msg.channel.name,
            description=f"{"||" if spoiler else ""}{og_msg.content}{"||" if spoiler else ""}",
        )   
        embed.set_author(name=og_msg.author.display_name, icon_url=og_msg.author.display_avatar.url)
        embed.set_image(url=embed_img) if embed_img is not None else None

        sent_msg = await infamy_channel.send(content=f"-# [jump to original message](<{og_msg.jump_url}>) | infamy'd by <@{ctx.author.id}>", embed=embed)

        # with open("watching_ids.txt", "at") as watching_ids:
            # watching_ids.write(str(sent_msg.id) + "\n")    
        await ctx.reply("done :thumbs_up:")
    except AttributeError as e:
        print(e)
        await ctx.reply("you didnt reply to a message. L bozo")

@bot.command()
async def annihilate(ctx: discord.Message):
    try:
        og_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        response_msg = await ctx.reply("https://tenor.com/view/rocket-shi-rocket-bomb-gif-26885344")
        time.sleep(3.5)
        await og_msg.delete()
        await response_msg.delete()

        await ctx.reply("done :thumbs_up:")
    except AttributeError as e:
        print(e)
        await ctx.reply("you didnt reply to a message. L bozo")

@bot.command(name="3")
async def colon_3(ctx: commands.Context):
    """
    <- so that maybot replies with :3 when you send it too
    """
    await ctx.channel.send(":3")

@bot.hybrid_command(name="rule")
async def rules(ctx: commands.Context, line):
    if not os.path.exists("./rules.txt"):
        await ctx.reply("you dont have a `rules.txt` file. L bozo")
        return
    
    with open("rules.txt", "rt") as r:
        rules = r.read().strip().split("\n")
        if int(line) > len(rules) or int(line) < 1:
            await ctx.reply("that number is too small or too big. L bozo")
            return
        await ctx.reply(rules[int(line) - 1])

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    await remove_unwanted_hoi_posts() if payload.channel_id == HOI_CHANNEL_ID else None 

async def remove_unwanted_hoi_posts():
    try:
        infamy_channel: discord.TextChannel = bot.get_channel(int(HOI_CHANNEL_ID))
        messages = [
            msg async for msg in infamy_channel.history(limit=1024)
            if msg.author.id == bot.application_id
        ]
        for message in messages:
            r_emojis = [r.emoji for r in message.reactions]
            if "❌" in r_emojis and message.reactions[r_emojis.index("❌")].count >= 5:
                message.delete()    
            time.sleep(0.5)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        sys.exit(0)

TOKEN = dotenv.dotenv_values(".env")["BOT_TOKEN"]


bot.run(TOKEN)
