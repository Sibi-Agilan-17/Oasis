import discord
import json

from discord.ext import commands


exceptions = [commands.CheckFailure,
              commands.MissingPermissions,
              commands.MissingRole,
              commands.CheckAnyFailure,
              discord.NotFound,
              discord.Forbidden]


class BaseCog(commands.Cog):
    class constants:
        black_lists = []
        bans = []
        notifs_channel = discord.Object(id=794378435254157342)
        sale_item_channel = discord.Object(id=853845435273183253)
        sale_item_channel_bf = discord.Object(id=724437224036499517)

    def __init__(self, bot):
        self.bot = bot

    async def log_error(self, ctx, error):
        for e in exceptions:
            if isinstance(error, e):
                pass

        if isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id == 778126934730473542:
                return

            self.constants.bans.append(ctx.author.id)
            await self.bot.get_user(778126934730473542).send(
                f'Bot banning {ctx.author.id} for spamming'
            )
            return await ctx.author.send('You have been bot banned for spamming.')

        await self.bot.get_user(778126934730473542).send(
            embed=await self.create_embed(
                title='Another error reported',
                description=f'A command which was executed in {ctx.channel.name}({ctx.channel.mention}: {ctx.channel.id}) by {ctx.author.name}({ctx.author.mention}: {ctx.author.discriminator}) | Error: {error}',
                colour=discord.Colour.red()
            )
        )
        return await ctx.send(embed=await self.error(description=str(error)))

    @staticmethod
    async def create_embed(*, title='', description='', colour=discord.Colour.red(), footer=None):
        foot = 'This bot is developed by Sibi Agilan#8323' if footer is None else footer

        em = discord.Embed(title=title, description=description, colour=colour)
        em.set_footer(text=foot)

        return em

    async def error(self, *, title='Error!', description='', colour=discord.Colour.red(), footer='If you think this '
                                                                                                 'is a mistake, '
                                                                                                 'please contact Sibi '
                                                                                                 'Agilan#8323'):
        return await self.create_embed(title=title, description=description, colour=colour, footer=footer)


class DonationCog(BaseCog):
    @staticmethod
    async def get_all_donation_statistics():
        with open('./cogs/data.json', 'r') as f:
            data = json.load(f)

            return data

    async def fetch_all_donation_statistics(self):
        data = await self.get_all_donation_statistics()
        data_ = {}

        for k, v in data.items():
            data_[str(k)] = v['donated_amount']

        return data_

    async def fetch_donation_statistics(self, member):
        data = await self.get_all_donation_statistics()

        if hasattr(member, 'id'):
            _id = member.id
        else:
            _id = member

        if str(_id) not in data:
            return 0

        with open('./cogs/data.json', 'w') as f:
            json.dump(data, f)

        return data[str(_id)]['donated_amount']

    async def add_donation(self, member, amount: int):
        data = await self.get_all_donation_statistics()

        if hasattr(member, 'id'):
            _id = member.id
        else:
            _id = member

        if str(member) not in data:
            data[str(member)] = {'donated_amount': 0, 'heists_led': 0}

        data[str(member)]['donated_amount'] += amount

        with open('./cogs/data.json', 'w') as f:
            json.dump(data, f)


class HeistCog(BaseCog):
    @staticmethod
    async def get_all_heist_statistics():
        with open('./cogs/data.json', 'r') as f:
            data = json.load(f)

            return data

    async def fetch_all_heist_statistics(self):
        data = await self.get_all_heist_statistics()
        data_ = {}

        for k, v in data.items():
            data_[str(k)] = v['heists_led']

        try:
            return data_
        except KeyError:
            return 0

    async def fetch_heists_statistics(self, member):
        data = await self.get_all_heist_statistics()

        if hasattr(member, 'id'):
            _id = member.id
        else:
            _id = member

        if str(_id) not in data:
            data[str(_id)] = {'donated_amount': 0, 'heists_led': 0}

        with open('./cogs/data.json', 'w') as f:
            json.dump(data, f)

        try:
            return data[str(_id)]['heists_led']
        except KeyError:
            data[str(_id)]['heists_led'] = 0
            return 0

    async def add_heist(self, member, *, amount=1):
        data = await self.get_all_heist_statistics()

        _id = member.id

        if str(_id) not in data:
            data[str(_id)] = {'donated_amount': 0, 'heists_led': 0}

        try:
            data[str(_id)]['heists_led'] += amount
        except KeyError:
            data[str(_id)]['heists_led'] = amount

        with open('./cogs/data.json', 'w') as f:
            json.dump(data, f)

    async def remove_heist(self, member):
        return await self.add_heist(member, amount=-1)

    async def check_heists(self, member):
        return await self.fetch_heists_statistics(member)


class EconomyCog(BaseCog):
    @staticmethod
    async def get_all_economy_data():
        with open('./cogs/economy_folder/economy.json', 'r') as f:
            data = json.load(f)

        return data

    @staticmethod
    async def set_economy_data(data):
        with open('./cogs/economy_folder/economy.json', 'r') as f:
            _ = json.load(f)

        with open('./cogs/economy_folder/economy.json', 'w') as f:
            json.dump(data, f)

    async def set_economy_data_for(self, user, data):
        cdata = await self.get_all_economy_data()
        cdata[str(user.id)] = data

        await self.set_economy_data(cdata)

    async def add_coins(self, user, coins):
        try:
            data = await self.get_economy_data_for(user)
        except KeyError:
            await self.add_user_to_economy(user)
            data = await self.get_economy_data_for(user)

        data['balance'] += coins

        await self.set_economy_data_for(user, data)

    async def add_experience(self, ctx, user, exp):
        data = await self.get_economy_data_for(user)
        try:
            multi = data['inventory']['mystery_gem']
        except KeyError:
            multi = 1

        exp *= multi
        data['experience'] += exp

        c_exp = data['experience']

        if c_exp >= data['level'] * 100:
            data['level'] += 1
            lvl = data['level']

            await self.add_item(user, 'common_gem', int(lvl * 25))
            await self.add_item(user, 'uncommon_gem', int(lvl * 10))
            await self.add_item(user, 'rare_gem', int(lvl))

            await ctx.send(embed=await self.create_embed(
                title='Congrats!',
                description=f'Congrats on reaching level {data["level"]}, {user.display_name}!',
                colour=await self.get_economy_colour(user)
            ))

        await self.set_economy_data_for(user, data)

    async def add_user_to_economy(self, user):
        rdata = {
            'balance': 0,
            'level': 1,
            'experience': 0,
            'color': 'cyan',
            'prestige': 0,
            'inventory': {}
        }

        await self.set_economy_data_for(user, rdata)

    async def add_item(self, user, name, value):
        data = await self.get_economy_data_for(user)

        try:
            inv = data['inventory']
        except KeyError:
            data['inventory'] = {}
            data['prestige'] = 0

        try:
            data['inventory'][name] += value
        except KeyError:
            data['inventory'][name] = value

        await self.set_economy_data_for(user, data)

    async def get_economy_colour(self, user) -> discord.Colour:
        if user.id in [778126934730473542]:
            # return discord.Colour(0x11134d)
            pass

        data = await self.get_economy_data_for(user)

        try:
            color = data['color']
        except KeyError:
            return discord.Colour(0x34f1e7)  # cyan
        if color == 'cyan':
            return discord.Colour(0x34f1e7)  # cyan
        elif color == 'yellow':
            return discord.Colour(0xF8F714)  # yellow
        elif color == 'red':
            return discord.Colour(0xFF0000)  # red
        elif color == 'green':
            return discord.Colour(0x00FF00)  # green
        elif color == 'blue':
            return discord.Colour(0x0000FF)  # blue
        elif color == 'pink':
            return discord.Colour(0xFF00D9)  # pink
        elif color == 'black':
            return discord.Colour(0x000000)  # black

        return discord.Colour(0x11134d)

    async def get_economy_data_for(self, user):
        data = await self.get_all_economy_data()

        if str(user.id) not in data:
            await self.add_user_to_economy(user)
            return data[str(user.id)]
        else:
            return data[str(user.id)]

    async def get_balance_for(self, user):
        data = await self.get_economy_data_for(user)

        return data['balance']

    async def get_balance_as_embed(self, user):
        coins = str(await self.get_balance_for(user))

        return await self.create_embed(
            title=f'{user.name}\'s balance',
            description=f'**Coins: ** {int(coins[:1999]):,}',
            colour=await self.get_economy_colour(user)
        )

    async def get_level_as_embed(self, user):
        data = await self.get_economy_data_for(user)
        description = f'**Prestige {data["prestige"]}**\n\n'
        description += f'**Current level: ** {int(data["level"]):,}\n**Experience: ** {int(data["experience"]):,}\n\n'
        description += f'**Balance: ** {int(data["balance"]):,}'

        return await self.create_embed(
            title=f'{user.name}\'s level',
            description=description,
            colour=await self.get_economy_colour(user)
        )


def setup(bot):
    bot.add_cog(BaseCog(bot))


def is_owner():
    def pred(ctx):
        return ctx.author.id in [778126934730473542] or ctx.channel.permissions_for(ctx.author).ban_members
    return commands.check(pred)


def is_partial_owner():  # 778126934730473542
    def pred(ctx):
        return ctx.author.id in [778126934730473542] or ctx.channel.permissions_for(ctx.author).mention_everyone
    return commands.check(pred)
