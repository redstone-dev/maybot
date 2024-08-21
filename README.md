# maybot
- A bot for my private server with friends that I'm open-sourcing because yes.
- Made with discord.py.
- The default prefix is `:`.
- Use `:help` to get a command list. The output should look something like this:
```
bot for the gay nerds server

literally may from pokemon

she has that name because her creator briefly considered may as a chosen name

​No Category:
  3          <- so that maybot replies with :3 when you send it too
  annihilate delete a message with a missile >:)
  help       Shows this message
  infamy     sends a message to the hall of infamy
  oocqc      get stuff from a bunch of messages out of context
  rule       get a rule from rules.txt
  sync-tree  command to sync the command tree

Type :help command for more info on a command.
You can also type :help category for more info on a category.
```

## Configuring Rules
Create a file with the path `bot-config/rules.txt` and just put your rules in line by line like this:
```
rule 1
rule 2
the third one
```
When you run `/rule x`, maybot will reply with the rule on that line number in `rules.txt`.

## Custom Bot Description
In the same `bot-config` directory, you can add a `description.txt`. Whatever is in there will replace the default bot description when running `:help`.

## Other Config
Make a `.env` file in the same directory as `bot_main.py` and add this to it:
```
# User IDs for the bot to function
BOT_TOKEN=
OWNER_USER_ID=

# Bot config stuff
BOT_PREFIX=:
OOC_EMBED_CHAR_LIMIT=4096
HOI_CHANNEL_ID=
HOI_REACTION_REMOVAL_THRESH=3
```
Add your bot token, own user ID, and ID of the channel you want to use as the Hall of Infamy (HoI).