import discord
import asyncio
from discord.ext import commands, tasks, menus
from discord.ext.commands.cooldowns import BucketType
import sqlite3
from discord.ext import menus
import time

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
    async def return_values(self):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (self.guild_id,))
        info = cursor.fetchone()
        connection.close()
        listtoreturn = []
        if info[1] == True:
            listtoreturn.append(':white_check_mark: Main logging toggle on. Disable with the :stop_button: reaction.')
        else:
            listtoreturn.append(':x: Main logging toggle off. Enable with the :play_pause: reaction.')
        if info[2] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :one: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :one: reaction.')
        if info[3] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :two: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :two: reaction.')
        if info[4] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[5] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[6] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :one: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :one: reaction.')
        if info[7] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :two: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :two: reaction.')
        if info[8] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[9] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[10] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :one: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :one: reaction.')
        if info[11] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :two: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :two: reaction.')
        if info[12] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[13] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[14] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :one: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :one: reaction.')
        if info[15] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :two: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :two: reaction.')
        if info[16] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[17] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[18] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :one: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :one: reaction.')
        if info[19] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :two: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :two: reaction.')
        if info[20] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[21] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        return tuple(listtoreturn)

    async def send_initial_message(self, ctx, channel):
        self.menupage = 1
        self.guild_name = ctx.guild.name
        self.guild_id = ctx.guild.id
        self.embed = discord.Embed (title=f'Logging Toggles for {ctx.guild.name}', description='Use the reactions to navigate through the available options!')
        info = self.return_values()
        self.embed.add_field(name='On message delete toggle:', value = info[1])
        self.embed.add_field(name='On bulk message delete toggle:', value = info[2])
        return await channel.send(embed=self.embed)

    @menus.button('\U00000031\U0000fe0f\U000020e3')
    async def on_one(self, payload):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        if self.menupage == 1:
            cursor.execute('SELECT OnBulkMsgDeleteToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = cursor.fetchone()
            info = info[0]
            if info == None or info == False: 
                info = True
            else:
                info = False
            cursor.execute('UPDATE LOGGING SET OnMsgDeleteToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            info = self.return_values()
            self.embed.insert_field_at(0, name='On message delete toggle:', value=info[1])
            self.embed.remove_field(1)
            cursor.execute('UPDATE LOGGING SET OnMsgDeleteToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            await self.message.edit(embed=self.embed)
            connection.commit()

    @menus.button('\U00000032\U0000fe0f\U000020e3')
    async def on_two(self, payload):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        if self.menupage == 1:
            cursor.execute('SELECT OnBulkMsgDeleteToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = cursor.fetchone()
            info = info[0]
            if info == None or info == False: 
                info = True
            else:
                info = False
            info = self.return_values()
            self.embed.insert_field_at(1, name='On bulk message delete toggle:', value=info[2])
            self.embed.remove_field(2)
            cursor.execute('UPDATE LOGGING SET OnMsgDeleteToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            await self.message.edit(embed=self.embed)
            connection.commit()

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
            await ctx.send('A logging channel has already been bound to this server! Are you sure you want to continue? `yes/no`')
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
        cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (message.guild.id,))
        info = cursor.fetchone()
        connection.close()
        if info == None:
            pass
        else:
            if info[3] == None or info[3] == False:
                pass
            else:
                channel = discord.utils.get(message.guild.channels, id=info[2])
                try:
                    embed = discord.Embed(title = f'Message deleted in #{message.channel}', description = message.content, timestamp = message.created_at, colour = 0xFF5353)
                    embed.set_footer(text=f'Author: {message.author} | Support: https://discord.gg/33utPs9', icon_url=message.author.avatar_url)
                    await channel.send(embed=embed)
                except:
                    pass
    
    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
        info = cursor.fetchone()
        connection.close()
        if info == None:
            pass
        else:
            if info[4] == None or info[4] == False:
                pass
            else:
                channel = self.bot.get_channel(payload.channel_id)
                try:
                    embed = discord.Embed(title = f'Bulk message delete in #{channel.name}', description = 'A bulk message delete was run!', timestamp = time.time(), colour = 0xFF5353)
                    embed.set_footer(text=f'Support: https://discord.gg/33utPs9', icon_url=self.bot.avatar_url)
                    await channel.send(embed=embed)
                except:
                    pass

def setup(bot):
    bot.add_cog(Logging(bot))