import discord
import asyncio
from discord.ext import commands, tasks, menus
from discord.ext.commands.cooldowns import BucketType
import sqlite3
from discord.ext import menus

class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    async def premium(self, ctx):
        embed = discord.Embed(title='AlternativeBot Premium Access', description='Unlock additional features by buying AlternativeBot Premium!', colour=0x00FFFF)
        embed.add_field(name='Perks:', value='Run `/premium perks` to view perks!')

def setup(bot):
    bot.add_cog(Premium(bot))