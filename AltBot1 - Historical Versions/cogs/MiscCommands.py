import discord
from discord.ext import commands
#Misc
#clear command
class Misc(commands.Cog):
    def __init__(self,client):
        self.client = client

    #whois command
    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        roles = [role for role in member.roles]
        embed = discord.Embed (color=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f'User info on {member}')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name='Discord ID:', value=member.id)
        embed.add_field(name='Nickname:', value=member.display_name)

        embed.add_field(name='Created at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
        embed.add_field(name='Joined at:', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

        embed.add_field(
            name=f'Roles: ({len(roles)})',
            value=" ".join(role.mention for role in roles),
        )

        embed.add_field(name='Top Role:', value=member.top_role.mention)

        bot_status = 'Yes' if member.bot == True else 'No'
        embed.add_field(name='Am I a bot:', value=bot_status)

        await ctx.send(embed=embed)

    #about command
    @commands.command(aliases = ['info'])
    async def about (self, ctx):
        await ctx.send ('''Hey there, I\'m a bot created by ThisIsanAltYT#0117 for the server AltSquad!
    If you see this bot on another server other than`discord.gg/SUzSuTa`, please contact ThisIsanAltYT#0117!''')

       

def setup(client):
    client.add_cog(Misc(client))
