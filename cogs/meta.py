import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
import random

class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
            
    @commands.command()
    async def acceptbug(self, ctx, userid, bug_number, *, description):
        if ctx.author.id == 447119084627427351:
            userid1 = int(userid)
            user = self.bot.get_user(userid1)
            await user.send(f'Your bug report {bug_number} has been approved!')
            channel = self.bot.get_channel(702605147402010654)
            embed = discord.Embed(title='AlternativeBot Bug Report', color=ctx.author.color, timestamp=ctx.message.created_at)
            embed.add_field(name='Description:', value=description)
            embed.add_field(name='Bug ID:', value=bug_number)
            embed.set_footer(text=f'Requested by {ctx.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
            await channel.send(embed=embed)
    

    @commands.command()
    async def declinebug(self, ctx, userid, bug_number):
        if ctx.author.id == 447119084627427351:
            userid1 = int(userid)
            user = self.bot.get_user(userid1)
            await user.send(f'Your bug report {bug_number} has been declined.')

    @commands.command()
    async def bugreport(self, ctx, *, description=None):
        bug_number = random.randint(0, 500)
        user = self.bot.get_user(447119084627427351)
        if description != None:
            await ctx.send(f'Your bug has been reported!')
            embed=discord.Embed(title='AlternativeBot Bug Report', color=ctx.author.color, timestamp=ctx.message.created_at)
            embed.add_field(name='Description:', value=description)
            embed.add_field(name='Reported By', value=ctx.author.mention)
            embed.add_field(name='Bug ID:', value=bug_number)
            embed.set_footer(text=f'Requested by {ctx.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await user.send(embed=embed)
        else:
            await ctx.send('**Bug report wizard**\n\nFollow the prompts and answer them!')
            await ctx.send('What\'s the description of the bug?')
            
            def check(message : discord.Message) -> bool:
                return message.author == ctx.author
            try:
                description = await self.bot.wait_for('message', timeout = 60, check=check)
            except asyncio.TimeoutError: 
                await ctx.send("You took too long to respond!")            
            else: 
                await ctx.send(f'''Your bug has been reported!''')
                embed=discord.Embed(title='AlternativeBot bug report', color=ctx.author.color, timestamp=ctx.message.created_at)
                embed.add_field(name='Description:', value=description.content)
                embed.add_field(name='Reported By', value=ctx.author.mention)
                embed.add_field(name='Bug ID:', value=bug_number)
                embed.set_footer(text=f'Requested by {ctx.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                await user.send(embed=embed)


    @commands.command() 
    async def membercount(self, ctx):
        await ctx.send(f'{ctx.guild.name} currently has {ctx.guild.member_count} members!')
        
    @commands.command()
    async def suggest(self, ctx, *, suggestion = None):
        user = self.bot.get_user(447119084627427351)
        if suggestion != None:
            await ctx.send(f'Thanks for your suggestion!')
            embed=discord.Embed(title='AlternativeBot Suggestion Form', color=ctx.author.color, timestamp=ctx.message.created_at)
            embed.add_field(name='Suggestion', value=suggestion)
            embed.add_field(name='Suggested by', value=ctx.author.mention)
            embed.set_footer(text=f'Requested by {ctx.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await user.send(embed=embed)
        else:
            await ctx.send('**Suggestion wizard**\n\nFollow the prompts and answer them!')
            await ctx.send('What would you like to suggest?')
        
            def check(message : discord.Message) -> bool:
                return message.author == ctx.author
            try:
                description = await self.bot.wait_for('message', timeout = 60, check=check)
            except asyncio.TimeoutError: 
                await ctx.send("You took too long to respond!")            
            else: 
                await ctx.send(f'Thanks for your suggestion!')
                embed=discord.Embed(title='AlternativeBot Suggestion Form', color=ctx.author.color, timestamp=ctx.message.created_at)
                embed.add_field(name='Suggestion', value=description.content)
                embed.add_field(name='Suggested by', value=ctx.author.mention)
                embed.set_footer(text=f'Requested by {ctx.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                await user.send(embed=embed)


    #ping command
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f":ping_pong: Pong! {round(self.bot.latency * 1000)}ms")
        
    #about command
    @commands.command()
    async def about(self, ctx):
        embed = discord.Embed(title="About the bot", colour=ctx.author.color)
        embed.add_field(name='Developer', value = "ThisIsanAlt#3043")
        embed.add_field(name='Server invite', value = 'https://discord.gg/33utPs9')
        embed.add_field(name='Programming Language and library', value="Python 3.8.5, discord.py version 1.5.0")
        embed.set_footer(text=f'Requested by {ctx.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
    
        await ctx.send (embed=embed)

    #whois command
    @commands.command()
    async def whois(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        if ctx.guild != None:
            roles = [role for role in member.roles]
            embed = discord.Embed (color=member.color, timestamp=ctx.message.created_at)
            embed.set_author(name=f'User info on {member}')
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f'Requested by {ctx.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
            embed.add_field(name='Discord ID:', value=member.id)
            if member.display_name == member.name:
                value1 = 'None'
            else:
                value1 = member.display_name
            embed.add_field(name='Nickname:', value=value1)
            embed.add_field(name='Created at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
            embed.add_field(name='Joined at:', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
            embed.add_field(name=f'Roles: ({len(roles)})', value=" ".join([role.mention for role in roles]))
            embed.add_field(name='Top Role:', value=member.top_role.mention)

            if member.bot:
                bot_status = 'Yes'
            else:
                bot_status = 'No'
            embed.add_field(name='Am I a bot:', value=bot_status)

            if member.premium_since != None:
                embed.add_field(name='Boosting since:', value=member.premium_since.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

            embed.add_field(name='Status:', value=member.status)
            await ctx.send(embed=embed)
        else:
            await ctx.send('You aren\'t in a guild at the moment. Try again in a guild.')       

    @commands.command()
    async def invite(self, ctx):
        await ctx.send ('The goods are on their way.', delete_after=3)
        await asyncio.sleep(3)
        await ctx.send('https://discord.gg/33utPs9')

def setup(bot):
    bot.add_cog(Meta(bot))