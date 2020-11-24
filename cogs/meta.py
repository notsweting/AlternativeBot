import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
import random

class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
     
    @commands.command()
    async def dev_update(self, ctx):
        await ctx.channel.purge(limit = 1)
        await ctx.send(f''' > **AlternativeBot Version 0.1.12**
    > 
    > **New stuff:**
    > - `/rockpaperscissors`is finally complete! Challenge all of your friends and **defeat them all.**
    > - `/mute` is done! Use `/bindmuterole` to automatically create a `Muted` role, or pass in your own role to use your own!
    > 
    > **In progress:**
    > - Channel and server-wide lock command
    ''')

    #help command
    @commands.cooldown(1, 3, BucketType.user)
    @commands.command(ignore_extra=True)
    async def help(self, ctx, info=None):
        if info == None:
            embed = discord.Embed(title="AlternativeBot Help and Documentation", description="Categories. Do /help [category] to get more info.\
            \nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
            embed.add_field(name='Fun', value='Some fun commands for you to use!')
            embed.add_field(name='Meta', value='Bot-related and user-related commands. Includes /whois, /about, and /bugreport.')
            embed.add_field(name='Moderation', value='These commands empower the moderation team. Rest assured, I won\'t do what the user can\'t.')
            embed.set_footer(text=f'(optional) [required] | Requested by {ctx.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
            await ctx.send (embed=embed, delete_after=60)
        elif info.lower()=='fun':
            embed = discord.Embed(title="AlternativeBot Help and Documentation", description="Here are some fun commands for you to use!\
            \nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
            embed.add_field(name="/8ball (question)", value="Ask the magic 8ball a question!")
            embed.add_field(name='/slap [person]', value='Slap someone.')
            embed.add_field(name='/hug [person]', value='Hug someone.')
            embed.add_field(name='/fight [person]', value='Fight someone.')
            embed.add_field(name='/rockpaperscissors [person] **BETA**', value='Challenge someone to a rock paper scissors challenge! \
            (Must have DMs open) **WARNING: Command is in beta and may not work as intended. Use /bugreport to report bugs.**')
            embed.set_footer(text=f'(optional) [required] | Requested by {ctx.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
            await ctx.send (embed=embed, delete_after=60)
        elif info.lower()=='meta':
            embed = discord.Embed(title="AlternativeBot Help and Documentation", description="Meta commands. Concerns more of the geeky side of the userbase.\
            \nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
            embed.add_field(name='/about', value='Get information about the bot!')
            embed.add_field(name="/ping", value="Check the ping of the bot to the Discord API.")    
            embed.add_field(name='/whois (person)', value='Get info on a member in the server.')
            embed.add_field(name= '/membercount', value='Get the amount of members in the server.')
            embed.add_field(name='/bugreport (description)', value='Report a bug!')    
            embed.add_field(name='~~/suggest (suggestion)~~', value='**Command is currently unavailable.** ~~Suggest something for the bot!~~')
            embed.set_footer(text=f'(optional) [required] | Requested by {ctx.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
            await ctx.send (embed=embed, delete_after=60)
        elif info.lower()=='mod' or info.lower()=='moderation':
            embed = discord.Embed(title="AlternativeBot Help and Documentation", description="Moderation commands.\nThis message will be deleted in 60 seconds.", colour=ctx.author.color)
            embed.add_field(name='/purge (no. of messages)', value='Purge messages. Number of messages defaults to 5. Requires manage messages permission.')
            embed.add_field(name="/kick [member] (reason)", value="Kick a member. Reason defaults to no reason. Requires kick members permission.")
            embed.add_field(name="/ban [member/user id] (reason)", value="Permanently ban a member. Reason defaults to no reason. Requires ban members permission.")
            embed.set_footer(text=f'(optional) [required] | Requested by {ctx.author} | Support: https://discord.gg/33utPs9', icon_url=ctx.author.avatar_url)
            await ctx.send (embed=embed, delete_after=60)
        else:
            await ctx.send('That\'s not a valid field!')
        
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
        bug_number = random.randint(0,500)
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

    @commands.guild_only()
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
    @commands.guild_only()
    @commands.command()
    async def whois(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
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
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        await ctx.send ('The goods are on their way.', delete_after=3)
        await asyncio.sleep(3)
        await ctx.send('https://discord.gg/33utPs9')
    
def setup(bot):
    bot.add_cog(Meta(bot))
    