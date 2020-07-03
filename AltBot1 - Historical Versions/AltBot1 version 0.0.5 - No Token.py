import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import time
import os

client = commands.Bot(command_prefix = ["/"])
client.remove_command('help')

status_change = True

if status_change is True:
    status = cycle(['/help is the way to go!', 'Use /about to learn more!', 'Use /info to learn more!', 'Version 0.5 [ALPHA]',])
else:
    status = cycle(['UNDER DEVElOPMENT', 'UNDER DEVELOPMENT'])

#when the bot is ready
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    change_status.start()

#change the playing status
@tasks.loop(seconds=5)
async def change_status ():
        await client.change_presence(activity=discord.Game(next(status)))

#help command
@client.command()
async def help(ctx):
    embed = discord.Embed(title="AltBot1 Help and Documentation", description="Basic commands", colour=ctx.author.color)
    embed.add_field(name='/about(aka info)', value='Get information about the bot!')
    embed.add_field(name="/ping", value="Check the ping of the bot to the Discord Server.")
    embed.add_field(name="/8ball", value="Ask the magic 8ball a question!")
    embed.add_field(name='/whois {person}', value='Get info on a member in the guild.')
    embed.add_field(name='/slap {person} for {reason}', value='Slap a person!')
    embed.set_footer(text='{required} [optional] Developed by ThisIsanAltYT#0117 | Contact him for more info!')
    await ctx.send (embed=embed)

#ping command
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

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

#coinflip command
@client.command()
async def coinflip (ctx):
    responses = [":large_blue_diamond: Heads",
                 ":large_orange_diamond: Tails"]
    await ctx.send('Flipping.....')
    time.sleep(3)
    await ctx.channel.purge(limit=1)
    await ctx.send(f"{random.choice(responses)}")

#slap command
@client.command()
async def slap(ctx, member: discord.Member, *, reason,):
  await ctx.send (f'{ctx.author.mention} slapped {member.mention} {reason}')

#purge command
# outdated
@client.command()
async def purge(ctx, amount=5):
    if ctx.author.id not in mod_ids:
        await ctx.send('Hmmm.... :thinking: You don\'t have permission to use this command!')    
    else:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send('Messages cleared.')

#warn command
@client.command()
async def warn (ctx, member, warnlevel):
    
    if ctx.author.id not in mod_ids:
        await ctx.send ('Hey you! You don\'t have permissions to use this command!')

    else:
        numwarnlevel = int(warnlevel)
        if numwarnlevel == '1':
            await member.add_roles(510852414111219712)
        elif numwarnlevel == '2':
            await member.add_roles(504023257880592404)
        elif numwarnlevel == '3':
            await member.add_roles(510852486333202454)
        elif numwarnlevel > 3:
            await ctx.send ('Error: There are only 3 warn levels. Please enter a number from 1 to 3, otherwise manually add the role.')

#whois command
@client.command()
async def whois(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    roles = [role for role in member.roles]
    embed = discord.Embed (color=member.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f'User info on {member}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name='Discord ID:', value=member.id)
    embed.add_field(name='Nickname:', value=member.display_name)

    embed.add_field(name='Created at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
    embed.add_field(name='Joined at:', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

    embed.add_field(name=f'Roles: ({len(roles)})', value=" ".join([role.mention for role in roles]))
    embed.add_field(name='Top Role:', value=member.top_role.mention)
    
    if member.bot == True:
      bot_status = 'Yes'
    else:
      bot_status = 'No'
    embed.add_field(name='Am I a bot:', value=bot_status)

    await ctx.send(embed=embed)

#about command
@client.command(aliases = ['info'])
async def about (ctx):
    await ctx.send ('''Hey there, I\'m a bot created by ThisIsanAltYT#0117 for the server AltSquad!
If you see this bot on another server other than`discord.gg/SUzSuTa`, please contact ThisIsanAltYT#0117!''')


'''
Commands:
    Fun:
        ping, 8ball, coinflip, slap
    Mod:
        purge, warn
    Misc:
        whois

    AltBot1 has 207 lines of code
'''
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
        
client.run(token)
