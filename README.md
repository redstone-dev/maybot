# maybot
- a bot for my private server with friends that i'm open-sourcing because yes
- made with discord.py
- default prefix is `:`
- use `:help` to get a command list. the output should look something like this:
```
bot for the gay nerds server

literally may from pokemon

she has that name because her creator briefly considered may as a chosen name

​No Category:
  3          <- so that maybot replies with :3 when you send it too
  annihilate 
  help       Shows this message
  infamy     only works with non-slash commands    
  oocqc      
  rule       

Type :help command for more info on a command.
You can also type :help category for more info on a category.
```

## configuring rules
make a file with the path `bot-config/rules.txt` and just put your rules in line by line like this:
```
rule 1
rule 2
the third one
```
when you run `/rule x`, maybot will reply with the rule on that line number in `rules.txt`
