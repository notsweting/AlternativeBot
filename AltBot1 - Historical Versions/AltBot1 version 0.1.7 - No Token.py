import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
import random
from itertools import cycle
import time
 
bot = commands.Bot(command_prefix = ["/", ])
bot.remove_command('help')
case_insensitive = True
bot_version = 'Version 0.1.7 [BETA]'
bot_invite = 'https://discord.gg/33utPs9'
developer = '@ThisIsanAlt#0117'
embed_footer = f'| Developed by {developer} | {bot_invite} | {bot_version}'
NotEnoughPermissions = "Hmmm.... :thinking: You don't have permission to use this command!"
NotInGuild = 'You aren\'t in a guild at the moment. Try again in a guild.'
#b is rememberance day, a regular, c halloween
statuschoice = 'a'
regularstatus = cycle(['/help is the way to go!', 'Use /about to learn more!', bot_version, bot_invite])
statusremember = cycle(['Lest we forget', 'Lest we forget', 'Lest we forget', bot_version, bot_invite])
statushalloween = cycle(['/help is the way to go!', 'Use /about to learn more!', 'Happy Halloween!', 'Happy Halloween!', 'Happy Halloween!', bot_version, bot_invite])
dev= cycle(['UNDER TESTING. UNSTABLE.', 'UNSTABLE.', bot_version])
if statuschoice == 'a':
 status = regularstatus
elif statuschoice == 'b':
 status = statusremember
elif statuschoice == 'd':
 status = dev
else:
 status = statushalloween

@bot.event
async def on_message(message):
  if len(message.mentions)>2:
    await message.channel.purge(limit=1)
    await message.channel.send(f'{message.author.mention}, Don\'t mass ping!')
  else:
    await bot.process_commands(message)

#when the bot is ready
@bot.event
async def on_ready():
   change_status.start()
   print('We have logged in as {0.user}'.format(bot))

#change the playing status
@tasks.loop(seconds=10)
async def change_status ():
       await bot.change_presence(activity=discord.Game(next(status)))
 
#error handler
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    pass
  elif isinstance(error, commands.MissingPermissions):
    await ctx.send ('You don\'t have permmission to do that!')
  else:
    print (error)
    embed = discord.Embed(title="Oh noes!", description="There's been an issue!", colour=ctx.author.color)
    embed.add_field(name='The following exception was raised:', value=f' ```{error}``` The issue has been sent to {developer}!')
    await ctx.send (embed=embed)
 
 
#show rules
@bot.command()
async def rules(ctx):
 embed = discord.Embed(title="AltBot1/AltSquad Server Rules", description="Follow these rules to stay in the server!", colour=ctx.author.color)
 embed.add_field(name='It\'s simple.', value='''Just use common sense. Swearing is allowed, but only to a certain extent. No NSFL/NSFW content or advertising. ''')
 await ctx.send (embed=embed)
 
#help command
@bot.command()
async def help(ctx):
   embed = discord.Embed(title="AltBot1 Help and Documentation", description="Basic commands.\nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
   embed.add_field(name='/about', value='Get information about the bot!')
   embed.add_field(name="/ping", value="Check the ping of the bot to the Discord Server.")
   embed.add_field(name="/8ball [question]", value="Ask the magic 8ball a question!")
   embed.add_field(name='/whois (person)', value='Get info on a member in the server.')
   embed.add_field(name='/slap (person)', value='Slap someone.')
   embed.add_field(name='/hug (person)', value='Hug someone.')
   embed.add_field(name='/fight (person)', value='Fight someone.')
   embed.add_field(name= '/membercount', value='Get the amount of members in the server.')
   embed.set_footer(text=f'Requested by {ctx.author} ' + embed_footer, icon_url=ctx.author.avatar_url)
   if ctx.guild != None:
    await ctx.send (f'{ctx.author.mention}, I have sent you the documentation!')
   await ctx.author.send (embed=embed, delete_after=60) 

 
#ping command
@bot.command()
async def ping(ctx):
   await ctx.send(f":ping_pong: Pong! {round(bot.latency * 1000)}ms")
 
      
#about command
@bot.command()
async def about (ctx):
   embed = discord.Embed(title="About the bot", colour=ctx.author.color)
   embed.add_field(name='Developer', value="ThisIsanAlt#0117")
   embed.add_field(name='Server invite', value=f'{bot_invite}')
   embed.add_field(name='Programming Language and library', value="discord.py version 1.3.0")
 
   await ctx.send (embed=embed)
 
@bot.command()
async def dev_update(ctx):
 await ctx.channel.purge(limit = 1)
 await ctx.send(f''' > ***AltBot1 Version {bot_version}***
> 
> **New stuff:**
> - doing /whois with the wrong member will no longer send that cryptic message
> 
> **In progress:**
> - Bad word detection (Will eventually be used to prevent spam pings, etc.)
> - Mod help command
''')

#whois command
@bot.command()
async def whois(ctx, member: discord.Member = None):
 member = ctx.author if not member else member
 roles = [role for role in member.roles]
 embed = discord.Embed (color=member.color, timestamp=ctx.message.created_at)
 embed.set_author(name=f'User info on {member}')
 embed.set_thumbnail(url=member.avatar_url)
 embed.set_footer(text=f'Requested by {ctx.author} ' + embed_footer, icon_url=ctx.author.avatar_url)
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
    #User.avatar
    #User.avatar_url
    #User.avatar_url_as
    #User.block
    #User.bot
    #User.color
    #User.colour
 bot_status = 'Yes' if member.bot == True else 'No'
 embed.add_field(name='Am I a bot:', value=bot_status)
 #Member.status
 #WidgetMember.status
 #Member.web_status
 #Member.mobile_status
 #Member.desktop_status
 embed.add_field(name='Status:', value=member.status)
 if ctx.guild != None:
   await ctx.send(embed=embed)
 else:
   await ctx.send(NotInGuild)

@bot.command()
async def invite(ctx):
 await ctx.send ('The goods are on their way.')
 await asyncio.sleep(3)
 await ctx.send (bot_invite)

#unused = discord.utils.find(lambda role: not role.members, guild.roles)

# for attributes, it's easier with
#admin = discord.utils.get(guild.roles, name="admin")

# AND
#channel = discord.utils.get(guild.text_channels, name="help", topic="help channel")

# when was the message created?
#created_at = discord.utils.snowflake_time(discord_id) # works for almost all IDs

# Invite Me!
#invite = discord.utils.oauth_url(bot.user.id, guild.me.guild_permissions)

# Escape markdowns...
#safe = discord.utils.escape_markdown("**Bold text** and ||spoiler||")

# Don't Mention It!
#safe_everyone = discord.utils.escape_mentions(guild.me.mention)

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
@bot.command()
async def purge(ctx, amount=5):
  embed = discord.Embed (title='**A purge has been run!**', color=ctx.author.color, timestamp=ctx.message.created_at)
  embed.set_footer(text=f'AltBot1 {bot_version}')
  embed.add_field(name='Purged messages:', value=amount)
  embed.add_field(name='Purged by:', value=ctx.author.mention)
  await ctx.channel.purge(limit=amount+1)
  await ctx.send(embed=embed)
 
@bot.command()
async def kick(ctx, member : discord.Member, *, reason='no reason'):
  embed = discord.Embed (title='You\'ve been kicked!', color=member.color, timestamp=ctx.message.created_at)
  embed.set_footer(text=f'AltBot1 {bot_version}')
  embed.add_field(name='You were kicked by:', value=ctx.author.mention)
  embed.add_field(name='Reason:', value=reason)
  if ctx.author.id not in mod_ids:
    await ctx.send(NotEnoughPermissions)   
  else:
    await member.send(embed=embed)
    await ctx.guild.kick(member, reason=reason,)  
    await ctx.send(f'Succesfully kicked {member.mention} for {reason}') 
    
@bot.command() 
async def membercount(ctx):
    await ctx.send(f'{ctx.guild.name} currently has {ctx.guild.member_count} members!')
    
#8ball command
@bot.command(aliases=["8ball"])
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
@bot.command()
async def slap(ctx, member):
 reasons = ['for being rude.',
 'because why not.',
 'for being incompetent.',
 'for sleeping in class.',
 f'but {member} slapped him back!']
 await ctx.send (f'{ctx.author.mention} slapped {member} {random.choice(reasons)}')
 
@bot.command()
async def hug(ctx, member):
 reasons = ['for being nice.',
 f'because {ctx.author.mention} recieved a nice note from {member}.',
 'becuase why not?']
 await ctx.send (f'{ctx.author.mention} hugged {member} {random.choice(reasons)}')
 
@bot.command()
async def fight(ctx, member):
 reasons = [f'because {member} was mean.',
 f"{member} stole {ctx.author.mention}'s phone.",
 f'because {ctx.author.mention} was fricked in the head.',]
 await ctx.send (f'{ctx.author.mention} fought {member} {random.choice(reasons)}')
 
#coinflip command
@bot.command()
async def coinflip (ctx):
   responses = [":large_blue_diamond: Heads",
                ":large_orange_diamond: Tails"]
   await ctx.send('Flipping.....')
   await asyncio.sleep(3)
   await ctx.channel.purge(limit=1)
   await ctx.send(f"{random.choice(responses)}")

#warn command
@bot.command()
async def warn(ctx, member: discord.Member, warnlevel, *, reason = 'no reason'):
 if ctx.guild is None:
  await ctx.send(NotInGuild)

 elif ctx.author.id in mod_ids:
  warn1 = discord.utils.get(ctx.guild.roles, name="1")
  warn2 = discord.utils.get(ctx.guild.roles, name="2")
  success = f'Success! \n {member.mention} has been warned by {ctx.author.mention} for {reason}! ({warnlevel}/3)'
  if warnlevel == '1':
    await member.add_roles(warn1, reason=reason)
    await ctx.send(success)
  elif warnlevel == '2':
    await member.add_roles(warn2, reason=reason)
    await ctx.send(success)
  elif warnlevel == '3':
    await ctx.kick(member, reason='3 Warns')
    await member.send()
  elif warnlevel > 3:
    await ctx.send ('Error: There are only 3 warn levels. Please enter a number from 1 to 3.')
 else: 
  await ctx.send (NotEnoughPermissions)
 
bot.run(token)