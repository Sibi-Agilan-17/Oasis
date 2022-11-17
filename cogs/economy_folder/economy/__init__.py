def economy_setup(bot):
    from .balance import bal
    from .multi import multi
    from .add_coins import add_coins
    from .level import level
    from .bet import bet
    from .shop import shop
    from .buy import buy
    from .inv import inv
    from .prestige import prestige
    from .share import share

    bal(bot)
    multi(bot)
    add_coins(bot)
    level(bot)
    bet(bot)
    shop(bot)
    buy(bot)
    inv(bot)
    prestige(bot)
    share(bot)
