import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
import aiosqlite

'''
Table definitions:

TABLE MUTEDROLES, columns (ServerID, RoleID)
TABLE LOGGING, columns (ServerID, LoggingToggle, LoggingChannelID, \
    OnMsgDeleteToggle, OnBulkMsgDeleteToggle, OnMsgEditToggle, \
    OnReactionClearToggle, OnChannelCreateDeleteToggle, OnChannelEditToggle, \
    OnMemberJoinToggle, OnMemberLeaveToggle, OnMemberEditToggle, \
    OnGuildEditToggle, OnGuildRoleCreateDeleteToggle, OnGuildRoleUpdateToggle, \
    OnGuildMemberBanUnbanToggle, OnGuildMemberKickToggle, OnGuildInviteCreateDeleteToggle)
'''

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @commands.has_permissions(manage_server=True)
    @commands.command()
    async def togglelogging(self, ctx, ):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (ctx.guild.id))
        info = await cursor.fetchone()
        if info == None:
            await ctx.send('You don\'t have a logging channel set up yet! Please run `bindloggingchannel` to set up a logging channel!')
        
    
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def bindloggingchannel(self, ctx, channel : discord.Channel):
        pass
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (message.guild.id))
        info = await cursor.fetchone()
        if info == None:
            pass
        else:
            if info[3] == None:
                pass
            else:
                channel = discord.utils.get(ctx.guild.channels, id=info[2])
                try:
                    embed = discord.Embed(title = 'Message deleted in {message.channel}', description = message.content, timestamp = ctx.message.created_at)
                    embed.set_footer(text=f'{message.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
                    await channel.send(embed=embed)
                except:
                    pass

def setup(bot):
    bot.add_cog(Logging(bot))