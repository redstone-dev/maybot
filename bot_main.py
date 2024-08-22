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

if os.path.exists("./bot-config/description.txt"):
    with open("./bot-config/description.txt", "rt") as desc:
        description = desc.read() if desc.read() != "" else "custom help description file is empty. L bozo"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

dotenv_file = dotenv.dotenv_values()

bot = commands.Bot(command_prefix=dotenv_file["BOT_PREFIX"], description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await remove_unwanted_hoi_posts()

@bot.command(name="sync-tree")
async def sync_tree(ctx: commands.Context):
    """
    command to sync the command tree
    only works if youre the owner
    """
    if ctx.author.id != int(dotenv_file["OWNER_USER_ID"]):
        await ctx.reply("this command can only be used by the owner of the bot. L bozo")
        return
    
    bot_reply = await ctx.reply("doing...")

    if any(await bot.tree.sync()):
        await bot_reply.edit(content="done :thumbs_up:")
    else:
        await bot_reply.edit(content="something went wrong with syncing. L bozo")

@bot.hybrid_group(name="oocqc")
async def oocqc(ctx):
    """get stuff from a bunch of messages out of context"""
    return

@oocqc.command(name="random")
async def ooc_random(ctx):
    """
    random string from oocqc
    """
    with open("oocqc.txt", "rt") as oocqc_file:
            oocqc_strings = oocqc_file.read().split("\n")
            if ctx.invoked_subcommand is None:  
                await ctx.reply(random.choice(oocqc_strings))   

@oocqc.command(name="line")
async def _oocqc_line(ctx, line: int):
    """
    specific line from oocqc file
    """
    with open("oocqc.txt", "rt") as oocqc_file:
        oocqc_strings = oocqc_file.read().split("\n")
        try:
            assert line < len(oocqc_strings)
        except:
            await ctx.reply("wow that line is out of this world!1!! L bozo")
        await ctx.reply(oocqc_strings[line - 1])

@oocqc.command(name="string")
async def _oocqc_string(ctx, string: str):
    """
    searches for a specific string in oocqc
    """
    with open("oocqc.txt", "rt") as oocqc_file:
        oocqc_strings = oocqc_file.read().split("\n")
        try:
            results = [s for s in oocqc_strings if string.lower() in s.lower()]
            results_formatted = discord.Embed(
                title=f"{len(results)} result{'s' if len(oocqc_strings) != 1 else ''} found for \"{string}\"", 
                description="\n".join(results)
                )
            OOC_EMBED_CHAR_LIMIT = int(dotenv_file["OOC_EMBED_CHAR_LIMIT"])
            if len(results_formatted) > OOC_EMBED_CHAR_LIMIT:
                await ctx.reply(f"only showing first {OOC_EMBED_CHAR_LIMIT} characters")
                results_formatted = discord.Embed(
                    title=f"{len(results)} result{'s' if len(oocqc_strings) != 1 else ''} found for \"{string}\"", 
                    description="\n".join(results)[:OOC_EMBED_CHAR_LIMIT]
                )
                await ctx.reply(embed=results_formatted)
            else:
                await ctx.reply(embed=results_formatted)
        except Exception as e:
            await ctx.reply(f"error. L bozo (probably <@{dotenv_file['OWNER_USER_ID']}>'s fault)\n```({e})```")
            print(e)

@oocqc.command(name="lineof")
async def _oocqc_lineof(ctx, string: str):
    """
    get line number of specific quote
    """
    with open("oocqc.txt", "rt") as oocqc_file:
        oocqc_strings = oocqc_file.read().split("\n")
        try:
            await ctx.reply(oocqc_strings.index(string) + 1)
        except ValueError:
            await ctx.reply("try wrapping the string in quotes and escaping any quotes that are inside of that. L bozo")

HOI_CHANNEL_ID = int(dotenv_file["HOI_CHANNEL_ID"])

async def send_to_hoi(og_msg: discord.Message, user: discord.User, /, spoiler: bool):
    embed_img = None
    if len(og_msg.attachments) > 0:
        embed_img = og_msg.attachments[0]

    embed = discord.Embed(
        title="#" + og_msg.channel.name,
        description=f"{"||" if spoiler else ""}{og_msg.content}{"||" if spoiler else ""}",
    ) 
    embed.set_author(name=og_msg.author.display_name, icon_url=og_msg.author.display_avatar.url)
    embed.set_image(url=embed_img) if embed_img is not None else None

    await bot.get_channel(int(HOI_CHANNEL_ID)).send(
        content=f"-# [jump to original message](<{og_msg.jump_url}>) | inducted by <@{user.id}>", 
        embed=embed)

@bot.hybrid_group(name="infamy", aliases=["hoi"])
async def hoi(ctx: commands.Context, spoiler: bool | None):
    """
    sends a message to the hall of infamy
    only the id subcommand works as a slash command
    """
    
    if ctx.invoked_subcommand:
        return

    try:
        send_to_hoi(ctx.message.reference, ctx.author)
    
        await ctx.reply("done :thumbs_up:")
    except AttributeError as e:
        await ctx.reply("you didnt reply to a message. L bozo")

@hoi.command(name="id")
async def _c_hoi_id(ctx, _id: str, spoiler: bool | None):
    """
    add to hall of infamy using the id of a message (for slash commands)
    """
    try:
        id = int(_id)
        infamy_channel = bot.get_channel(HOI_CHANNEL_ID)

        og_msg = await ctx.channel.fetch_message(id)

        embed_img = None
        if len(og_msg.attachments) > 0:
            embed_img = og_msg.attachments[0]

        embed = discord.Embed(
            title="#" + og_msg.channel.name,
            description=f"{"||" if spoiler else ""}{og_msg.content}{"||" if spoiler else ""}",
        ) 
        embed.set_author(name=og_msg.author.display_name, icon_url=og_msg.author.display_avatar.url)
        embed.set_image(url=embed_img) if embed_img is not None else None

        await infamy_channel.send(
            content=f"-# [jump to original message](<{og_msg.jump_url}>) | infamy'd by <@{ctx.author.id}>", 
            embed=embed)
    
        await ctx.reply("done :thumbs_up:")
    except AttributeError as e:
        await ctx.reply("you didnt reply to a message. L bozo")
    except commands.errors.HybridCommandError:
        await ctx.reply("message doesnt exist. L bozo")
    except TypeError:
        await ctx.reply("not a number. L bozo")
    
@bot.tree.context_menu(name='Induct into the Hall of Infamy')
async def add_to_infamy(interaction: discord.Interaction, message: discord.Message):

    """
    add to hall of infamy using the id of a message (for slash commands)
    """
    await send_to_hoi(message, interaction.user, spoiler=False)

    await interaction.response.send_message("done :thumbs_up:", silent=True)

@bot.command()
async def annihilate(ctx: discord.Message):
    """ 
    delete a message with a missile >:)
    """
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
async def rules(ctx: commands.Context, line: int | None):
    """get a rule from rules.txt"""

    if not os.path.exists("./bot-config/rules.txt"):
        await ctx.reply("you dont have a `rules.txt` file. L bozo")
        return
    
    if line is None:
        await ctx.reply("you didnt give a line number. L bozo")
        return
    
    with open("./bot-config/rules.txt", "rt") as r:
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
        infamy_channel: discord.TextChannel = bot.get_channel(HOI_CHANNEL_ID)
        messages = [
        msg async for msg in infamy_channel.history(limit=1024)
            if msg.author.id == bot.application_id
        ]
        for message in messages:
            r_emojis = [r.emoji for r in message.reactions]
            HOI_REACTION_REMOVAL_THRESH = dotenv_file["HOI_REACTION_REMOVAL_THRESH"]
            if "❌" in r_emojis \
                and message.reactions[r_emojis.index("❌")].count >= int(HOI_REACTION_REMOVAL_THRESH):
                await message.delete()    
            time.sleep(0.5)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        sys.exit(0)

TOKEN = dotenv_file["BOT_TOKEN"]
bot.run(TOKEN)
