import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
import pickle

class Cleverbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Cleverbot(bot))