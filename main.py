import discord
import asyncio
from discord.ext import commands, tasks
from itertools import cycle
import sys
import traceback
import os
from dotenv import load_dotenv
import aiosqlite
import dbl

load_dotenv()
bot = commands.Bot(command_prefix = commands.when_mentioned_or('/', '@'), case_insensitive=True)
class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)

bot.help_command = MyNewHelp()
bot_version = 'Version 0.1.12 [BETA]'
intents = discord.Intents.default()
intents.members = True
#a regular, b remembrance day, c halloween
status = cycle(['/help is the way to go!', 'Use /about to learn more!'])

#when the bot is ready
@bot.event
async def on_ready():
    change_status.start()
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_command_error(ctx, error):
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send ('You don\'t have permmission to do that!')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You\'re missing an argument. Check the command and ensure that all arguments are present.')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('One or more of your arguments didn\'t make sense. Are you sure that your arguments are of the right type?')
    elif isinstance(error, discord.Forbidden):
        await ctx.send('I don\'t have permission to do that! Make sure I have the correct permissions, then try again.')
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(error)
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send('You\'re not in a server! This command is server-only.')
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        embed = discord.Embed(title='Oh noes!', description = f'Something went wrong: \n ```{error}``` \
            \n The devs have been notified. If this continues, please file a bug report using `/bugreport`.')
        await ctx.send(embed=embed)


def findPrefix(bot, message):
    connection = asyncio.run(aiosqlite.connect('AltBotDataBase.db'))
    cursor = asyncio.run(connection.cursor())
    asyncio.run(cursor.execute('SELECT * from SERVERADMIN WHERE id = ?', (message.guild.id)))
    if asyncio.run(cursor.fetchone()) is None:
        asyncio.run(cursor.execute('INSERT INTO SERVERADMIN VALUES (?,?)', (message.guild.id, '/')))
        return '/'
    else:
        asyncio.run(cursor.execute('SELECT * FROM SERVERADMIN WHERE id = ?', (message.guild.id,)))
        server = asyncio.run(cursor.fetchone())
        return server[1]

@bot.event
async def on_message(message):
    if len(message.mentions)>4:
        try:
            await message.delete()
        except:
            pass
        else:
            await message.channel.send(f'{message.author.mention}, Don\'t mass ping!')
    else:
        await bot.process_commands(message)

#change the playing status
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

# This example uses dblpy's webhook system.
# In order to run the webhook, at least webhook_port argument must be specified (number between 1024 and 49151).

dbl_token = os.getenv('TOPGGTOKEN')
bot.dblpy = dbl.DBLClient(bot, dbl_token, webhook_path='/dblwebhook', webhook_auth='password', webhook_port=5000)

@bot.event
async def on_dbl_vote(data):
    """An event that is called whenever someone votes for the bot on top.gg."""
    print(f"Received an upvote:\n{data}")

load_list = ['moderation', 'fun', 'meta', 'logging', 'admin', 'premium', 'music']

@bot.command()
async def dev(ctx, reload = None, cog = None):
    success = True
    if await bot.is_owner(ctx.author) or reload == 'reload':
        if cog is None:
            message = ''
            for i in load_list:
                try:
                    bot.reload_extension(f'cogs.{i}')
                except:
                    message += f'Something went wrong while reloading cog {i} :x: \n'
                    success = False
                else:
                    message += f'Cog {i} was successfully reloaded :white_check_mark: \n'
            if not success:
                message += 'All cogs reloaded successfully!'
            await ctx.send(message)
        else:
            try:
                bot.reload_extension(f'cogs.{cog}')
            except:
                await ctx.send(f'Something went wrong while reloading cog {cog} :x:')
            else:
                await ctx.send(f'Cog {cog} was successfully reloaded :white_check_mark:')
    else:
        await ctx.send('You can\'t do that!')

#unused = discord.utils.find(lambda role: not role.members, guild.roles)
# for attributes, it's easier with
#admin = discord.utils.get(guild.roles, name='admin')
# AND
#channel = discord.utils.get(guild.text_channels, name='help', topic='help channel')
# when was the message created?
#created_at = discord.utils.snowflake_time(discord_id) # works for almost all IDs
# Invite Me!
#invite = discord.utils.oauth_url(bot.user.id, guild.me.guild_permissions)
# Escape markdowns...
#safe = discord.utils.escape_markdown('**Bold text** and ||spoiler||')
# Don't Mention It!
#safe_everyone = discord.utils.escape_mentions(guild.me.mention)

for i in load_list:
    bot.load_extension(f'cogs.{i}')
    
bot.run(os.getenv('TOKEN'))
