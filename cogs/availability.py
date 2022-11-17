import asyncio
import discord

from cogs import BaseCog
from discord.ext import commands


class Availability(BaseCog):
    _cache = {"755071438419001409": True}
    _mm_cache = {}

    intervals = (
        ('years', 29030400),  # 60 * 60 * 24 * 7 * 4 * 12
        ('months', 2419200),  # 60 * 60 * 24 * 7 * 4
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),  # 60 * 60 * 24
        ('hours', 3600),  # 60 * 60
        ('minutes', 60),  # 1 * 60
        ('seconds', 1),
    )

    def convert_seconds(self, seconds):
        result = []

        for name, count in self.intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:10])

    @staticmethod
    async def convert_time(time):
        if time is None:
            return None

        pos = ["s", "m", "h", "d", "w"]

        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

        unit = time[-1]

        if unit not in pos:
            return None
        try:
            val = int(time[:-1])
        except:
            return None

        return val * time_dict[unit]

    @commands.check_any(
        commands.is_owner(),
        commands.has_role('Giveaway Manager'),
        commands.has_permissions(manage_channels=True),
        commands.has_permissions(manage_guild=True)
    )
    @commands.command(name='available')
    @commands.max_concurrency(10, commands.BucketType.guild)
    async def available(self, ctx, *, time=None):
        time = await self.convert_time(time)

        if time is None:
            return await ctx.send(embed=await self.error(description='Invalid time provided!'))

        if str(ctx.author.id) in self._cache:
            return await ctx.send(embed=await self.error(description='You are already marked as an available manager '
                                                                     'lol'))

        _time = self.convert_seconds(time)

        self._cache[str(ctx.author.id)] = True

        await ctx.send(ctx.author.mention, embed=await self.create_embed(title='Ok!', description=f'You will be '
                                                                                                  f'marked as '
                                                                                                  f'available for the '
                                                                                                  f'next {_time} (or) '
                                                                                                  f'until you go '
                                                                                                  f'offline. If you '
                                                                                                  f'are invisible, '
                                                                                                  f'this will not '
                                                                                                  f'work.',
                                                                         colour=discord.Colour.green()))

        for x in range(int(time / 10)):
            if str(ctx.author.id) not in self._cache:
                return

            if hasattr(ctx.author, 'status'):
                if str(ctx.author.status) == 'offline':
                    self._cache.pop(str(ctx.author.id))
                    return

            await asyncio.sleep(10)

        self._cache.pop(str(ctx.author.id))

    @available.error
    async def available_error(self, ctx, error):
        if isinstance(error, commands.MaxConcurrencyReached):
            return await ctx.send(embed=await self.create_embed(description='There are already enough giveaway '
                                                                            'managers available right now. Please '
                                                                            'check back later.'))

        await self.log_error(ctx, error)

    @commands.check_any(
        commands.is_owner(),
        commands.has_role('Giveaway Manager'),
        commands.has_permissions(manage_channels=True),
        commands.has_permissions(manage_guild=True)
    )
    @commands.command(name='unavailable')
    async def unavailable(self, ctx):
        if str(ctx.author.id) not in self._cache:
            return await ctx.send(embed=await self.error(description='You are not marked as an available manager lol'))

        self._cache.pop(str(ctx.author.id))

        return await ctx.send(embed=await self.create_embed(title='Ok!', description='You are now marked as '
                                                                                     'unavailable.', ))

    @unavailable.error
    async def unavailable_error(self, ctx, error):
        await self.log_error(ctx, error)

    @commands.command(name='managers', aliases=['available-managers', 'gaw', 'gaw-managers'])
    async def manager(self, ctx):
        if self._cache == {}:
            return await ctx.send(embed=await self.error(description='There are currently no available giveaway '
                                                                     'managers. You can always ping any Farmers '
                                                                     'daughter to host your giveaway. Check the pins '
                                                                     'for more information regarding this.'))

        em = await self.create_embed(title='Available gaw managers', description='These are the available gaw '
                                                                                 'managers:\n',
                                     colour=discord.Colour.green())

        for x in self._cache:
            em.description += f'<@!{x}>\n'

        return await ctx.send(embed=em)

    @manager.error
    async def manager_error(self, ctx, error):
        await self.log_error(ctx, error)

    @commands.check_any(
        commands.is_owner(),
        commands.has_role('Giveaway Manager'),
        commands.has_role('Heist Leader'),
        commands.has_role('Farm Hand - Chat Moderator'),
        commands.has_permissions(manage_channels=True),
        commands.has_permissions(mention_everyone=True),
        commands.has_permissions(manage_guild=True)
    )
    @commands.command(name='mm-available')
    @commands.max_concurrency(15, commands.BucketType.guild)
    async def mm_available(self, ctx, *, time=None):
        time = await self.convert_time(time)

        if time is None:
            return await ctx.send(embed=await self.error(description='Invalid time provided!'))

        if str(ctx.author.id) in self._mm_cache:
            return await ctx.send(embed=await self.error(description='You are already marked as an available middleman '
                                                                     'lol'))

        _time = self.convert_seconds(time)

        self._mm_cache[str(ctx.author.id)] = True

        await ctx.send(ctx.author.mention, embed=await self.create_embed(title='Ok!', description=f'You will be '
                                                                                                  f'marked as '
                                                                                                  f'available for the '
                                                                                                  f'next {_time} (or) '
                                                                                                  f'until you go '
                                                                                                  f'offline. If you '
                                                                                                  f'are invisible, '
                                                                                                  f'this will not '
                                                                                                  f'work.',
                                                                         colour=discord.Colour.green()))

        for x in range(int(time / 10)):
            if str(ctx.author.id) not in self._mm_cache:
                return

            if hasattr(ctx.author, 'status'):
                if str(ctx.author.status) == 'offline':
                    self._mm_cache.pop(str(ctx.author.id))
                    return

            await asyncio.sleep(10)

        self._mm_cache.pop(str(ctx.author.id))

    @mm_available.error
    async def mm_available_error(self, ctx, error):
        if isinstance(error, commands.MaxConcurrencyReached):
            return await ctx.send(embed=await self.create_embed(description='There are already enough middle mans '
                                                                            'available right now. Please '
                                                                            'check back later.'))

        await self.log_error(ctx, error)

    @commands.check_any(
        commands.is_owner(),
        commands.has_role('Giveaway Manager'),
        commands.has_role('Heist Leader'),
        commands.has_role('Farm Hand - Chat Moderator'),
        commands.has_permissions(manage_channels=True),
        commands.has_permissions(mention_everyone=True),
        commands.has_permissions(manage_guild=True)
    )
    @commands.command(name='mm-unavailable')
    async def mm_unavailable(self, ctx):
        if str(ctx.author.id) not in self._mm_cache:
            return await ctx.send(embed=await self.error(description='You are not marked as an available mm lol'))

        self._mm_cache.pop(str(ctx.author.id))

        return await ctx.send(embed=await self.create_embed(title='Ok!', description='You are now marked as '
                                                                                     'unavailable.', ))

    @mm_unavailable.error
    async def mm_unavailable_error(self, ctx, error):
        await self.log_error(ctx, error)

    @commands.command(name='middle-man', aliases=['mm', 'available-mm', 'middle-mans'])
    async def mm(self, ctx):
        if self._mm_cache == {}:
            return await ctx.send(embed=await self.error(description='There are currently no available middle '
                                                                     'mans. You can DM <@!855270214656065556> to '
                                                                     'find a middle man for your trade.'))

        em = await self.create_embed(title='Available Middle Mans', description='These are the available middle'
                                                                                'mans:\n',
                                     colour=discord.Colour.green())

        for x in self._mm_cache:
            em.description += f'<@!{x}>\n'

        return await ctx.send(embed=em)

    @mm.error
    async def mm_error(self, ctx, error):
        await self.log_error(ctx, error)


def setup(bot):
    bot.add_cog(Availability(bot))
