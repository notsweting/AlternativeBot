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
            listtoreturn.append(':white_check_mark: Main logging toggle on. Disable with the :play_pause: reaction.')
        else:
            listtoreturn.append(':x: Main logging toggle off. Enable with the :play_pause: reaction.')
        if info[3] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :one: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :one: reaction.')
        if info[4] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :two: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :two: reaction.')
        if info[5] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[6] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[7] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :one: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :one: reaction.')
        if info[8] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :two: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :two: reaction.')
        if info[9] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[10] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[11] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :one: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :one: reaction.')
        if info[12] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :two: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :two: reaction.')
        if info[13] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[14] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[15] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :one: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :one: reaction.')
        if info[16] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :two: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :two: reaction.')
        if info[17] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        tupletoreturn = tuple(listtoreturn)
        return tupletoreturn

    async def send_initial_message(self, ctx, channel):
        self.menupage = 1
        self.guild_name = ctx.guild.name
        self.guild_id = ctx.guild.id
        self.embed = discord.Embed (title=f'Logging Toggles for {ctx.guild.name}', description='Use the reactions to navigate through the available options!')
        info = await self.return_values()
        self.embed.add_field(name='Main logging toggle:', value = info[0])
        self.embed.add_field(name='On message delete toggle:', value = info[1])
        self.embed.add_field(name='On bulk message delete toggle:', value = info[2])
        self.embed.add_field(name='On message edit toggle:', value = info[3])
        self.embed.set_footer(text='Page 1/3: Support: https://discord.gg/33utPs9')
        return await channel.send(embed=self.embed)

    @menus.button('\U000023ef\U0000fe0f')
    async def maintoggle(self, payload):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT LoggingToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
        info = cursor.fetchone()
        info = info[0]
        if info == None or info == False: 
            info = True
            enabled = ':white_check_mark: Enabled. Toggle with the :play_pause: reaction.'
        else:
            info = False
            enabled = ':x: Disabled. Toggle with the :play_pause: reaction.'
        cursor.execute('UPDATE LOGGING SET LoggingToggle = ? WHERE ServerID = ?', (info, payload.guild_id))

        self.embed.insert_field_at(0, name='Main logging toggle:', value=enabled)
        self.embed.remove_field(1)
        await self.message.edit(embed=self.embed)
        connection.commit()
        
    @menus.button('\U00000031\U0000fe0f\U000020e3')
    async def on_one(self, payload):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        if self.menupage == 1:
            cursor.execute('SELECT OnMsgDeleteToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = cursor.fetchone()
            info = info[0]
            if info == None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :one: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :one: reaction.'
            cursor.execute('UPDATE LOGGING SET OnMsgDeleteToggle = ? WHERE ServerID = ?', (info, payload.guild_id))

            self.embed.insert_field_at(1, name='On message delete toggle:', value=enabled)
            self.embed.remove_field(2)
            await self.message.edit(embed=self.embed)
            connection.commit()
        elif self.menupage == 2:
            cursor.execute('SELECT OnReactionClearToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = cursor.fetchone()
            info = info[0]
            if info == None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :one: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :one: reaction.'
            cursor.execute('UPDATE LOGGING SET OnReactionClearToggle = ? WHERE ServerID = ?', (info, payload.guild_id))

            self.embed.insert_field_at(1, name='On reaction clear toggle:', value=enabled)
            self.embed.remove_field(2)
            await self.message.edit(embed=self.embed)
            connection.commit()
        elif self.menupage == 3:
            pass
        elif self.menupage == 4:
            pass
        else:
            pass

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
                enabled = ':white_check_mark: Enabled. Toggle with the :two: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            cursor.execute('UPDATE LOGGING SET OnBulkMsgDeleteToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(2, name='On bulk message delete toggle:', value=enabled)
            self.embed.remove_field(3)
            await self.message.edit(embed=self.embed)
            connection.commit()
        elif self.menupage == 2:
            cursor.execute('SELECT OnChannelCreateDeleteToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = cursor.fetchone()
            info = info[0]
            if info == None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :two: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            cursor.execute('UPDATE LOGGING SET OnChannelCreateDeleteToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(2, name='On channel create/delete toggle:', value=enabled)
            self.embed.remove_field(3)
            await self.message.edit(embed=self.embed)
            connection.commit()
        elif self.menupage == 3:
            pass
        elif self.menupage == 4:
            pass
        else:
            pass

    @menus.button('\U00000033\U0000fe0f\U000020e3')
    async def on_three(self, payload):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        if self.menupage == 1:
            cursor.execute('SELECT OnMsgEditToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = cursor.fetchone()
            info = info[0]
            if info == None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :three: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            cursor.execute('UPDATE LOGGING SET OnMsgEditToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(3, name='On message edit toggle:', value=enabled)
            self.embed.remove_field(4)
            await self.message.edit(embed=self.embed)
            connection.commit()
        elif self.menupage == 2:
            cursor.execute('SELECT OnChannelEditToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = cursor.fetchone()
            info = info[0]
            if info == None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :three: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            cursor.execute('UPDATE LOGGING SET OnChannelEditToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(3, name='On channel edit toggle:', value=enabled)
            self.embed.remove_field(4)
            await self.message.edit(embed=self.embed)
            connection.commit()
        elif self.menupage == 3:
            cursor.execute('SELECT OnMemberEditToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = cursor.fetchone()
            info = info[0]
            if info == None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :two: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            cursor.execute('UPDATE LOGGING SET OnMemberEditToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(3, name='On member edit toggle:', value=enabled)
            self.embed.remove_field(4)
            await self.message.edit(embed=self.embed)
            connection.commit()
        elif self.menupage == 4:
            cursor.execute('SELECT OnGuildRoleUpdateToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = cursor.fetchone()
            info = info[0]
            if info == None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :two: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            cursor.execute('UPDATE LOGGING SET OnGuildRoleUpdateToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(3, name='On role edit toggle:', value=enabled)
            self.embed.remove_field(4)
            await self.message.edit(embed=self.embed)
            connection.commit()
        else:
            cursor.execute('SELECT OnGuildInviteCreateDeleteToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = cursor.fetchone()
            info = info[0]
            if info == None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :two: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            cursor.execute('UPDATE LOGGING SET OnGuildInviteCreateDeleteToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(3, name='On invite create/delete toggle:', value=enabled)
            self.embed.remove_field(4)
            await self.message.edit(embed=self.embed)
            connection.commit()

    @menus.button('\U000023f9\U0000fe0f')
    async def on_stop(self, payload):
        await self.message.delete()
        self.stop()

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
        if info == None or message.author.id == 527682196744699924:
            pass
        else:
            if info[3] == None or info[3] == False or info[1] == None or info[1] == False:
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
            if info[4] == None or info[4] == False or info[1] == None or info[1] == False:
                pass
            else:
                channel = self.bot.get_channel(payload.channel_id)
                loggingchannel = self.bot.get_channel(info[2])
                embed = discord.Embed(title = f'Bulk message delete in #{channel.name}', description = 'A bulk message delete was run!', colour = 0xFF5353)
                embed.set_footer(text=f'Support: https://discord.gg/33utPs9', icon_url='https://cdn.discordapp.com/avatars/527682196744699924/f756a3c3af60b450514c27819dda8fcf.webp?size=1024')
                await loggingchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (before.guild.id,))
        info = cursor.fetchone()
        connection.close()
        if info == None:
            pass
        else:
            if info[5] == None or info[5] == False or info[5] == None or info[1] == False or before.content == after.content:
                pass
            else:
                loggingchannel = self.bot.get_channel(info[2])
                embed = discord.Embed(title = f'Message edited in {before.channel.name}', description = f'**Before:**\n{before.content}\n\n**After:**\n{after.content}', timestamp = after.created_at, colour = 0xFF5353)
                embed.set_footer(text=f'Author: {before.author} Support: https://discord.gg/33utPs9', icon_url=before.author.avatar_url)
                await loggingchannel.send(embed=embed)

def setup(bot):
    bot.add_cog(Logging(bot))