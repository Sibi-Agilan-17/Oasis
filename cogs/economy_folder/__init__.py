def setup(bot):
    # from .games import games_setup
    from .economy import economy_setup

    # games_setup(bot)
    economy_setup(bot)
