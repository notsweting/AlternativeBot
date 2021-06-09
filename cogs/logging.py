import discord
import asyncio
from discord.ext import commands, tasks, menus
from discord.ext.commands.cooldowns import BucketType
import aiosqlite
from discord.ext import menus
import datetime

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
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (self.guild_id,))
        info = await cursor.fetchone()
        await connection.close()
        listtoreturn = []
        if info[1] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :play_pause: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :play_pause: reaction.')
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
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :one: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :one: reaction.')
        if info[10] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :two: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :two: reaction.')
        if info[11] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :three: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :three: reaction.')
        if info[12] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :one: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :one: reaction.')
        if info[13] == True:
            listtoreturn.append(':white_check_mark: Enabled. Toggle with the :two: reaction.')
        else:
            listtoreturn.append(':x: Disabled. Toggle with the :two: reaction.')
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
        return tuple(listtoreturn)

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
        self.embed.set_footer(text='Page 1/5: Support: https://discord.gg/33utPs9')
        return await channel.send(embed=self.embed)

    @menus.button('\U000023ef\U0000fe0f')
    async def maintoggle(self, payload):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute('SELECT LoggingToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
        info = await cursor.fetchone()
        info = info[0]
        if info is None or info == False: 
            info = True
            enabled = ':white_check_mark: Enabled. Toggle with the :play_pause: reaction.'
        else:
            info = False
            enabled = ':x: Disabled. Toggle with the :play_pause: reaction.'
        await cursor.execute('UPDATE LOGGING SET LoggingToggle = ? WHERE ServerID = ?', (info, payload.guild_id))

        self.embed.insert_field_at(0, name='Main logging toggle:', value=enabled)
        self.embed.remove_field(1)
        await self.message.edit(embed=self.embed)
        await connection.commit()
        
    @menus.button('\U00000031\U0000fe0f\U000020e3')
    async def on_one(self, payload):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        if self.menupage == 1:
            await cursor.execute('SELECT OnMsgDeleteToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :one: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :one: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnMsgDeleteToggle = ? WHERE ServerID = ?', (info, payload.guild_id))

            self.embed.insert_field_at(1, name='On message delete toggle:', value=enabled)
        elif self.menupage == 2:
            await cursor.execute('SELECT OnReactionClearToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :one: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :one: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnReactionClearToggle = ? WHERE ServerID = ?', (info, payload.guild_id))

            self.embed.insert_field_at(1, name='On reaction clear toggle:', value=enabled)
        elif self.menupage == 3:
            await cursor.execute('SELECT OnMemberJoinToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :one: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :one: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnMemberJoinToggle = ? WHERE ServerID = ?', (info, payload.guild_id))

            self.embed.insert_field_at(1, name='On member join toggle:', value=enabled)
        elif self.menupage == 4:
            await cursor.execute('SELECT OnGuildEditToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :one: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :one: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnGuildEditToggle = ? WHERE ServerID = ?', (info, payload.guild_id))

            self.embed.insert_field_at(1, name='On guild edit toggle:', value=enabled)
        else:
            await cursor.execute('SELECT OnMemberBanUnbanToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :one: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :one: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnMemberBanUnbanToggle = ? WHERE ServerID = ?', (info, payload.guild_id))

            self.embed.insert_field_at(1, name='On member ban/unban toggle:', value=enabled)

        self.embed.remove_field(2)
        await self.message.edit(embed=self.embed)
        await connection.commit()

    @menus.button('\U00000032\U0000fe0f\U000020e3')
    async def on_two(self, payload):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        if self.menupage == 1:
            await cursor.execute('SELECT OnBulkMsgDeleteToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :two: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnBulkMsgDeleteToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(2, name='On bulk message delete toggle:', value=enabled)
            self.embed.remove_field(3)
            await self.message.edit(embed=self.embed)
            await connection.commit()
        elif self.menupage == 2:
            await cursor.execute('SELECT OnChannelCreateDeleteToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :two: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnChannelCreateDeleteToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(2, name='On channel create/delete toggle:', value=enabled)
            self.embed.remove_field(3)
            await self.message.edit(embed=self.embed)
            await connection.commit()
        elif self.menupage == 3:
            await cursor.execute('SELECT OnMemberLeaveToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :two: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnMemberLeaveToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(2, name='On member leave toggle:', value=enabled)
            self.embed.remove_field(3)
            await self.message.edit(embed=self.embed)
        elif self.menupage == 4:
            await cursor.execute('SELECT OnGuildRoleCreateDeleteToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :two: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnGuildRoleCreateDeleteToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(2, name='On role create/delete toggle:', value=enabled)
            self.embed.remove_field(3)
            await self.message.edit(embed=self.embed)
        else:
            await cursor.execute('SELECT OnMemberKickToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :two: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnMemberKickToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(2, name='On member kick toggle:', value=enabled)
            self.embed.remove_field(3)
            await self.message.edit(embed=self.embed)

    @menus.button('\U00000033\U0000fe0f\U000020e3')
    async def on_three(self, payload):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        if self.menupage == 1:
            await cursor.execute('SELECT OnMsgEditToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :three: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnMsgEditToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(3, name='On message edit toggle:', value=enabled)
        elif self.menupage == 2:
            await cursor.execute('SELECT OnChannelEditToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :three: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnChannelEditToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(3, name='On channel edit toggle:', value=enabled)
        elif self.menupage == 3:
            await cursor.execute('SELECT OnMemberEditToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :two: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnMemberEditToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(3, name='On member edit toggle:', value=enabled)
        elif self.menupage == 4:
            await cursor.execute('SELECT OnGuildRoleUpdateToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :two: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnGuildRoleUpdateToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(3, name='On role edit toggle:', value=enabled)
        else:
            await cursor.execute('SELECT OnGuildInviteCreateDeleteToggle FROM LOGGING WHERE ServerID = ?', (payload.guild_id,))
            info = await cursor.fetchone()
            info = info[0]
            if info is None or info == False: 
                info = True
                enabled = ':white_check_mark: Enabled. Toggle with the :two: reaction.'
            else:
                info = False
                enabled = ':x: Disabled. Toggle with the :two: reaction.'
            await cursor.execute('UPDATE LOGGING SET OnGuildInviteCreateDeleteToggle = ? WHERE ServerID = ?', (info, payload.guild_id))
            self.embed.insert_field_at(3, name='On invite create/delete toggle:', value=enabled)

        self.embed.remove_field(4)
        await self.message.edit(embed=self.embed)
        await connection.commit()
    
    @menus.button('\U000025c0\U0000fe0f')
    async def on_left(self, payload):
        self.embed.clear_fields()
        info = await self.return_values()
        if self.menupage == 1:
            self.menupage = 5
            self.embed.add_field(name='Main logging toggle:', value = info[0])
            self.embed.add_field(name='On member ban toggle:', value = info[13])
            self.embed.add_field(name='On member kick toggle:', value = info[14])
            self.embed.add_field(name='On guild invite create toggle:', value = info[15])
            self.embed.set_footer(text='Page 5/5: Support: https://discord.gg/33utPs9')
        elif self.menupage == 2:
            self.menupage = 1
            self.embed.add_field(name='Main logging toggle:', value = info[0])
            self.embed.add_field(name='On message delete toggle:', value = info[1])
            self.embed.add_field(name='On bulk message delete toggle:', value = info[2])
            self.embed.add_field(name='On message edit toggle:', value = info[3])
            self.embed.set_footer(text='Page 1/5: Support: https://discord.gg/33utPs9')
        elif self.menupage == 3:
            self.menupage = 2
            self.embed.add_field(name='Main logging toggle:', value = info[0])
            self.embed.add_field(name='On reaction clear toggle:', value = info[4])
            self.embed.add_field(name='On channel create/delete toggle:', value = info[5])
            self.embed.add_field(name='On channel edit toggle:', value = info[6])
            self.embed.set_footer(text='Page 2/5: Support: https://discord.gg/33utPs9')
        elif self.menupage == 4:
            self.menupage = 3
            self.embed.add_field(name='Main logging toggle:', value = info[0])
            self.embed.add_field(name='On member join toggle:', value = info[7])
            self.embed.add_field(name='On member leave toggle:', value = info[8])
            self.embed.add_field(name='On member edit toggle:', value = info[9])
            self.embed.set_footer(text='Page 3/5: Support: https://discord.gg/33utPs9')
        else:
            self.menupage = 4
            self.embed.add_field(name='Main logging toggle:', value = info[0])
            self.embed.add_field(name='On guild edit toggle:', value = info[10])
            self.embed.add_field(name='On role create/delete toggle:', value = info[11])
            self.embed.add_field(name='On role edit toggle:', value = info[12])
            self.embed.set_footer(text='Page 4/5: Support: https://discord.gg/33utPs9')
        await self.message.edit(embed = self.embed)

    @menus.button('\U000025b6\U0000fe0f')
    async def on_right(self, payload):
        self.embed.clear_fields()
        info = await self.return_values()
        if self.menupage == 4:
            self.menupage = 5
            self.embed.add_field(name='Main logging toggle:', value = info[0])
            self.embed.add_field(name='On member ban toggle:', value = info[13])
            self.embed.add_field(name='On member kick toggle:', value = info[14])
            self.embed.add_field(name='On guild invite create toggle:', value = info[15])
            self.embed.set_footer(text='Page 5/5: Support: https://discord.gg/33utPs9')
        elif self.menupage == 5:
            self.menupage = 1
            self.embed.add_field(name='Main logging toggle:', value = info[0])
            self.embed.add_field(name='On message delete toggle:', value = info[1])
            self.embed.add_field(name='On bulk message delete toggle:', value = info[2])
            self.embed.add_field(name='On message edit toggle:', value = info[3])
            self.embed.set_footer(text='Page 1/5: Support: https://discord.gg/33utPs9')
        elif self.menupage == 1:
            self.menupage = 2
            self.embed.add_field(name='Main logging toggle:', value = info[0])
            self.embed.add_field(name='On reaction clear toggle:', value = info[4])
            self.embed.add_field(name='On channel create/delete toggle:', value = info[5])
            self.embed.add_field(name='On channel edit toggle:', value = info[6])
            self.embed.set_footer(text='Page 2/5: Support: https://discord.gg/33utPs9')
        elif self.menupage == 2:
            self.menupage = 3
            self.embed.add_field(name='Main logging toggle:', value = info[0])
            self.embed.add_field(name='On member join toggle:', value = info[7])
            self.embed.add_field(name='On member leave toggle:', value = info[8])
            self.embed.add_field(name='On member edit toggle:', value = info[9])
            self.embed.set_footer(text='Page 3/5: Support: https://discord.gg/33utPs9')
        else:
            self.menupage = 4
            self.embed.add_field(name='Main logging toggle:', value = info[0])
            self.embed.add_field(name='On guild edit toggle:', value = info[10])
            self.embed.add_field(name='On role create/delete toggle:', value = info[11])
            self.embed.add_field(name='On role edit toggle:', value = info[12])
            self.embed.set_footer(text='Page 4/5: Support: https://discord.gg/33utPs9')
        await self.message.edit(embed = self.embed)

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
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (ctx.guild.id,))
        info = await cursor.fetchone()
        if info is None or info[2] is None:
            await ctx.send('You don\'t have a logging channel set up yet! Please run `/bindloggingchannel` to set up a logging channel!')
        else:
            m = MyMenu()
            await m.start(ctx)
        await connection.close()        
               
    
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def bindloggingchannel(self, ctx, channel : discord.TextChannel):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute(f'SELECT LoggingChannelID FROM LOGGING WHERE ServerID=?', (ctx.guild.id,))
        info = await cursor.fetchone()
        if info == None:
            await cursor.execute(f'INSERT INTO LOGGING(ServerID, LoggingChannelID) VALUES (?, ?)', (ctx.guild.id, channel.id))
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
                    await cursor.execute('UPDATE LOGGING SET LoggingChannelID = ? WHERE ServerID = ?', (channel.id, ctx.guild.id))
                    await ctx.send(f':thumbsup: Bound {channel.mention} to {ctx.guild.name} as logging channel.')
                else:
                    await ctx.send('Process aborted.')
        else:
            await ctx.send('A logging channel has already been bound to this server, but it was deleted. Binding new Muted role.')
            await cursor.execute('UPDATE LOGGING SET LoggingChannelID = ? WHERE ServerID = ?', (channel.id, ctx.guild.id))
            await ctx.send(f':thumbsup: Bound {channel.mention} to {ctx.guild.name} as logging channel.')
        await connection.commit()
        await connection.close()   
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (message.guild.id,))
        info = await cursor.fetchone()
        await connection.close()
        if (
            info != None
            and message.author.id != 527682196744699924
            and info[3] != None
            and info[3] != False
            and info[1] != None
            and info[1] != False
        ):
            channel = discord.utils.get(message.guild.channels, id=info[2])
            async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete, before=datetime.datetime.utcnow()):
                author = entry.user if not None else author
            try:
                embed = discord.Embed(title = f'Message deleted in #{message.channel}', description = f'**Message content:** {message.content}\n\n**Deleted by:**{author.mention}', timestamp = datetime.datetime.utcnow(), colour = 0xFF5353)
                embed.set_footer(text=f'Author: {message.author} | Support: https://discord.gg/33utPs9', icon_url=message.author.avatar_url)
                await channel.send(embed=embed)
            except:
                pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (before.guild.id,))
        info = await cursor.fetchone()
        await connection.close()
        if (
            info != None
            and info[5] != None
            and info[5] != False
            and info[1] != False
            and before.content != after.content
        ):
            loggingchannel = self.bot.get_channel(info[2])
            embed = discord.Embed(title = f'Message edited in {before.channel.name}', description = f'**Before:**\n{before.content}\n\n**After:**\n{after.content}', timestamp = datetime.datetime.utcnow(), colour = 0xFF5353)
            embed.set_footer(text=f'Author: {before.author} Support: https://discord.gg/33utPs9', icon_url=before.author.avatar_url)
            await loggingchannel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_reaction_clear(self, message, reactions):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (message.guild.id,))
        info = await cursor.fetchone()
        await connection.close()
        if info == None:
            pass
        else:
            if info[6] == None or info[6] == False or info[5] == None or info[1] == False:
                pass
            else:
                loggingchannel = self.bot.get_channel(info[2])
                embed = discord.Embed(title = f'Reactions cleared in {message.channel.name}', description = f'Reactions cleared: {i for i in reactions}', timestamp = datetime.datetime.utcnow(), colour = 0xFF5353)
                embed.set_footer(text=f'Support: https://discord.gg/33utPs9', icon_url=self.bot.user.avatar_url)
                await loggingchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (channel.guild.id,))
        info = await cursor.fetchone()
        await connection.close()
        if (
            info is not None
            and info[7] != None
            and info[7] != False
            and info[5] != None
            and info[1] != False
        ):
            async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create, before=datetime.datetime.utcnow()):
                creator = entry.user
                reason = entry.reason
            loggingchannel = self.bot.get_channel(info[2])
            embed = discord.Embed(title = f'New channel created: {channel.name}', description = f'**Creator of the channel:**\n{creator.mention}\n\n**Reason:**\n{reason}', timestamp = datetime.datetime.utcnow(), colour = 0xFF5353)
            embed.set_footer(text=f'Support: https://discord.gg/33utPs9', icon_url=self.bot.user.avatar_url)
            await loggingchannel.send(embed=embed) 


    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        pass

    @commands.Cog.listener()
    async def on_guild_channel_edit(self, before, after):
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        pass

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        pass

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        pass

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        pass

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        pass

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        pass
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        pass

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        pass
    
    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        pass

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        pass

'''
TABLE LOGGING, columns (ServerID, LoggingToggle, LoggingChannelID, \
OnMsgDeleteToggle, OnBulkMsgDeleteToggle, OnMsgEditToggle, \
OnReactionClearToggle, OnChannelCreateDeleteToggle, OnChannelEditToggle, \
OnMemberJoinToggle, OnMemberLeaveToggle, OnMemberEditToggle, \
OnGuildEditToggle, OnGuildRoleCreateDeleteToggle, OnGuildRoleUpdateToggle, \
OnGuildMemberBanUnbanToggle, OnGuildMemberKickToggle, OnGuildInviteCreateDeleteToggle)
'''
def setup(bot):
    bot.add_cog(Logging(bot))