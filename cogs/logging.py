import discord
import asyncio
from discord.ext import commands, tasks, menus
from discord.ext.commands.cooldowns import BucketType
import sqlite3
from discord.ext import menus

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

class MyMenu(menus.Menu):

    async def send_initial_message(self, ctx, channel):
        self.connection = sqlite3.connect('AltBotDataBase.db')
        self.cursor = self.connection.cursor()
        self.menupage = 1
        embed = discord.Embed (title=f'Logging Toggles for {ctx.guild.name}', description='Use the reactions to navigate through the available options!')

        embed.add_field(name='On message delete toggle:', value='Enabled. Disable with the :one: reaction.')
        return await channel.send(embed = embed)

    @menus.button('\N{keycap ten}')
    async def on_ten(self, payload):
        if self.menupage == 1:
            self.cursor.execute('SELECT OnMsgDeleteToggle FROM LOGGING WHERE ServerID = ?', (payload.guild.id,))
            info = self.cursor.fetchone()
            info = info[0]
            if info == None or info == False: 
                info = True
            else:
                info = False
            self.cursor.execute('UPDATE LOGGING SET OnMsgDeleteToggle = ? WHERE ServerID = ?', (info, payload.guild.id))
            await self.message.edit(content='hi')

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def togglelogging(self, ctx):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (ctx.guild.id,))
        info = cursor.fetchone()
        if info == None or info[2] == None:
            await ctx.send('You don\'t have a logging channel set up yet! Please run `/bindloggingchannel` to set up a logging channel!')
        else:
            m = MyMenu()
            await m.start(ctx)
        connection.close()        
               
    
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def bindloggingchannel(self, ctx, channel : discord.TextChannel):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT LoggingChannelID FROM LOGGING WHERE ServerID=?', (ctx.guild.id,))
        info = cursor.fetchone()
        if info == None:
            cursor.execute(f'INSERT INTO LOGGING(ServerID, LoggingChannelID) VALUES (?, ?)', (ctx.guild.id, channel.id))
            await ctx.send(f':thumbsup: Bound {channel.mention} to {ctx.guild.name} as logging channel.')
        elif discord.utils.get(ctx.guild.channels, id=int(channel.id)) != None:
            await ctx.send('A logginc channel has already been bound to this server! Are you sure you want to continue? `yes/no`')
            def check(message : discord.Message) -> bool:
                return message.author == ctx.author and message.channel == ctx.channel
            
            try:
                message = await self.bot.wait_for('message', timeout = 60, check = check)
            except asyncio.TimeoutError: 
                await ctx.send('You took too long to respond! Aborting process.')            
            else:
                if message.content.lower() == 'yes':
                    cursor.execute('UPDATE LOGGING SET LoggingChannelID = ? WHERE ServerID = ?', (channel.id, ctx.guild.id))
                    await ctx.send(f':thumbsup: Bound {channel.mention} to {ctx.guild.name} as logging channel.')
                else:
                    await ctx.send('Process aborted.')
        else:
            await ctx.send('A logging channel has already been bound to this server, but it was deleted. Binding new Muted role.')
            cursor.execute('UPDATE LOGGING SET LoggingChannelID = ? WHERE ServerID = ?', (channel.id, ctx.guild.id))
            await ctx.send(f':thumbsup: Bound {channel.mention} to {ctx.guild.name} as logging channel.')
        connection.commit()
        connection.close()   
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT OnMsgDeleteToggle FROM LOGGING WHERE ServerID = ?', (message.guild.id,))
        info = cursor.fetchone()
        if info == None:
            pass
        else:
            if info[0] == None or info[0] == False:
                pass
            else:
                channel = discord.utils.get(message.guild.channels, id=info[2])
                try:
                    embed = discord.Embed(title = 'Message deleted in {message.channel}', description = message.content, timestamp = message.message.created_at)
                    embed.set_footer(text=f'{message.author} | Support: https://discord.gg/33utPs9', icon_url=message.author.avatar_url)
                    await channel.send(embed=embed)
                except:
                    pass
        connection.close()

def setup(bot):
    bot.add_cog(Logging(bot))