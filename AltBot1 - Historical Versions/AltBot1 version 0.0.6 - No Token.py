import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import time
import os

client = commands.Bot(command_prefix = ["/"])
client.remove_command('help')

status_change = True

if status_change:
    status = cycle(['/help is the way to go!', 'Use /about to learn more!', 'Use /info to learn more!', 'Version 0.6 [ALPHA]', 'UNSTABLE',])
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
    embed.set_footer(text='Developed by ThisIsanAltYT#0117 | Contact him for more info!')
    await ctx.send (embed=embed)


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

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        
client.run(token)
