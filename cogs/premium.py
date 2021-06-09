import discord
import asyncio
from discord.ext import commands, tasks, menus
from discord.ext.commands.cooldowns import BucketType
import aiosqlite
from discord.ext import menus

class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    async def premium(self, ctx, arg=None):
        if not arg:
            embed = discord.Embed(title='AlternativeBot Premium Access', description='Unlock additional features by buying AlternativeBot Premium!', colour=0x00FFFF)
            embed.add_field(name='Perks:', value='Run `/premium perks` to view perks!')
            embed.add_field(name='Buying:', value='Run `/premium buy` to buy premium!')
        elif arg.lower() == 'perks':
            embed = discord.Embed(title='AlternativeBot Premium Perks', description='Perks you get for buying AlternativeBot Premium!')
            embed.add_field(name='Additional Music Features', description='-Ability to control volume')
            embed.add_field(name='Prioritized Bug Reports', description='-Bug reports are handled separately\n-Premium support queue when things go wrong')
            embed.add_field(name='Exclusive BETA Features', description='-Gain access to commands nobody else has\n-Exclusive BETA bot ')


def setup(bot):
    bot.add_cog(Premium(bot))