import json
from discord import Member

booster = 649658625224343554
double_booster = 732497481358770186
quad_booster = 733838986992156752
satellite_supporter = 800799561174089758
gay = 714361456371564585
farm_supporter = 753210431983583302
thot_farm_member = 746828738150400140
staff_roles = [
    790290355631292467,
    723035638357819432,
    855877108055015465,
    814004142796046408,
    682698693472026749,
    658770981816500234,
    663162896158556212

]
top_dmc = 794393331773865994
server_boss = 820294120621867049
muted = 718993225263874090
elite_member = 830194009473024060
level_25 = 719012715204444181
level_30 = 719315435601788978
level_50 = 719012710062358560
level_69 = 732799368066760714
level_75 = 719012703812845699
level_100 = 719012692609728533
level_200 = 735315266568978463

role_100 = 794295747800465428
role_250 = 794295625365192704
role_500 = 820295774927323156
role_1000 = 820295730601918494
role_2500 = 820295144788066375


async def multiplier_calculator(user: Member):
    """Multipliers
    ---------------

    The latest set of multipliers are as follows:
    1. Booster: +10% | Double Booster: +20% | Quad Booster: +30%
    2. Satellite Supporter: +15%
    3. 69% Gay: +15%
    4. Farm supporter: +25%
    5. Thot Farm Member: +15%
    6. In Bot Farm for 1 year+: +30%
    7. Account age 1 year+: +5%
    8. Top DMC donator: +150%
    9. Server boss: +50%
    10. Elite Bot Farm Member: +25%
    11. Muted: -50%
    12. Level 25: +25%
    13. Level 30: +30%
    14. Level 50: +50%
    15. Level 69: +69%
    16. Level 75: +75%
    17. Level 100: +100%
    18. Level 200: +200%
    19. 100b+ cash: +5%
    20. Partner manager / Heist leader / Giveaway manager: +25% for each role
    21. Farm hand: +30%
    22. Farmer's daughter: +50%
    23. Farmer: +100%
    24. Server admin: +250%
    25. `oasis` in nick name: +100%
    26. 100m DMC donator: 10%
    27. 250m DMC donator: 25%
    28. 500m DMC donator: 50%
    29. 1b DMC donator: 100%
    30. 2.5b DMC donator: 250%
    """
    current_multiplier = 0

    with open('./cogs/economy_folder/economy.json', 'r') as f:
        data = json.load(f)

    try:
        multi = data[str(user.id)]['prestige']
    except KeyError:
        p_multi = 0
    else:
        p_multi = (multi * 50) if multi > 0 else 0

    try:
        dgem = data[str(user.id)]['inventory']['diamond_gem']
    except KeyError:
        d_multi = 0
    else:
        d_multi = (dgem * 25) if dgem > 0 else 0

    current_multiplier += 300 if d_multi > 300 else d_multi
    current_multiplier += 500 if p_multi > 500 else p_multi

    for role in user.roles:
        current_multiplier += 10 if role.id == booster else 0
        current_multiplier += 10 if role.id == double_booster else 0
        current_multiplier += 10 if role.id == quad_booster else 0
        current_multiplier += 15 if role.id == satellite_supporter else 0
        current_multiplier += 15 if role.id == gay else 0
        current_multiplier += 25 if role.id == farm_supporter else 0
        current_multiplier += 15 if role.id == thot_farm_member else 0
        current_multiplier += 30 if 'year' in user.joined_at.strftime("%m/%d/%Y, %H:%M:%S") else 0
        current_multiplier += 5 if 'year' in user.created_at.strftime("%m/%d/%Y, %H:%M:%S") else 0
        current_multiplier += 150 if role.id == top_dmc else 0
        current_multiplier += 50 if role.id == server_boss else 0
        current_multiplier += 25 if role.id == elite_member else 0
        current_multiplier -= 50 if role.id == muted else 0
        current_multiplier += 25 if role.id == level_25 else 0
        current_multiplier += 30 if role.id == level_30 else 0
        current_multiplier += 50 if role.id == level_50 else 0
        current_multiplier += 69 if role.id == level_69 else 0
        current_multiplier += 75 if role.id == level_75 else 0
        current_multiplier += 100 if role.id == level_100 else 0
        current_multiplier += 200 if role.id == level_200 else 0
        current_multiplier += 25 if role.id == staff_roles[0] else 0
        current_multiplier += 25 if role.id == staff_roles[1] else 0
        current_multiplier += 25 if role.id == staff_roles[2] else 0
        current_multiplier += 30 if role.id == staff_roles[3] else 0
        current_multiplier += 50 if role.id == staff_roles[4] else 0
        current_multiplier += 100 if role.id == staff_roles[5] else 0
        current_multiplier += 250 if role.id == staff_roles[6] else 0
        current_multiplier += 10 if role.id == role_100 else 0
        current_multiplier += 25 if role.id == role_250 else 0
        current_multiplier += 50 if role.id == role_500 else 0
        current_multiplier += 100 if role.id == role_1000 else 0
        current_multiplier += 250 if role.id == role_2500 else 0
        current_multiplier += 1000 if role.id == 864075477245624331 else 0

    current_multiplier += 100 if 'oasis' in user.display_name.lower() else 0
    return 1000 if current_multiplier > 1000 else current_multiplier
