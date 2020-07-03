import discord
from discord.ext import commands
#Moderation commands
#clear command
class Fun(commands.Cog):
    def __init__(self,client):
        self.client = client

    #ping command
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(client.latency * 1000)}ms")
    
    #8ball command
    @commands.command(aliases=["8ball"])
    async def _8ball (self, ctx, *, question):
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

    #coinflip command
    @commands.command()
    async def coinflip (self, ctx):
        responses = [":large_blue_diamond: Heads",
                     ":large_orange_diamond: Tails"]
        await ctx.send('Flipping.....')
        time.sleep(3)
        await ctx.channel.purge(limit=1)
        await ctx.send(f"{random.choice(responses)}")

    #slap command
    @commands.command()
    async def slap(self, ctx, member: discord.Member, *, reason,):
      await ctx.send (f'{ctx.author.mention} slapped {member.mention} {reason}')

    
def setup(client):
    client.add_cog(Fun(client))
