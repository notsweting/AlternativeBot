import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
import random
from itertools import cycle
import time
import pickle
import json

bot = commands.Bot(command_prefix = commands.when_mentioned_or('/', '@'), case_insensitive=True)
bot.remove_command('help')
bot_version = 'Version 0.1.11 [BETA]'
#b is rememberance day, a regular, c halloween
statuschoice = 'a'
regularstatus = cycle(['/help is the way to go!', 'Use /about to learn more!'])
statusremember = cycle(['Lest we forget', 'Lest we forget', 'Lest we forget'])
statushalloween = cycle(['/help is the way to go!', 'Use /about to learn more!', 'Happy Halloween!', 'Happy Halloween!', 'Happy Halloween!'])
dev = cycle(['UNDER TESTING. UNSTABLE.', 'UNSTABLE.', bot_version])
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
    elif isinstance(error, commands.BadArgument):
        await ctx.send('One or more of your arguments didn\'t make sense. Make sure your arguments are valid, then try again.')
    elif isinstance(error, discord.Forbidden):
        await ctx.send('I don\'t have permission to do that! Make sure I have the correct permissions, then try again.')
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(error)
    else:
        print(error)

@bot.event
async def on_message(message):
    if len(message.mentions)>4:
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
async def dev_update(ctx):
    await ctx.channel.purge(limit = 1)
    await ctx.send(f''' > ***AlternativeBot {bot_version}***
> 
> **New stuff:**
> - Restructured code. Internal update only.
> 
> **In progress:**
> - Channel and server-wide lock command
> - Mute command
''')

#help command
@commands.cooldown(1, 3, BucketType.user)
@bot.command(ignore_extra=True)
async def help(ctx, info=None):
    if info == None:
        embed = discord.Embed(title="AlternativeBot Help and Documentation", description="Categories. Do /help [category] to get more info.\
        \nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
        embed.add_field(name='Fun', value='Some fun commands for you to use!')
        embed.add_field(name='Meta', value='Bot-related and user-related commands. Includes /whois, /about, and /bugreport.')
        embed.add_field(name='Moderation', value='These commands empower the moderation team. Rest assured, I won\'t do what the user can\'t.')
        embed.set_footer(text=f'(optional) [required] | Requested by {ctx.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
        await ctx.send (embed=embed, delete_after=60)
    elif info.lower()=='fun':
        embed = discord.Embed(title="AlternativeBot Help and Documentation", description="Here are some fun commands for you to use!\
        \nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
        embed.add_field(name="/8ball (question)", value="Ask the magic 8ball a question!")
        embed.add_field(name='/slap [person]', value='Slap someone.')
        embed.add_field(name='/hug [person]', value='Hug someone.')
        embed.add_field(name='/fight [person]', value='Fight someone.')
        embed.add_field(name='/rockpaperscissors [person] **BETA**', value='Challenge someone to a rock paper scissors challenge! \
        (Must have DMs open) **WARNING: Command is in beta and may not work as intended. Use /bugreport to report bugs.**')
        embed.set_footer(text=f'(optional) [required] | Requested by {ctx.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
        await ctx.send (embed=embed, delete_after=60)
    elif info.lower()=='meta':
        embed = discord.Embed(title="AlternativeBot Help and Documentation", description="Meta commands. Concerns more of the geeky side of the userbase.\
        \nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
        embed.add_field(name='/about', value='Get information about the bot!')
        embed.add_field(name="/ping", value="Check the ping of the bot to the Discord API.")    
        embed.add_field(name='/whois (person)', value='Get info on a member in the server.')
        embed.add_field(name= '/membercount', value='Get the amount of members in the server.')
        embed.add_field(name='/bugreport (description)', value='Report a bug!')    
        embed.add_field(name='~~/suggest (suggestion)~~', value='**Command is currently unavailable. **~~Suggest something for the bot!~~')
        embed.set_footer(text=f'(optional) [required] | Requested by {ctx.author} | Support: https://discord.gg/33utPs9'', icon_url=ctx.author.avatar_url)
        await ctx.send (embed=embed, delete_after=60)
    elif info.lower()=='mod' or info.lower()=='moderation':
        embed = discord.Embed(title="AlternativeBot Help and Documentation", description="Moderation commands.\nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
        embed.add_field(name='/purge (no. of messages)', value='Purge messages. Number of messages defaults to 5. Requires manage messages permission.')
        embed.add_field(name="/kick [member] (reason)", value="Kick a member. Reason defaults to no reason. Requires kick members permission.")
        embed.add_field(name="/ban [member/user id] (reason)", value="Permanently ban a member. Reason defaults to no reason. Requires ban members permission.")
        embed.set_footer(text=f'(optional) [required] | Requested by {ctx.author} | Support: https://discord.gg/33utPs9'', icon_url=ctx.author.avatar_url)
        await ctx.send (embed=embed, delete_after=60)
    else:
        await ctx.send('That\'s not a valid field!')


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



load_list = ['moderation', 'fun', 'meta',]

for i in load_list:
    bot.load_extension(f'cogs.{i}')
    
bot.run(token)
