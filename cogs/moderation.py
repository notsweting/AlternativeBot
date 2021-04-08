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
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM LOGGING WHERE ServerID = ?', (ctx.guild.id,))
        info = cursor.fetchone()
        connection.close()
        if info == None:
            pass
        else:
            if info[4] == None or info[4] == False or info[1] == None or info[1] == False:
                pass
            else:
                channel = self.bot.get_channel(ctx.channel.id)
                loggingchannel = self.bot.get_channel(info[2])
                embed = discord.Embed(title = f'Bulk message delete in #{channel.name}', description = f'A bulk message delete was run! User: {ctx.author}', timestamp = datetime.datetime.utcnow(), colour = 0xFF5353)
                embed.set_footer(text=f'Support: https://discord.gg/33utPs9', icon_url='https://cdn.discordapp.com/avatars/527682196744699924/f756a3c3af60b450514c27819dda8fcf.webp?size=1024')
                await loggingchannel.send(embed=embed)
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
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT RoleID FROM MUTEDROLES WHERE ServerID=?', (ctx.guild.id,))
        role = cursor.fetchone()
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
        connection.close()

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT RoleID FROM MUTEDROLES WHERE ServerID=?', (ctx.guild.id,))
        role = cursor.fetchone()
        roleID = role[0]

        if not roleID:
            await ctx.send('A Muted role has not been bound yet! Run `/bindmuterole` to bind a Muted role to this server!')
        else:
            role = discord.utils.get(ctx.guild.roles, id=int(roleID))
            if role != None:
                try:
                    await member.remove_roles(role, reason=f'Unmuted by {ctx.author}')
                except discord.Forbidden:
                    await ctx.send('Hm. Something went wrong. Please try again and ensure that I have the `Manage Roles` permission.')
                else:
                    await ctx.send(f':thumbsup: Unmuted {member}')                            
            else:
                await ctx.send('Hmmmmm, it seems like your Muted role has been deleted! Please run `/bindmuterole` to bind a new one!')            
        connection.close()

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def bindmuterole(self, ctx, role: discord.Role = None):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()   
        role = await ctx.guild.create_role(name = 'Muted', reason = f'{ctx.author} (ID:{ctx.author.id}) ran /bindmuterole') if not role else
        await ctx.send(discord.utils.escape_mentions(f'You\'re about to set {role.mention} as this server\'s Muted role. `Y/N`'))

        try:
            message = await self.bot.wait_for('message', timeout = 60, check = check)
        except asyncio.TimeoutError: 
            await ctx.send('You took too long to respond! Aborting process.')            
        else:
            if message.content.lower() == 'y':
                for i in ctx.guild.channels:
                await i.set_permissions(role, send_messages=False)
                cursor.execute(f'INSERT INTO MUTEDROLES(ServerID, RoleID) VALUES (?, ?)', (ctx.guild.id, role.id))
                await ctx.send(f':thumbsup: Bound {role.mention} to {ctx.guild.name} as Muted role.')
            else:
                await ctx.send('Process aborted.')
                await role.delete()
        connection.commit()
        connection.close()

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def unbindmuterole(self, ctx):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT RoleID FROM MUTEDROLES WHERE ServerID=?', (ctx.guild.id,))
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
                    cursor.execute(f'DELETE FROM MUTEDROLES WHERE ServerID = ?', (ctx.guild.id,))
                    await ctx.send(f':thumbsup: {role.mention} is no longer this server\'s muted role.')
                else:
                    await ctx.send('Process aborted.')
        else:
            await ctx.send('A Muted role has already been bound to this server, but it was deleted. Aborting process.')
            cursor.execute(f'DELETE FROM MUTEDROLES WHERE ServerID=?', (ctx.guild.id,))
        connection.commit()
        connection.close()

    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def lock(self, ctx):
        for i in ctx.guild.roles:
            if i.permissions.manage_messages == True:
                pass
            elif i in ctx.channel.overwrites:
                await ctx.channel.set_permissions(i, send_messages=False)
        await ctx.send(':thumbsup: Locked channel.')

    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def unlock(self, ctx):
        connection = sqlite3.connect('AltBotDataBase.db')
        cursor.execute(f'SELECT RoleID FROM MUTEDROLES WHERE ServerID=?', (ctx.guild.id,))
        roleID = cursor.fetchone()[0]
        connection.close()
        for i in ctx.guild.roles:
            if i.id = roleID:
                pass
            elif i in ctx.channel.overwrites:
                await ctx.channel.set_permissions(i, send_messages=True)
        await ctx.send(':thumbsup: Unlocked channel.')

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def role(self, ctx, member : discord.Member, role : discord.Role):
        if role not in member.roles:
            try:
                await member.add_roles(role, reason=f'{ctx.author}(ID: {ctx.author.id}) ran /role')
            except discord.Forbidden:
                await ctx.send(':x: I don\'t have permission to do that! Make sure I have the correct permissions, then try again.')
            else:
                await ctx.send(f':white_check_mark: Added {role.name} to {member}')
        else:
            try:
                await member.remove_roles(role, reason=f'{ctx.author}(ID: {ctx.author.id}) ran /role')
            except discord.Forbidden:
                await ctx.send(':x: I don\'t have permission to do that! Make sure I have the correct permissions, then try again.')
            else:
                await ctx.send(f':white_check_mark: Removed {role.name} from {member}')

def setup(bot):
    bot.add_cog(Moderation(bot))
