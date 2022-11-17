from .items import Collectable


class CommonGem(Collectable):
    __name__ = 'Common Gem'

    def __init__(self):
        super().__init__(
            name='Common Gem',
            description='The common gem posses the power to do nothing!?? Since this is way too common, it is called a Common Gem'
        )
        self.buy_price = 100


class UncommonGem(Collectable):
    __name__ = 'UnCommon Gem'

    def __init__(self):
        super().__init__(
            name='Uncommon Gem',
            description='The opposite of Common Gem. A little uncommon than the common gem.'
        )
        self.buy_price = 1000


class RareGem(Collectable):
    __name__ = 'Rare Gem'

    def __init__(self):
        super().__init__(
            name='Rare Gem',
            description='The rare gem is pretty rare, even though some players have thousands of them.'
        )
        self.buy_price = 10000


class EpicGem(Collectable):
    __name__ = 'Epic Gem'

    def __init__(self):
        super().__init__(
            name='Epic Gem',
            description='The epic gem possess the power of epicness, which could be useful sometimes!'
        )
        self.buy_price = 100000


class GoldenGem(Collectable):
    __name__ = 'Golden Gem'

    def __init__(self):
        super().__init__(
            name='Golden Gem',
            description='The rare golden gem is made of pure gold! Buy it if you can!'
        )
        self.buy_price = 1000000


class DiamondGem(Collectable):
    __name__ = 'Diamond Gem'

    def __init__(self):
        super().__init__(
            name='Diamond Gem',
            description='The super rare diamond gem is never found by the average player! It is owned only by the '
                        'richest of the richest of the richest of the rich! '
        )
        self.buy_price = 10000000


class LegendaryGem(Collectable):
    __name__ = 'Legendary Gem'

    def __init__(self):
        super().__init__(
            name='Legendary Gem',
            description='The legendary gem has been in the hands of only the legends of the bot!')
        self.buy_price = 1000000000


common_gem = CommonGem()
uncommon_gem = UncommonGem()
rare_gem = RareGem()
epic_gem = EpicGem()
golden_gem = GoldenGem()
diamond_gem = DiamondGem()
legendary_gem = LegendaryGem()
