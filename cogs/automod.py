import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
import sqlite3
import datetime

'''
Table definitions:

TABLE MUTEDROLES, columns (ServerID, RoleID)
TABLE LOGGING, columns (ServerID, LoggingToggle, LoggingChannelID)
'''

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

def setup(bot):
    bot.add_cog(AutoMod(bot))
