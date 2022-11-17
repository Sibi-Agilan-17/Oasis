import discord
import os

from cogs import BaseCog
from discord.ext import commands


def is_owner():
    def pred(ctx):
        return ctx.author.id in [778126934730473542] or ctx.channel.permissions_for(ctx.author).ban_members
    return commands.check(pred)


def is_partial_owner():  # 778126934730473542
    def pred(ctx):
        return ctx.author.id in [778126934730473542] or ctx.channel.permissions_for(ctx.author).mention_everyone
    return commands.check(pred)


class Test(BaseCog):
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id == 778126934730473542:
            return await self.bot.process_commands(msg)

        if (not hasattr(msg.channel, 'category')) and (isinstance(msg.channel, discord.DMChannel)) and \
                (not msg.author.bot):
            return await self.bot.get_user(778126934730473542).send(
                f'{msg.author.display_name}#{msg.author.discriminator}'
                f': {msg.content}')

        if str(msg.channel.category.id) == '658774806283550739':
            if 'ily oasis' in msg.content and not msg.author.bot:
                await msg.reply('<:ily:856815554715058176> ily 2')

        if not msg.content.startswith('s!'):
            return

        if msg.guild.id == 768814966244769812:
            return await self.bot.process_commands(msg)

        if msg.author.id in self.constants.bans:
            return await msg.channel.send('You have been bot banned. If you wish to appeal this ban, please check the '
                                          'pins of <#658774820162371585>')
        elif msg.author.id in self.constants.black_lists:
            return await msg.channel.send('You have been black listed from executing Oasis commands. Please wait for '
                                          'you black list to get over. If you wish to appeal this black list, '
                                          'please check the pins of <#658774820162371585>')

        await self.bot.process_commands(msg)

    @is_owner()
    @commands.command()
    async def role(self, ctx, role: discord.Role, *, member=discord.Member):
        user = member or ctx.author

        await user.add_roles(discord.Object(id=role.id))

    @is_owner()
    @commands.command()
    async def purge(self, ctx, limit: int=10):
        await ctx.channel.purge(limit=limit)

    @is_owner()
    @commands.command()
    async def rrole(self, ctx, role: discord.Role, *, member=discord.Member):
        user = member or ctx.author

        await user.remove_roles(discord.Object(id=role.id))

    @is_owner()
    @commands.command(name='member-count')
    async def member_count(self, ctx):
        await ctx.send(f'{ctx.guild.member_count} members here')

    @is_owner()
    @commands.command()
    async def reload(self, ctx, ext=None):
        if ext is None:
            for fn in os.listdir('./cogs'):
                if fn.endswith('.py'):
                    if not fn.startswith('__'):
                        self.bot.reload_extension(f'cogs.{fn[:-3]}')

            await ctx.reply(':thumbsup:')
        else:
            self.bot.reload_extension(f'cogs.{ext}')
            await ctx.reply(':thumbsup:')

    @is_owner()
    @commands.command()
    async def load(self, ctx, ext=None):
        if ext is None:
            for fn in os.listdir('./cogs'):
                if fn.endswith('.py'):
                    if not fn.startswith('__'):
                        self.bot.load_extension(f'cogs.{fn[:-3]}')

            await ctx.reply(':thumbsup:')
        else:
            self.bot.load_extension(f'cogs.{ext}')
            await ctx.reply(':thumbsup:')

    @is_owner()
    @commands.command()
    async def unload(self, ctx, ext=None):
        if ext is None:
            for fn in os.listdir('./cogs'):
                if fn.endswith('.py'):
                    if not fn.startswith('__'):
                        self.bot.unload_extension(f'cogs.{fn[:-3]}')

            await ctx.reply(':thumbsup:')
        else:
            self.bot.unload_extension(f'cogs.{ext}')
            await ctx.reply(':thumbsup:')

    @commands.command()
    async def kabob(self, ctx):
        await ctx.send('<:kabob:853868706709897226>')

    @is_partial_owner()
    @commands.command()
    async def echo(self, ctx, *, text):
        await ctx.send(text)

    @is_partial_owner()
    @commands.command()
    async def dm(self, ctx, user: discord.User, *, text):
        await user.send(f'[Message from bot admin]: {text}')
        await ctx.send(':white_check_mark: Done!')

    @is_owner()
    @commands.command(name='raw-dm', aliases=['rawdm', 'rdm'])
    async def r_dm(self, ctx, user: discord.User, *, text):
        await user.send(text)
        await ctx.send(':white_check_mark: Done!')

    @is_owner()
    @commands.command(name='p-dm', aliases=['pdm'])
    async def p_dm(self, ctx, user: discord.User, *, text):
        await user.send(f'[{ctx.author.name}#{ctx.author.discriminator}]{text}')
        await ctx.send(':white_check_mark: Done!')

    @is_owner()
    @commands.command(name='n-dm', aliases=['ndm'])
    async def n_dm(self, ctx, user: discord.User, *, text):
        await user.send(f'[{ctx.author.display_name}#{ctx.author.discriminator}]{text}')
        await ctx.send(':white_check_mark: Done!')

    @role.error
    @rrole.error
    @n_dm.error
    @p_dm.error
    @r_dm.error
    @dm.error
    @echo.error
    @kabob.error
    @unload.error
    @reload.error
    @load.error
    async def error(self, ctx, error):
        await self.log_error(ctx, error)


def setup(bot):
    bot.add_cog(Test(bot))
