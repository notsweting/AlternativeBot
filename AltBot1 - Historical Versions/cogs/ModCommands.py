import discord
from discord.ext import commands
#Moderation commands
#clear command
class Moderation(commands.Cog):
    def __init__(self,client):
        self.client = client

    #purge command
    @commands.command()
    async def purge(self, ctx, amount=5):
        if ctx.author.id not in mod_ids:
            await ctx.send('Hmmm.... :thinking: You don\'t have permission to use this command!')    
        else:
            await ctx.channel.purge(limit=amount+1)
            await ctx.send('Messages cleared.')

    #warn command
    @commands.command()
    async def warn (self, ctx, member, warnlevel):
        
        if ctx.author.id not in mod_ids:
            await ctx.send ('Hey you! You don\'t have permissions to use this command!')

        else:
            numwarnlevel = int(warnlevel)
            if numwarnlevel == '1':
                await member.add_roles(510852414111219712)
            elif numwarnlevel == '2':
                await member.add_roles(504023257880592404)
            elif numwarnlevel == '3':
                await member.add_roles(510852486333202454)
            elif numwarnlevel > 3:
                await ctx.send ('Error: There are only 3 warn levels. Please enter a number from 1 to 3, otherwise manually add the role.')

        mod_ids=[447119084627427351,
            318068014899527691,
            511561638785056771,
            382634433771208725,
            513798090071736320,
            448280112207626241,
            315249559473225729,
            552235268342677529,
            486186037702426625,
            510397521554833409,
            534851751531249674,
            473835913907142656]

    
def setup(client):
    client.add_cog(Moderation(client))
