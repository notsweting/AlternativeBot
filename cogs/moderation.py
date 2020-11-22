import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
import datetime
import time
import aiosqlite

'''
Table definitions:

TABLE MUTEDROLES, columns (ServerID, RoleID)
TABLE LOGGING, columns (ServerID, LoggingToggle, LoggingChannelID)
'''

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #clear command
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def purge(self, ctx, amount : int=5):
        embed = discord.Embed (title='**A purge has been run!**', color=ctx.author.color, timestamp=ctx.message.created_at)
        embed.add_field(name='Purged messages:', value=amount)
        embed.add_field(name='Purged by:', value=ctx.author.mention)
        embed.set_footer(text='Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.has_permissions(kick_members=True)   
    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason='no reason'):
        embed = discord.Embed (title=f'You\'ve been kicked from {ctx.guild.name}!', color=member.color, timestamp=ctx.message.created_at)
        embed.add_field(name='You were kicked by:', value=ctx.author.mention)
        embed.add_field(name='Reason:', value=reason)
        embed.set_footer(text='Support: https://discord.gg/33utPs9')
        try:
            msg = await member.send(embed=embed)
        except:            
            await ctx.send('I couldn\'t DM the selected member with details about their kick.')
            try:
                await ctx.guild.kick(member, reason=reason)
            except discord.Forbidden:
                await ctx.send('I couldn\'t kick the selected member.')
            else:
                await ctx.send(f'Kicked {member.mention} for {reason}. They could not be messaged about their kick.')
        else:
            try:
                await ctx.guild.kick(member, reason=reason)
            except discord.Forbidden:
                await ctx.send('I couldn\'t kick the selected member.')
                await msg.delete()
            else:
                await ctx.send(f'Successfully kicked {member.mention} for {reason}. They have also been DMed about their kick.')

    @commands.guild_only()
    @commands.has_permissions(ban_members=True)   
    @commands.command()
    async def ban(self, ctx, member : discord.User, *, reason = None):
        embed = discord.Embed (title=f'You\'ve been permanently banned from {ctx.guild.name}!', color=member.color, timestamp=ctx.message.created_at)
        embed.add_field(name='You were banned by:', value=ctx.author.mention)
        embed.add_field(name='Reason:', value=reason)
        embed.set_footer(text='Support: https://discord.gg/33utPs9')
        try:
            msg = await member.send(embed=embed)
        except:            
            await ctx.send('I couldn\'t DM the selected member with details about their ban.')
            try:
                await ctx.guild.ban(member, reason=reason)
            except discord.Forbidden:
                await ctx.send('I couldn\'t ban the selected member.')
            else:
                await ctx.send(f'Banned {member.mention} for {reason}. They could not be messaged about their ban.')
        else:
            try:
                await ctx.guild.ban(member, reason=reason)
            except discord.Forbidden:
                await ctx.send('I couldn\'t ban the selected member.')
                await msg.delete()
            else:
                await ctx.send(f'Successfully banned {member.mention} for {reason}. They have also been DMed about their ban.')

    @commands.guild_only()
    @commands.has_permissions(ban_members=True)   
    @commands.command()
    async def unban(self, ctx, member : discord.User, *, reason='No reason'):
        await ctx.guild.unban(member)
        try:
            embed = discord.Embed (title=f'You\'ve been unbanned from {ctx.guild.name}!', color=member.color, timestamp=ctx.message.created_at)
            embed.add_field(name='You were unbanned by:', value=ctx.author.mention)
            embed.add_field(name='Reason:', value=reason)
            embed.set_footer(text='Support: https://discord.gg/33utPs9')
            await member.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(f'{member.mention}, unbanned. I could not message them about their unban.')
        else:
            await ctx.send(f'{member.mention}, successfully unbanned.')
    
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def mute(self, ctx, member: discord.Member, *, reason = 'no reason'):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute(f'SELECT RoleID FROM MUTEDROLES WHERE ServerID=?', (ctx.guild.id))
        role = await cursor.fetchone()
        roleID = role[0]

        if roleID == None:
            await ctx.send('A Muted role has not been bound yet! Run `/bindmuterole` to bind a Muted role to this server!')
        else:
            role = discord.utils.get(ctx.guild.roles, id=int(roleID))
            if role != None:
                try:
                    await member.add_roles(role, reason=f'Muted by {ctx.author}, reason: {reason}')
                except discord.Forbidden:
                    await ctx.send('Hm. Something went wrong. Please try again and ensure that I have the `Manage Roles` permission.')
                else:
                    await ctx.send(f':thumbsup: Muted {member}')                            
            else:
                await ctx.send('Hmmmmm, it seems like your Muted role has been deleted! Please run `/bindmuterole` to bind a new one!')
        await connection.close()

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute(f'SELECT RoleID FROM MUTEDROLES WHERE ServerID=?', (ctx.guild.id))
        role = await cursor.fetchone()
        roleID = role[0]

        if roleID == None:
            await ctx.send('A Muted role has not been bound yet! Run `/bindmuterole` to bind a Muted role to this server!')
        else:
            role = discord.utils.get(ctx.guild.roles, id=int(roleID))
            if role != None:
                try:
                    await member.add_roles(role, reason=f'Unmuted by {ctx.author}')
                except discord.Forbidden:
                    await ctx.send('Hm. Something went wrong. Please try again and ensure that I have the `Manage Roles` permission.')
                else:
                    await ctx.send(f':thumbsup: Unmuted {member}')                            
            else:
                await ctx.send('Hmmmmm, it seems like your Muted role has been deleted! Please run `/bindmuterole` to bind a new one!')            
        await connection.close()

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def bindmuterole(self, ctx, role: discord.Role = None):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        if role == None:
            await cursor.execute(f'SELECT RoleID FROM MUTEDROLES WHERE ServerID=?', (ctx.guild.id))
            role = await cursor.fetchone()
            roleID = role[0]
            if role == None:
                role = await ctx.guild.create_role(name = 'Muted', reason = f'{ctx.author} (ID:{ctx.author.id}) ran /bindmuterole')
                for i in ctx.guild.channels:
                    await i.set_permissions(role, send_messages=False)
                await cursor.execute(f'INSERT INTO MUTEDROLES(ServerID, RoleID) VALUES (?, ?)', (ctx.guild.id, role.id))
                await ctx.send(f':thumbsup: Bound {role.mention} to {ctx.guild.name} as Muted role.')
            elif discord.utils.get(ctx.guild.roles, id=int(roleID)) != None:
                await ctx.send('A Muted role has already been bound to this server! Are you sure you want to continue? `yes/no`')
                def check(message : discord.Message) -> bool:
                    return message.author == ctx.author and message.channel == ctx.channel
                
                try:
                    message = await self.bot.wait_for('message', timeout = 60, check = check)
                except asyncio.TimeoutError: 
                    await ctx.send('You took too long to respond! Aborting process.')            
                else:
                    if message.content.lower() == 'yes':
                        role = await ctx.guild.create_role(name = 'Muted', reason = f'{ctx.author} (ID:{ctx.author.id}) ran /bindmuterole')
                        for i in ctx.guild.channels:
                            await i.set_permissions(role, send_messages=False)
                        await cursor.execute('UPDATE MUTEDROLES SET RoleID = ? WHERE ServerID = ?', (role.id, ctx.guild.id))
                        await ctx.send(f':thumbsup: Bound {role.mention} to {ctx.guild.name} as Muted role.')
                    else:
                        await ctx.send('Process aborted.')
            else:
                await ctx.send('A Muted role has already been bound to this server, but it was deleted. Binding new Muted role.')
                role = await ctx.guild.create_role(name = 'Muted', reason = f'{ctx.author} (ID:{ctx.author.id}) ran /bindmuterole')
                for i in ctx.guild.channels:
                    await i.set_permissions(role, send_messages=False)
                await cursor.execute('UPDATE MUTEDROLES SET RoleID = ? WHERE ServerID = ?', (role.id, ctx.guild.id))
                await ctx.send(f':thumbsup: Bound {role.mention} to {ctx.guild.name} as Muted role.')

        else:
            await cursor.execute(f'SELECT RoleID FROM MUTEDROLES WHERE ServerID=?', (ctx.guild.id))
            role = await cursor.fetchone()
            roleID = role[0]
            if role == None:
                await cursor.execute(f'INSERT INTO MUTEDROLES(ServerID, RoleID) VALUES (?, ?)', (ctx.guild.id, role.id))
                await ctx.send(f':thumbsup: Bound {role.mention} to {ctx.guild.name} as Muted role.')
        await connection.commit()
        await connection.close()

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def unbindmuterole(self, ctx):
        connection = await aiosqlite.connect('AltBotDataBase.db')
        cursor = await connection.cursor()
        await cursor.execute(f'SELECT RoleID FROM MUTEDROLES WHERE ServerID=?', (ctx.guild.id))
        role = await cursor.fetchone()
        roleID = role[0]
        if role == None:
            await ctx.send('This server doesn\'t have a Muted role! Aborting process.')
        elif discord.utils.get(ctx.guild.roles, id=int(roleID)) != None:
            await ctx.send('I\'m about to unbind this server\'s muted role! Are you sure? `yes/no`')
            def check(message : discord.Message) -> bool:
                return message.author == ctx.author and message.channel == ctx.channel
            
            try:
                message = await self.bot.wait_for('message', timeout = 60, check = check)
            except asyncio.TimeoutError: 
                await ctx.send('You took too long to respond! Aborting process.')
            else:
                if message.content.lower() == 'yes':
                    await cursor.execute(f'DELETE FROM MUTEDROLES WHERE ServerID = ?', (ctx.guild.id))
                    await ctx.send(f':thumbsup: {role.mention} is no longer this server\'s muted role.')
                else:
                    await ctx.send('Process aborted.')
        else:
            await ctx.send('A Muted role has already been bound to this server, but it was deleted. Aborting process.')
            await cursor.execute(f'DELETE FROM MUTEDROLES WHERE ServerID=?', (ctx.guild.id))
        await connection.commit()
        await connection.close()

    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def lock(self, ctx):
        for i in ctx.guild.roles:
                if i.permissions.manage_messages == True:
                    pass
                elif i in ctx.channel.overwrites:
                    await ctx.channel.set_permissions(i, send_messages=False)
                else:
                    pass
        await ctx.send(':thumbsup: Locked channel.')

    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def unlock(self, ctx):
        for i in ctx.guild.roles:
                if i.name == 'Muted':
                    pass
                elif i in ctx.channel.overwrites:
                    await ctx.channel.set_permissions(i, send_messages=True)
                else:
                    pass
        await ctx.send(':thumbsup: Unlocked channel.')

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def role(self, ctx, member : discord.Member, role : discord.Role):
        try:
            await member.add_roles(role, reason=f'{ctx.author}(ID: {ctx.author.id}) ran /role')
        except discord.Forbidden:
            await ctx.send('I don\'t have permission to do that! Make sure I have the correct permissions, then try again.')
        else:
            await ctx.send(f':white_check_mark: Added {role.name} to {member}')

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def removerole(self, ctx, member : discord.Member, role : discord.Role):
        try:
            await member.remove_roles(role, reason=f'{ctx.author}(ID: {ctx.author.id}) ran /removerole')
        except discord.Forbidden:
            await ctx.send('I don\'t have permission to do that! Make sure I have the correct permissions, then try again.')
        else:
            await ctx.send(f':white_check_mark: Removed {role.name} from {member}')

def setup(bot):
    bot.add_cog(Moderation(bot))