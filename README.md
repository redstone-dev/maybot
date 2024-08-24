# maybot
- A bot for my private server with friends that I'm open-sourcing because yes.
- Made with discord.py.
- Most commands are slash commands or in the message right-click menu except for `.sync-tree`, which you should run after making changes to an application command.

## Installation
1. Clone the repo to a directory of your choosing
2. `chmod u+x setup.sh`
3. `./setup.sh` and follow the instructions at the link it echoes

> NOTE: `setup.sh` requires `wget` to be installed. Check if it is, then install it using your package manager.

## Configuring Rules
Create a file with the path `bot-config/rules.txt` and just put your rules in line by line like this:
```
rule 1
rule 2
the third one
```
When you run `/rule x`, maybot will reply with the rule on that line number in `rules.txt`.

## Custom Bot Description
In the same `bot-config` directory, you can add a `description.txt`. Whatever is in there will replace the default bot description when running `.help`.

## Other Config
See [this wiki article](https://github.com/redstone-dev/maybot/wiki/Initial-configuration-of-maybot) for information about configuring maybot.
