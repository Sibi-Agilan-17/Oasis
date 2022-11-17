import discord

from cogs import HeistCog
from discord.ext import commands


class Heists(HeistCog):
    @commands.check_any(
        commands.is_owner(),
        commands.has_role('Heist Leader'),
        commands.has_role('Heist Expert'),
        commands.has_permissions(mention_everyone=True)
    )
    @commands.command(name='heist-add')
    async def heist_add(self, ctx: commands.Context, member: discord.Member = None):
        user = member or ctx.author

        await self.add_heist(user)

        return await ctx.send(embed=discord.Embed(title='Added!',
                                                  description=f'Added a heist point to {user.mention}',
                                                  colour=discord.Colour.green()))

    @commands.check_any(
        commands.is_owner(),
        commands.has_role('Heist Leader'),
        commands.has_role('Heist Expert'),
        commands.has_permissions(mention_everyone=True)
    )
    @commands.command(name='heist-remove')
    async def heist_remove(self, ctx: commands.Context, member: discord.Member = None):
        user = member or ctx.author

        await self.remove_heist(user)

        return await ctx.send(embed=discord.Embed(title='Removed!',
                                                  description=f'Removed a heist point from {user.mention}',
                                                  colour=discord.Colour.red()))

    @commands.check_any(
        commands.is_owner(),
        commands.has_role('Heist Leader'),
        commands.has_role('Heist Expert'),
        commands.has_permissions(mention_everyone=True)
    )
    @commands.command(name='heist-check')
    async def heist_check(self, ctx: commands.Context, member: discord.Member = None):
        user = member or ctx.author

        heists = await self.check_heists(user)

        return await ctx.send(embed=discord.Embed(title=f'Heists led by {user.name}',
                                                  description=f'{user.mention} has led {heists:,} heists.',
                                                  colour=discord.Colour.green()))

    @heist_add.error
    @heist_remove.error
    @heist_check.error
    async def heist_error(self, ctx, error):
        await self.log_error(ctx, error)


def setup(bot):
    bot.add_cog(Heists(bot))
