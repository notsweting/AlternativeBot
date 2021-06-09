import discord
import asyncio
from discord.ext import commands, tasks, menus
from discord.ext.commands.cooldowns import BucketType
import aiosqlite
from discord.ext import menus
import requests
from dotenv import load_dotenv
import os
from math import sqrt

load_dotenv()
class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(alias=['h', 'hstats'])
    @commands.guild_only()
    async def hypixel(self, ctx, player):
        embed=discord.Embed(header=f'Hypixel Network Stats', title=f'{player}', footer='Made by sweting#9238 | !support')
        data = requests.get(f"https://api.hypixel.net/player?key={os.getenv('APIKEY')}&name={player}").json()
        friends = requests.get(f"https://api.hypixel.net/friends?key={os.getenv('APIKEY')}&uuid={data['player']['uuid']}").json()
        guild = requests.get(f"https://api.hypixel.net/guild?key={os.getenv('APIKEY')}&uuid={data['player']['uuid']}").json()
        questno = 0
        for i in data['player']['quests']:
            try:
                questno += len(i['completions'])
            except:
                pass

        embed.add_field(name='Rank:', value=data['player']['newPackageRank'] if not data['player']['monthlyPackageRank'] else 'MVP_PLUS_PLUS')
        embed.add_field(name='Network Level:', value=(sqrt((2 * data['player']['networkExp']) + 30625) / 50) - 2.5)
        embed.add_field(name='Karma:', value="{:,}".format(data['player']['karma']))
        embed.add_field(name='Achievement Points:', value="{:,}".format(data['player']['achievementPoints']))
        embed.add_field(name='Quests Completed:', value="{:,}".format(questno))
        embed.add_field(name='Friends:', value="{:,}".format(len(friends['player']['records'])))
        embed.add_field(name='Guild:', value="{:,}".format(data['player']['karma']))
        embed.add_field(name='Guild Tag:', value="{:,}".format(data['player']['karma']))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Premium(bot))