import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import time
 
client = commands.Bot(command_prefix = ["/", ])
client.remove_command('help')
case_insensitive = True
bot_version = 'Version 0.1.6.2 [BETA]'
bot_invite = 'https://discord.gg/33utPs9'
developer = '@ThisIsanAlt#0117'
#b is rememberance day, a regular, c halloween
statuschoice = 'a'
regularstatus = cycle(['/help is the way to go!', 'Use /about to learn more!', 'Use /info to learn more!', bot_version, bot_invite])
statusremember = cycle(['Lest we forget', 'Lest we forget', 'Lest we forget', bot_version, bot_invite])
statushalloween = cycle(['/help is the way to go!', 'Use /about to learn more!', 'Use /info to learn more!', 'Happy Halloween!', 'Happy Halloween!', 'Happy Halloween!', bot_version, bot_invite])
dev= cycle(['CURRENTLY UNDER TESTING. UNSTABLE.', bot_version])
if statuschoice == 'a':
 status = regularstatus
elif statuschoice == 'b':
 status = statusremember
elif statuschoice == 'd':
 status = dev
else:
 status = statushalloween
 
#when the bot is ready
@client.event
async def on_ready():
   change_status.start()
   print('We have logged in as {0.user}'.format(client))
 
#change the playing status
@tasks.loop(seconds=10)
async def change_status ():
       await client.change_presence(activity=discord.Game(next(status)))
 
#error handler
@client.event
async def on_command_error(ctx, error):
   if isinstance(error, commands.CommandNotFound):
     await ctx.send('This command is nonexistent. Please use a proper command as documented in /help.')
   else:
     print (error)
     embed = discord.Embed(title="Oh noes!", description="There's been an issue!", colour=ctx.author.color)
     embed.add_field(name='The following exception was raised:', value=f' ```{error}``` The issue has been sent to {developer}!')
     await ctx.send (embed=embed)
 
 
#show rules
@client.command()
async def rules(ctx):
 embed = discord.Embed(title="AltBot1/AltSquad Server Rules", description="Follow these rules to stay in the server!", colour=ctx.author.color)
 embed.add_field(name='It\'s simple.', value='''Just use common sense. Swearing is allowed, but only to a certain extent. No NSFL/NSFW content or advertising. ''')
 await ctx.send (embed=embed)
 
@client.event
async def on_message(message):
 pass
 
@client.command()
async def alert(ctx, link):
 ctx.channel.purge(limit=1)
 ctx.send(f'''
 Hey @everyone, ThisIsanAlt posted a new video!
 Watch it now at {link}!
 ''')
 
#help command
@client.command()
async def help(ctx):
   embed = discord.Embed(title="AltBot1 Help and Documentation", description="Basic commands", colour=ctx.author.color)
   embed.add_field(name='/about', value='Get information about the bot!')
   embed.add_field(name="/ping", value="Check the ping of the bot to the Discord Server.")
   embed.add_field(name="/8ball", value="Ask the magic 8ball a question!")
   embed.add_field(name='/whois (person)', value='Get info on a member in the server.')
   embed.add_field(name='/slap (person)', value='Slap someone.')
   embed.add_field(name='/hug (person)', value='Hug someone.')
   embed.add_field(name='/fight (person)', value='Fight someone.')
   embed.set_footer(text= f'Requested by {ctx.author} | (required) [optional] | Developed by {developer} | Contact him for more info! | {bot_invite} | {bot_version}', icon_url=ctx.author.avatar_url)
   await ctx.send (embed=embed)
 
#ping command
@client.command()
async def ping(ctx):
   await ctx.send(f":ping_pong: Pong! {round(client.latency * 1000)}ms")
 
      
#about command
@client.command()
async def about (ctx):
   embed = discord.Embed(title="About the bot", colour=ctx.author.color)
   embed.add_field(name='Developer', value="ThisIsanAlt#0117")
   embed.add_field(name='Server invite', value="https://discord.gg/TauHxQ")
   embed.add_field(name='Programming Language and library', value="discord.py version 1.3.0")
 
   await ctx.send (embed=embed)
 
@client.command()
async def dev_update(ctx):
 await ctx.channel.purge(limit = 1)
 await ctx.send(f''' > ***AltBot1 Version {bot_version}***
>
> **New stuff:**
> - Fixed up /help
> - Added YouTube notifications
> - Fixed an issue that would return errors on every message in version and 1.6 1.6.1
>
> **In progress:**
> - Bad word detection (Will eventually be used to prevent spam pings, etc.)
>
> **Notes:**
> - Versions 1.6 and 1.6.1 were never released as a bug prevented the dev update message from being sent
''')
#whois command
@client.command()
async def whois(ctx, member: discord.Member = None):
 member = ctx.author if not member else member
 roles = [role for role in member.roles]
 embed = discord.Embed (color=member.color, timestamp=ctx.message.created_at)
 embed.set_author(name=f'User info on {member}')
 embed.set_thumbnail(url=member.avatar_url)
 embed.set_footer(text= f'Requested by {ctx.author.mention} | Developed by {developer} | Contact him for more info! | {bot_invite} | {bot_version}', icon_url=ctx.author.avatar_url)

 embed.add_field(name='Discord ID:', value=member.id)
 value1 = 'None' if member.display_name == member.name else member.display_name
 embed.add_field(name='Nickname:', value=value1)

 embed.add_field(name='Created at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
 embed.add_field(name='Joined at:', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

 embed.add_field(
     name=f'Roles: ({len(roles)})',
     value=" ".join(role.mention for role in roles),
 )
 embed.add_field(name='Top Role:', value=member.top_role.mention)
 bot_status = 'Yes' if member.bot == True else 'No'
 embed.add_field(name='Am I a bot:', value=bot_status)


 await ctx.send(embed=embed)
 
@client.command()
async def invite(ctx):
 await ctx.send ('The goods are on their way.')
 await ctx.purge(limit=1)
 await ctx.send (bot_invite)
 
mod_ids=[447119084627427351,
       318068014899527691,
       511561638785056771,
       382634433771208725,
       513798090071736320,
       448280112207626241,
       315249559473225729,
       552235268342677529,
       486186037702426625,
       510397521554833409,
       534851751531249674,
       473835913907142656]
 
#clear command
@client.command()
async def purge(ctx, amount=5):
 
   if ctx.author.id not in mod_ids:
       await ctx.send("Hmmm.... :thinking: You don't have permission to use this command!")   
   else:
       await ctx.channel.purge(limit=amount+1)
       await ctx.send('Messages cleared.')
 
@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
 if ctx.author.id not in mod_ids:
  await ctx.send("Hmmm.... :thinking: You don't have permission to use this command!")
 else:
  if reason is None:
   reason = f'{ctx.author.mention}'
  else:
   reason = reason + f' {ctx.author.mention}'

  await kick(member, reason=reason,)
 
#8ball command
@client.command(aliases=["8ball"])
async def _8ball (ctx, *, question):
   responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again later.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Dont count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
   await ctx.send(f"{random.choice(responses)}")
 
#slap command
@client.command()
async def slap(ctx, member):
 reasons = ['for being rude.',
 'because why not.',
 'for being incompetent.',
 'for sleeping in class.',
 f'but {member} slapped him back!']
 await ctx.send (f'{ctx.author.mention} slapped {member} {random.choice(reasons)}')
 
@client.command()
async def hug(ctx, member):
 reasons = ['for being nice.',
 f'because {ctx.author.mention} recieved a nice note from {member}.',
 'becuase why not?']
 await ctx.send (f'{ctx.author.mention} hugged {member} {random.choice(reasons)}')
 
@client.command()
async def fight(ctx, member):
 reasons = [f'because {member} was mean.',
 f"{member} stole {ctx.author.mention}'s phone.",
 f'because {ctx.author.mention} was fricked in the head.',]
 await ctx.send (f'{ctx.author.mention} fought {member} {random.choice(reasons)}')
 
#coinflip command
@client.command()
async def coinflip (ctx):
   responses = [":large_blue_diamond: Heads",
                ":large_orange_diamond: Tails"]
   await ctx.send('Flipping.....')
   time.sleep(3)
   await ctx.channel.purge(limit=1)
   await ctx.send(f"{random.choice(responses)}")
 
#warn command
#@client.command()
#async def warn (ctx, member: discord.Member, warnlevel):
 #if warnlevel == '1':
 # member.add_roles()
 #elif warnlevel == '2':
  # member.add_roles()
 #elif warn_level == '3':
  # member.add_roles()
 #elif warn_level > 3:
   #await ctx.send ('Error: There are only 3 warn levels. Please enter a number from 1 to 3.')
 
client.run(token)

