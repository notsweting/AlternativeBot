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
    async def togglelogging(self, ctx, choice = None):
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
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute('SELECT LoggingChannelID FROM LOGGING WHERE ServerID = ?', (ctx.guild.id))
        info = cursor.fetchone()
        loggingchannelID = info[0]
        if loggingchannelID == None:
            await ctx.send(f'Binding {channel.mention} as this server\'s logging channel...')
            await cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (ctx.guild.id))
            if cursor.fetchall() == None:
                await cursor.execute('INSERT INTO LOGGING(ServerID, LoggingChannelID) VALUES (?, ?)', (ctx.guild.id, channel.id))
                await ctx.send(f':thumbsup: Bound {channel.mention} to {ctx.guild.name} as logging channel.')
            else:
                await cursor.execute('UPDATE LOGGING SET LoggingChannelID = ? WHERE ServerID = ?', (channel.id, ctx.guild.id))
                await ctx.send(f':thumbsup: Bound {channel.mention} to {ctx.guild.name} as logging channel.')
        elif discord.utils.get(ctx.guild.channels, id=loggingchannelID) != None:
                await ctx.send('A logging channel has already been bound to this server! Are you sure you want to continue? `yes/no`')
                def check(message : discord.Message) -> bool:
                    return message.author == ctx.author and message.channel == ctx.channel                
                try:
                    message = await self.bot.wait_for('message', timeout = 60, check = check)
                except asyncio.TimeoutError: 
                    await ctx.send('You took too long to respond! Aborting process.')            
                else:
                    if message.content.lower() == 'yes':
                        await cursor.execute('UPDATE LOGGING SET LoggingChannelID = ? WHERE ServerID = ?', (channel.id, ctx.guild.id))
                        await ctx.send(f':thumbsup: Bound {channel.mention} to {ctx.guild.name} as logging channel.')
                    else:
                        await ctx.send('Process aborted.')
        else:
            await ctx.send('A logging channel has already been bound to this server, but it was deleted. Binding new logging channel.')
            await cursor.execute('UPDATE LOGGING SET LoggingChannelID = ? WHERE ServerID = ?', (channel.id, ctx.guild.id))
            await ctx.send(f':thumbsup: Bound {channel.mention} to {ctx.guild.name} as logging channel.')
                
    
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
                channel = discord.utils.get(message.guild.channels, id=info[2])
                try:
                    embed = discord.Embed(title = 'Message deleted in {message.channel}', description = message.content, timestamp = message.message.created_at)
                    embed.set_footer(text=f'{message.author} | Support: https://discord.gg/33utPs9', icon_url=message.author.avatar_url)
                    await channel.send(embed=embed)
                except:
                    pass

def setup(bot):
    bot.add_cog(Logging(bot))