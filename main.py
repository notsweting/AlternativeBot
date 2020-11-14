import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
from itertools import cycle

bot = commands.Bot(command_prefix = commands.when_mentioned_or('/', '@'), case_insensitive=True)
bot.remove_command('help')
bot_version = 'Version 0.1.12 [BETA]'
#b is rememberance day, a regular, c halloween
statuschoice = 'a'
regularstatus = cycle(['/help is the way to go!', 'Use /about to learn more!'])
statusremember = cycle(['Lest we forget', 'Lest we forget', 'Lest we forget'])
statushalloween = cycle(['/help is the way to go!', 'Use /about to learn more!', 'Happy Halloween!', 'Happy Halloween!', 'Happy Halloween!'])
if statuschoice == 'a':
    status = regularstatus
elif statuschoice == 'b':
    status = statusremember
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

load_list = ['moderation', 'fun', 'meta',]

@bot.command()
async def reload(ctx):
    if await bot.is_owner(ctx.author):
        for i in load_list:
            try:
                bot.reload_extension(f'cogs.{i}')
            except:
                await ctx.send(f'Something went wrong while load in cog {i} :x:')
            else:
                await ctx.send(f'Cog {i} was successfully loaded in :white_check_mark:')
    else:
        await ctx.send('You can\'t do that!')

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

for i in load_list:
    bot.load_extension(f'cogs.{i}')
    
bot.run(token)