import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #8ball command
    @commands.command(aliases=["8ball"])
    async def _8ball (self, ctx, *, question = None):
        responses = ["It is certain.",
                    "It is decidedly so.",
                    "Without a doubt",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again later.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Dont count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."]
        await ctx.send(f"{random.choice(responses)}")

    #slap command
    @commands.command()
    async def slap(self, ctx, member):
        reasons = ['for being rude.',
        ' because why not.',
        ' for being incompetent.',
        ' for sleeping in class.',
        f', but {member} slapped him back!']
        await ctx.send (f'{ctx.author.mention} slapped {member}{random.choice(reasons)}')
    
    @commands.command()
    async def hug(self, ctx, member):
        reasons = ['for being nice.',
        f'because {ctx.author.mention} recieved a nice note from {member}.',
        'because why not?']
        await ctx.send (f'{ctx.author.mention} hugged {member} {random.choice(reasons)}')

    @commands.command()
    async def fight(self, ctx, member):
        reasons = [f'because {member} was mean.',
        f"because {member} stole {ctx.author.mention}'s phone.",
        f'for being fricked in the head.',]
        await ctx.send (f'{ctx.author.mention} fought {member} {random.choice(reasons)}')

    #coinflip command
    @commands.command()
    async def coinflip (self, ctx):
        responses = [":large_blue_diamond: Heads",
                    ":large_orange_diamond: Tails"]
        await ctx.send('Flipping.....')
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1)
        await ctx.send(f"{random.choice(responses)}")

    
    @commands.command()
    async def rockpaperscissors(self, ctx, member: discord.Member):
        await ctx.send('**This command is under construction. Report bugs with /reportbug.**')
        await ctx.send(f'{ctx.author.mention} has challenged {member.mention} to a rock paper scissors contest!')
        await ctx.send(f'To accept the challenge, {member.mention}, send `accept` to accept!')
        responses = ['rock', 'paper', 'scissors']
        def check(message : discord.Message) -> bool:
            return message.author == member and message.content == 'accept'

        def check1(message : discord.Message) -> bool:
            return message.author == member and message.content in responses
        
        def check2(message : discord.Message) -> bool:
            return message.author == ctx.author and message.content in responses
        try:
            message = await self.bot.wait_for('message', timeout = 60, check = check)
        except asyncio.TimeoutError: 
            await ctx.send(f"{member.mention} took too long to respond!")            
        else:
            await ctx.author.send(f'{member} accepted your challenge! Please use any of the following: `rock` `paper` `scissors` to select your choice!')
            await member.send(f'You accepted {ctx.author}\'s challenge! Please use any of the following: `rock` `paper` `scissors` to select your choice!')
        
        try:
            memberresponse = await self.bot.wait_for('message', timeout = 29, check = check2)
        except asyncio.TimeoutError: 
            await member.send(f"{ctx.author.name} took too long to respond!")            
        else:

            try:
                    authorresponse = await self.bot.wait_for('message', timeout = 29, check = check2)
            except asyncio.TimeoutError: 
                    await member.send(f"{ctx.author.name} took too long to respond!")            
            else:   
                
                if authorresponse == 'rock' and memberresponse == 'scissors':
                        await ctx.author.send(f'You won! {member.name} chose scissors')
                        await member.send(f'You lost. {ctx.author.name} chose rock.')
                elif authorresponse == 'scissors' and memberresponse == 'paper':
                        await ctx.author.send(f'You won! {member.name} chose {memberresponse}')
                        await member.send(f'You lost. {ctx.author.name} chose {authorresponse}.')
                elif authorresponse == 'paper' and memberresponse == 'rock':
                        await ctx.author.send(f'You won! {member.name} chose {memberresponse}')
                        await member.send(f'You lost. {ctx.author.name} chose {authorresponse}.')
                elif authorresponse == memberresponse:
                        await ctx.author.send(f'You tied! {member.name} chose {memberresponse}')
                        await member.send(f'You tied! {ctx.author.name} chose {authorresponse}')
                        await member.send(f'You won! {ctx.author.name} chose {authorresponse}')
                        await ctx.author.send(f'You lost. {member.name} chose {memberresponse}.')
                elif memberresponse == 'paper' and authorresponse == 'rock':
                        await member.send(f'You won! {ctx.author.name} chose {authorresponse}')
                        await ctx.author.send(f'You lost. {member.name} chose {memberresponse}.')
                elif memberresponse == 'scissors' and authorresponse == 'paper':
                        await member.send(f'You won! {ctx.author.name} chose {authorresponse}')
                        await ctx.author.send(f'You lost. {member.name} chose {memberresponse}.')
                else:
                        pass
            
            finally: 
                pass

def setup(bot):
    bot.add_cog(Fun(bot))