import discord


class Collectable:
    buy_price = 'Not purchasable'
    sell_price = 'Collectables are not sellable'

    def __init__(self,
                 name: str,
                 description: str):
        self.name = name
        self.description = description

    def __int__(self):
        return 0

    async def to_embed(self,
                       owned: str,
                       color: discord.Colour,
                       icon_url: str) -> discord.Embed:
        em = discord.Embed(
            title=f'{self.name.title()} ({owned} owned)',
            description=f'{self.description}\nBuy price: {self.buy_price}\nSell price: {self.sell_price}',
            color=color
        )
        em.set_image(url=icon_url)
        return em


class Buyable:
    def __init__(self,
                 name: str,
                 description: str,
                 buy_price: int,
                 sell_price: int):
        self.name = name
        self.description = description
        self.buy_price = buy_price
        self.sell_price = sell_price

    def __int__(self):
        return self.buy_price

    async def to_embed(self,
                       owned: str,
                       color: discord.Colour,
                       icon_url: str) -> discord.Embed:
        em = discord.Embed(
            title=f'{self.name.title()} ({owned} owned)',
            description=f'{self.description}\nBuy price: {self.buy_price}\nSell price: {self.sell_price}',
            color=color
        )
        em.set_image(url=icon_url)
        return em
