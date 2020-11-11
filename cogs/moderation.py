import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
import datetime
import time
import sqlite3

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #clear command
    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def purge(self, ctx, amount : int=5):
        embed = discord.Embed (title='**A purge has been run!**', color=ctx.author.color, timestamp=ctx.message.created_at)
        embed.add_field(name='Purged messages:', value=amount)
        embed.add_field(name='Purged by:', value=ctx.author.mention)
        embed.set_footer(text='Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(embed=embed)

    @commands.has_permissions(kick_members=True)   
    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason='no reason'):
        if ctx.guild != None:
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
        else:
            await ctx.send('You aren\'t in a guild at the moment. Try again in a guild.')

    @commands.has_permissions(ban_members=True)   
    @commands.command()
    async def ban(self, ctx, member : discord.User, *, reason = None):
        if ctx.guild != None:
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
        else:
            await ctx.send('You aren\'t in a guild at the moment. Try again in a guild.')

    @commands.has_permissions(ban_members=True)   
    @commands.command()
    async def unban(self, ctx, member : discord.User, *, reason='No reason'):
        if ctx.guild != None:
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
        else:
            await ctx.send('You aren\'t in a guild at the moment. Try again in a guild.')
    
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def mute(self, ctx, member: discord.Member, *, reason = 'no reason'):
        if ctx.guild != None:  
            role = discord.utils.get(ctx.guild.roles, name='Muted')
            await member.add_roles(role, reason=f'Muted by {ctx.author}, reason: {reason}')
            await ctx.send(f':thumbsup: Muted {member}')
        else:
            await ctx.send('You aren\'t in a guild at the moment. Try again in a guild.')
    
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        if ctx.guild != None:  
            role = discord.utils.get(ctx.guild.roles, name='Muted')
            await member.remove_roles(role, reason=f'Unmute by {ctx.author}')
            await ctx.send(f':thumbsup: Unmuted {member}')
        else:
            await ctx.send('You aren\'t in a guild at the moment. Try again in a guild.')
    
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
    
def setup(bot):
    bot.add_cog(Moderation(bot))