import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
import random
from itertools import cycle
import time
import pickle
import json
 
bot = commands.Bot(command_prefix = ["/", '@'], case_insensitive=True)
bot.remove_command('help')
bot_version = 'Version 0.1.9 [BETA]'
bot_invite = 'https://discord.gg/33utPs9'
developer = '@ThisIsanAlt#0117'
embed_footer = f'| Developed by {developer} | {bot_invite} | {bot_version}'
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
async def on_command_error(ctx, error):
  error = getattr(error, "original", error)
  if isinstance(error, commands.CommandNotFound):
    pass
  elif isinstance(error, commands.MissingPermissions):
    await ctx.send ('You don\'t have permmission to do that!')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('You\'re missing an argument. Check the command and ensure that all arguments are present.')
  elif str(error).startswith('Member "'):
    MemberNotInGuild = discord.Embed (description=(':x: The member was not found.'), color=ctx.author.color)
    await ctx.send(embed=MemberNotInGuild)
  elif isinstance(error, commands.BadArgument):
    await ctx.send('One or more of your arguments didn\'t make sense. Make sure your arguments are valid, then try again.')
  elif isinstance(error, discord.Forbidden):
    await ctx.send('I don\'t have permission to do that! Make sure I have the correct permissions, then try again.')
  else:
    print (error)
    await ctx.send (f'Hm. Didn\'t work. Check the command and make sure all conditions are met. **Error:** *{error}*')

@bot.event
async def on_message(message):
  if len(message.mentions)>2:
    await message.delete()
    await message.channel.send(f'{message.author.mention}, Don\'t mass ping!')
  else:
    await bot.process_commands(message)

#when the bot is ready
@bot.event
async def on_ready():
   change_status.start()
   print(f'We have logged in as {bot.user}')

#change the playing status
@tasks.loop(seconds=10)
async def change_status():
       await bot.change_presence(activity=discord.Game(next(status)))
 
@bot.command()
async def tonedetector(ctx, *, paragraph):
  await ctx.send('**This command is in progress. Report bugs with this command with `/reportbug`.**')
  await ctx.send('Please enter your sentence to begin tone detection.')
  
  def check(message : discord.Message) -> bool:
      return message.author == ctx.author
  try:
     notlist = await bot.wait_for('message', timeout = 60, check=check)
  except asyncio.TimeoutError: 
      await ctx.send("You took too long to respond!")            
  else:     
    if notlist=='stats':
      await ctx.send('Loading stats:')
      await asyncio.sleep(2)
      with open('tonedetectionrating.txt', 'rb') as input_file:
        ratings=pickle.load(input_file)
        await ctx.send(f'Average rating:\n{ratings}')
    else:
      spacelist=[]
      commalist=[]
      periodlist=[]
      firstquote=[]
      secondquote=[]
      doublequote=[]
      doublequote2=[]
      done=[]
      spacelist=notlist.split(' ')
      for i in spacelist:
        if i.endswith(','):
          i = i[:-1]
          commalist.append(i)
        else:
          commalist.append(i)
      for i in commalist:
        if i.endswith('.'):
          i = i[:-1]
          periodlist.append(i)
        else:
          periodlist.append(i)
      for i in periodlist:
        x=i.strip()
        y=x.lower()
        if i.startswith('\''):
          i = i[1:]
          secondquote.append(i)
        else: 
          secondquote.append(i)
      for i in firstquote:
        if i.endswith('\''):
          i = i[:-1]
          doublequote.append(i)
        else:
          doublequote.append(i)
      for i in secondquote:
        if i.startswith('"'):
          i=i[1:]
          doublequote2.append(i)
        else:
          doublequote2.append(i)
      for i in doublequote:
        if i.endswith('"'):
          i=i[:-1]
          doublequote2.append(i)
        else:
          doublequote2.append(i)
      for i in doublequote2:
        i=i.strip()
        i=i.lower()
        if i.startswith('"'):
          i = i[1:]
          done.append(i)
        else:
          done.append(i)
        
      await ctx.send('The information has been indexed!')
      await asyncio.sleep(2)
      await ctx.send('Commencing processing...')
      happy=['happy',]
      angry=['hate']
      passionate=['love',]
      happy_count=0
      angry_count=0
      passionate_count=0
      for i in done:
        if i in happy:
          happy_count=happy_count+1
        if i in angry:
          angry_count=angry_count+1
        if i in passionate:
          passionate_count=passionate_count+1
      await ctx.send('Processing done!')
      await ctx.send(f'Your counts:\nHappy: {happy_count}\nAngry: {angry_count}\nPassionate: {passionate_count}')      
      await ctx.send('Please input your rating, on a scale of 1 to 10.')
      def check1(message : discord.Message) -> bool:
          return message.author == ctx.author
      try:
          ratings1 = await bot.wait_for('message', timeout = 60, check=check1)
      except asyncio.TimeoutError: 
          await ctx.send("You took too long to respond!")            
      else:     
        with open('tonedetectionrating.txt', 'rb') as input_file:
          ratings2=pickle.load(input_file)
        ratings=(ratings1+ratings2)/2
        with open('tonedetectionrating.txt', 'wb') as out_file:
          pickle.dump(ratings, out_file)

#help command
@bot.command(ignore_extra=True)
async def help(ctx, info=None):
  if ctx.prefix == '/':
    if info == None:
      embed = discord.Embed(title="AltBot1 Help and Documentation", description="Categories. Do /help [category] to get more info.\
      \nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
      embed.add_field(name='Fun', value='Some fun commands for you to use!')
      embed.add_field(name='Meta', value='Bot-related and user-related commands. Includes /whois, /about, and /bugreport.')
      embed.add_field(name='Cleverbot', value='I\'m a very clever bot! Use these commands to bring me to my full capabilities!')
      embed.add_field(name='Moderation', value='These commands empower the moderation team. Rest assured, I won\'t do what the user can\'t.')
      embed.set_footer(text=f'(optional) [required] | Requested by {ctx.author} {embed_footer}', icon_url=ctx.author.avatar_url)
      await ctx.send (embed=embed, delete_after=60)
    elif info.lower()=='fun':
      embed = discord.Embed(title="AltBot1 Help and Documentation", description="Here are some fun commands for you to use!\
      \nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
      embed.add_field(name="/8ball (question)", value="Ask the magic 8ball a question!")
      embed.add_field(name='/slap [person]', value='Slap someone.')
      embed.add_field(name='/hug [person]', value='Hug someone.')
      embed.add_field(name='/fight [person]', value='Fight someone.')
      embed.add_field(name='/rockpaperscissors [person] **BETA**', value='Challenge someone to a rock paper scissors challenge! \
      (Must have DMs open) **WARNING: Command is in beta and may not work as intended. Use /bugreport to report bugs.**')
      embed.set_footer(text=f'(optional) [required] | Requested by {ctx.author} {embed_footer}', icon_url=ctx.author.avatar_url)
      await ctx.send (embed=embed, delete_after=60)
    elif info.lower()=='meta':
      embed = discord.Embed(title="AltBot1 Help and Documentation", description="Meta commands. Concerns more of the geeky side of the userbase.\
      \nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
      embed.add_field(name='/about', value='Get information about the bot!')
      embed.add_field(name="/ping", value="Check the ping of the bot to the Discord API.")    
      embed.add_field(name='/whois (person)', value='Get info on a member in the server.')
      embed.add_field(name= '/membercount', value='Get the amount of members in the server.')
      embed.add_field(name='/bugreport (description)', value='Report a bug!')    
      embed.add_field(name='~~/suggest (suggestion)~~', value='**Command is currently unavailable. **~~Suggest something for the bot!~~')
      embed.set_footer(text=f'(optional) [required] | Requested by {ctx.author} {embed_footer}', icon_url=ctx.author.avatar_url)
      await ctx.send (embed=embed, delete_after=60)
    elif info.lower()=='cleverbot':
      embed = discord.Embed(title="AltBot1 Help and Documentation", description="Meta commands. Concerns more of the geeky side of the userbase.\
      \nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
      embed.add_field(name='/tonedetector **BETA**', value='Detects the tone of your writing. \
**WARNING: Command is in beta and may not work as intended. Use /bugreport to report bugs.**')
      embed.set_footer(text=f'(optional) [required] | Requested by {ctx.author} {embed_footer}', icon_url=ctx.author.avatar_url)
      await ctx.send (embed=embed, delete_after=60) 
    elif info.lower()=='mod' or info.lower()=='moderation':
      embed = discord.Embed(title="AltBot1 Help and Documentation", description="Moderation commands.\nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
      embed.add_field(name='/purge (no. of messages)', value='Purge messages. Number of messages defaults to 5. Requires manage messages permission.')
      embed.add_field(name="/kick [member] (reason)", value="Kick a member. Reason defaults to no reason. Requires kick members permission.")
      embed.add_field(name="/ban [member/user id] (reason)", value="Permanently ban a member. Reason defaults to no reason. Requires ban members permission.")
      embed.set_footer(text=f'(optional) [required] | Requested by {ctx.author} {embed_footer}', icon_url=ctx.author.avatar_url)
      await ctx.send (embed=embed, delete_after=60)
  else:
    await ctx.send('That\'s not a valid field!')

#ping command
@bot.command()
async def ping(ctx):
   await ctx.send(f":ping_pong: Pong! {round(bot.latency * 1000)}ms")

#suggest
@bot.command()
async def suggest(ctx, *, field=None):
  if field == None:
    await ctx.send('This command is temporarily disabled. Suggestions made may not be processed correctly.')
    await ctx.send('What would you like to suggest?')
    def check(message : discord.Message) -> bool:
      return message.author == ctx.author and message.channel==ctx.channel

    try:
      field = await bot.wait_for('message', timeout = 29, check = check)
    except asyncio.TimeoutError: 
      await ctx.send(f"You took too long to respond!")            
    else:
      pass

       
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
> - 
> 
> **In progress:**
> - yay nothing. please suggest things in #suggestions
''')

#whois command
@bot.command()
async def whois(ctx, *, member: discord.Member = None):
  member = ctx.author if not member else member
  if ctx.guild != None:
    roles = [role for role in member.roles]
    embed = discord.Embed (color=member.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f'User info on {member}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author} ' + embed_footer, icon_url=ctx.author.avatar_url)
    embed.add_field(name='Discord ID:', value=member.id)
    if member.display_name == member.name:
      value1 = 'None'
    else:
      value1 = member.display_name
    embed.add_field(name='Nickname:', value=value1)
    embed.add_field(name='Created at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
    embed.add_field(name='Joined at:', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
    embed.add_field(name=f'Roles: ({len(roles)})', value=" ".join([role.mention for role in roles]))
    embed.add_field(name='Top Role:', value=member.top_role.mention)

    if member.bot:
      bot_status = 'Yes'
    else:
      bot_status = 'No'
    embed.add_field(name='Am I a bot:', value=bot_status)

    if member.premium_since != None:
      embed.add_field(name='Boosting since:', value=member.premium_since.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

    embed.add_field(name='Status:', value=member.status)
    await ctx.send(embed=embed)
  else:
    await ctx.send(NotInGuild) 
       
@bot.command()
async def invite(ctx):
 await ctx.send ('The goods are on their way.', delete_after=3)
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
 
#clear command
@commands.has_permissions(manage_messages=True)
@bot.command()
async def purge(ctx, amount : int=5, member : discord.Member=None):
  embed = discord.Embed (title='**A purge has been run!**', color=ctx.author.color, timestamp=ctx.message.created_at)
  embed.set_footer(text=f'AltBot1 {bot_version}')
  embed.add_field(name='Purged messages:', value=amount)
  embed.add_field(name='Purged by:', value=ctx.author.mention)
  await ctx.channel.purge(limit=amount+1)
  await ctx.send(embed=embed)

@bot.command()
async def acceptbug(ctx, userid, bug_number, *, description):
  if ctx.author.id == 447119084627427351:
    userid1 = int(userid)
    user=bot.get_user(userid1)
    await user.send(f'Your bug report {bug_number} has been approved!')
    channel=bot.get_channel(702605147402010654)
    embed=discord.Embed(title='AltBot1 Bug Report', color=ctx.author.color, timestamp=ctx.message.created_at)
    embed.set_footer(text=f'AltBot1 {bot_version}')
    embed.add_field(name='Description:', value=description)
    embed.add_field(name='Bug ID:', value=bug_number)
    await channel.send(embed=embed)
  

@bot.command()
async def declinebug(ctx, userid, bug_number):
  if ctx.author.id == 447119084627427351:
    userid1 = int(userid)
    user=bot.get_user(userid1)
    await user.send(f'Your bug report {bug_number} has been declined.')

@bot.command()
async def bugreport(ctx, *, description=None,):
  bug_number = random.randint(0, 100)
  if description != None:
    user = bot.get_user(447119084627427351)
    await ctx.send(f'''Your bug has been reported!''')
    embed=discord.Embed(title='AltBot1 Bug Report', color=ctx.author.color, timestamp=ctx.message.created_at)
    embed.set_footer(text=f'AltBot1 {bot_version}')
    embed.add_field(name='Description:', value=description)
    embed.add_field(name='Reported By', value=ctx.author.mention)
    embed.add_field(name='Bug ID:', value=bug_number)
    await ctx.send(embed=embed)
    await user.send(embed=embed)
  else:
    await ctx.send('**Bug report wizard**\n\nFollow the prompts and answer them!')
    await ctx.send('What\'s the description of the bug?')
    
    def check(message : discord.Message) -> bool:
        return message.author == ctx.author
    try:
        description = await bot.wait_for('message', timeout = 60, check=check)
    except asyncio.TimeoutError: 
        await ctx.send("You took too long to respond!")            
    else: 
      user = bot.get_user(447119084627427351)
      await ctx.send(f'''Your bug has been reported!''')
      embed=discord.Embed(title='AltBot1 bug report', color=ctx.author.color, timestamp=ctx.message.created_at)
      embed.set_footer(text=f'AltBot1 {bot_version}')
      embed.add_field(name='Description:', value=description.content)
      embed.add_field(name='Reported By', value=ctx.author.mention)
      embed.add_field(name='Bug ID:', value=bug_number)
      await ctx.send(embed=embed)
      await user.send(embed=embed)
    finally: 
        pass

@commands.has_permissions(kick_members=True)   
@bot.command()
async def kick(ctx, member : discord.Member, *, reason='no reason'):
  embed = discord.Embed (title='You\'ve been kicked!', color=member.color, timestamp=ctx.message.created_at)
  embed.set_footer(text=f'AltBot1 {bot_version}')
  embed.add_field(name='You were kicked by:', value=ctx.author.mention)
  embed.add_field(name='Reason:', value=reason)
  try:
    msg = await member.send(embed=embed)
  except discord.Forbidden:            
    await ctx.send('I couldn\'t DM the selected member with details about their kick.')
    try:
      await ctx.guild.kick(member, reason=reason)
    except discord.Forbidden:
      await ctx.send('I couldn\'t kick the selected member.')
    else:
      await ctx.send(f'Kicked {member.mention} for {reason}. They could not be messaged about their kick.')
  else:
    try:
      await ctx.guild.kick(member, reason=reason)
    except discord.Forbidden:
      await ctx.send('I couldn\'t kick the selected member.')
      await msg.delete()
    else:
      await ctx.send(f'Successfully kicked {member.mention} for {reason}. They have also been DMed about their kick.')

@commands.has_permissions(ban_members=True)   
@bot.command()
async def ban(ctx, member : discord.User, *, reason = None):
  embed = discord.Embed (title='You\'ve been permanently banned!', color=member.color, timestamp=ctx.message.created_at)
  embed.set_footer(text=f'AltBot1 {bot_version}')
  embed.add_field(name='You were banned by:', value=ctx.author.mention)
  embed.add_field(name='Reason:', value=reason)
  try:
    msg = await member.send(embed=embed)
  except discord.Forbidden:            
    await ctx.send('I couldn\'t DM the selected member with details about their ban.')
    try:
      await ctx.guild.ban(member, reason=reason)
    except discord.Forbidden:
      await ctx.send('I couldn\'t ban the selected member.')
    else:
      await ctx.send(f'Banned {member.mention} for {reason}. They could not be messaged about their ban.')
  else:
    try:
      await ctx.guild.ban(member, reason=reason)
    except discord.Forbidden:
      await ctx.send('I couldn\'t ban the selected member.')
      await msg.delete()
    else:
      await ctx.send(f'Successfully banned {member.mention} for {reason}. They have also been DMed about their ban.')

@commands.has_permissions(ban_members=True)   
@bot.command()
async def unban(ctx, member : discord.User, *, reason='No reason'):
  await ctx.guild.unban(member)
  try:
    embed = discord.Embed (title='You\'ve been unbanned!', color=member.color, timestamp=ctx.message.created_at)
    embed.set_footer(text=f'AltBot1 {bot_version}')
    embed.add_field(name='You were unbanned by:', value=ctx.author.mention)
    embed.add_field(name='Reason:', value=reason)
    await member.send(embed=embed)
  except discord.Forbidden:
    await ctx.send(f'{member.mention}, unbanned. I could not message them about their unban.')
  else:
    await ctx.send(f'{member.mention}, successfully unbanned.')
  
@bot.command() 
async def membercount(ctx):
    await ctx.send(f'{ctx.guild.name} currently has {ctx.guild.member_count} members!')
    
#8ball command
@bot.command(aliases=["8ball"])
async def _8ball (ctx, *, question = None):
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
  ' because why not.',
  ' for being incompetent.',
  ' for sleeping in class.',
  f', but {member} slapped him back!']
  await ctx.send (f'{ctx.author.mention} slapped {member}{random.choice(reasons)}')
 
@bot.command()
async def hug(ctx, member):
  reasons = ['for being nice.',
  f'because {ctx.author.mention} recieved a nice note from {member}.',
  'because why not?']
  await ctx.send (f'{ctx.author.mention} hugged {member} {random.choice(reasons)}')

@bot.command()
async def fight(ctx, member):
  reasons = [f'because {member} was mean.',
  f"because {member} stole {ctx.author.mention}'s phone.",
  f'for being fricked in the head.',]
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
@commands.has_permissions(manage_roles=True)
@bot.command()
async def warn (ctx, member: discord.Member, warnlevel, *, reason = 'no reason'):
  if ctx.guild != None:  
    warn1 = discord.utils.get(ctx.guild.roles, name=warnlevel)
    await member.add_roles(warn1, reason=reason)
  else:
    await ctx.send(NotInGuild)

@bot.command()
async def leave(ctx):
  if ctx.guild!= None:
    confirmation_no = str(random.randint(1000, 9999))
    await ctx.send(f"Are you sure you want to leave? Send `{confirmation_no}` to confirm. You have 60 seconds.")

    def check(message : discord.Message) -> bool:
        return message.author == ctx.author and message.content == confirmation_no

    try:
        message = await bot.wait_for('message', timeout = 60, check = check)
    except asyncio.TimeoutError: 
        await ctx.send("You took too long to respond!")            
    else:
      await ctx.author.send(f'I\'m sorry you had to leave! We hope you had a great time at {ctx.guild.name}')
      try:
        await ctx.guild.kick(ctx.author, reason='User used /leave')
      except commands.CommandInvokeError:
        await ctx.send('There\'s an issue with my permissions. Make sure I have the right permissions, then try again.')
      else:
        pass
    finally: 
        pass
  else:
    await ctx.send(NotInGuild)
  
@bot.command()
async def rockpaperscissors(ctx, member: discord.Member):
  await ctx.send('**This command is under construction and will be part of version 0.1.9. Report bugs with /reportbug.**')
  await ctx.send(f'{ctx.author.mention} has challenged {member.mention} to a rock paper scissors contest!')
  await ctx.send(f'To accept the challenge, {member.mention}, send `accept` to accept!')
  responses = ['rock', 'paper', 'scissors']
  def check(message : discord.Message) -> bool:
    return message.author == member and message.content == 'accept'

  def check1(message : discord.Message) -> bool:
      return message.author == member and message.content in responses
  
  def check2(message : discord.Message) -> bool:
      return message.author == ctx.author and message.content in responses
  try:
    message = await bot.wait_for('message', timeout = 60, check = check)
  except asyncio.TimeoutError: 
    await ctx.send(f"{member.mention} took too long to respond!")            
  else:
    await ctx.author.send(f'{member} accepted your challenge! Please use any of the following: `rock` `paper` `scissors` to select your choice!')
    await member.send(f'You accepted {ctx.author}\'s challenge! Please use any of the following: `rock` `paper` `scissors` to select your choice!')
  
  try:
    memberresponse = await bot.wait_for('message', timeout = 29, check = check2)
  except asyncio.TimeoutError: 
    await member.send(f"{ctx.author.name} took too long to respond!")            
  else:

    try:
      authorresponse = await bot.wait_for('message', timeout = 29, check = check2)
    except asyncio.TimeoutError: 
      await member.send(f"{ctx.author.name} took too long to respond!")            
    else:   
      
      if authorresponse == 'rock' and memberresponse == 'scissors':
        await ctx.author.send(f'You won! {member.name} chose scissors')
        await member.send(f'You lost. {ctx.author.name} chose rock.')
      elif authorresponse == 'scissors' and memberresponse == 'paper':
        await ctx.author.send(f'You won! {member.name} chose {memberresponse}')
        await member.send(f'You lost. {ctx.author.name} chose {authorresponse}.')
      elif authorresponse == 'paper' and memberresponse == 'rock':
        await ctx.author.send(f'You won! {member.name} chose {memberresponse}')
        await member.send(f'You lost. {ctx.author.name} chose {authorresponse}.')
      elif authorresponse == memberresponse:
        await ctx.author.send(f'You tied! {member.name} chose {memberresponse}')
        await member.send(f'You tied! {ctx.author.name} chose {authorresponse}')
      elif memberresponse == 'rock' and authorresponse == 'scissors':
        await member.send(f'You won! {ctx.author.name} chose {authorresponse}')
        await ctx.author.send(f'You lost. {member.name} chose {memberresponse}.')
      elif memberresponse == 'paper' and authorresponse == 'rock':
        await member.send(f'You won! {ctx.author.name} chose {authorresponse}')
        await ctx.author.send(f'You lost. {member.name} chose {memberresponse}.')
      elif memberresponse == 'scissors' and authorresponse == 'paper':
        await member.send(f'You won! {ctx.author.name} chose {authorresponse}')
        await ctx.author.send(f'You lost. {member.name} chose {memberresponse}.')
      else:
        pass
    
  finally: 
    pass

bot.run(token)
