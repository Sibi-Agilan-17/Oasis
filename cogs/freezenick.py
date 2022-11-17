import asyncio
import discord
import json

from cogs import BaseCog
from discord.ext import commands, tasks
from cogs import is_owner


class FreezeNick(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

        self.main.start()

    @tasks.loop(seconds=0.1)
    async def main(self):
        with open('./cogs/fn_data.json', 'r') as f:
            data = json.load(f)

        g = await self.bot.fetch_guild(645753561329696785)

        if not self.bot.is_ready():
            await self.bot.wait_until_ready()

        for guild in self.bot.guilds:
            if guild.id == 645753561329696785:
                g = guild
                break

        for k, v in data.items():
            user = await g.fetch_member(int(k))
            try:
                await user.edit(nick=str(v))
            except discord.Forbidden:
                await self.bot.get_user(750245670761529346).send(f'Could not freeze nick of {user.id}')
            except AttributeError:
                pass

    @commands.check_any(is_owner(), commands.has_permissions(manage_nicknames=True))
    @commands.command(name='freeze-nick', aliases=['freezenick', 'fn'])
    async def fn(self, ctx, member: discord.Member, *, nick):
        if member is None:
            return await ctx.send(
                embed=await self.error(description='Please provide a valid member lol\nExample: `s!freeze-nick @user`'))

        await member.edit(nick=nick[:31])

        with open('./cogs/fn_data.json', 'r') as f:
            data = json.load(f)

        data[str(member.id)] = nick[:31]

        with open('./cogs/fn_data.json', 'w') as f:
            json.dump(data, f)

        return await ctx.send(':white_check_mark: Done')

    @commands.check_any(is_owner(), commands.has_permissions(manage_nicknames=True))
    @commands.command(name='un-freeze-nick', aliases=['unfreezenick', 'ufn'])
    async def ufn(self, ctx, member: discord.Member):
        if member is None:
            return await ctx.send(
                embed=await self.error(description='Please provide a valid member lol\nExample: `s!freeze-nick @user`'))

        with open('./cogs/fn_data.json', 'r') as f:
            data = json.load(f)

        data.pop(str(member.id))

        with open('./cogs/fn_data.json', 'w') as f:
            json.dump(data, f)

        return await ctx.send(':white_check_mark: Done')


def setup(bot):
    bot.add_cog(FreezeNick(bot))
