import json

# Because the pokemon memory blocks are just repeating the same rough shape, this
# script was made to help generate those memory addresses more quickly and easily.
def main():
    # From https://datacrystal.romhacking.net/wiki/Pok%C3%A9mon_FireRed_and_LeafGreen:RAM_map
    startVal = 33701932

    data = {}

    attributes = [
        {"name": "Personality value", "size": "=u4", "offset": 0},
        {"name": "OT ID", "size": "=u4", "offset": 4},
        {"name": "Nickname", "size": "=u10", "offset": 8},
        {"name": "Language", "size": "=u2", "offset": 18},
        {"name": "OT name", "size": "=u7", "offset": 20},
        {"name": "Markings", "size": "=u1", "offset": 27},
        {"name": "Checksum", "size": "=u2", "offset": 28},
        {"name": "????", "size": "=u2", "offset": 30},
        {"name": "Data", "size": "=u48", "offset": 32},
        {"name": "Status condition", "size": "=u4", "offset": 80},
        {"name": "Level", "size": "=u1", "offset": 84},
        {"name": "Pokerus remaining", "size": "=u1", "offset": 85},
        {"name": "Current HP", "size": "=u2", "offset": 86},
        {"name": "Total HP", "size": "=u2", "offset": 88},
        {"name": "Attack", "size": "=u2", "offset": 90},
        {"name": "Defense", "size": "=u2", "offset": 92},
        {"name": "Speed", "size": "=u2", "offset": 94},
        {"name": "Sp Atk", "size": "=u2", "offset": 96},
        {"name": "Sp Def", "size": "=u2", "offset": 98},
    ]

    for trainer in range(2):
        prefix = ""
        enemyOffset = 0
        if trainer == 0:
            prefix = "enemy_"
        else:
            # There are 6 enemy pokemon, each of which are 100 bytes long
            enemyOffset = 600

        for pkmn_index in range(6):
            for attribute in attributes:
                key = (
                    prefix
                    + "pkmn_"
                    + str(pkmn_index + 1)
                    + "_"
                    + str.join("_", attribute["name"].lower().split(" "))
                )

                value = startVal + (
                    pkmn_index * 100 + enemyOffset + attribute["offset"]
                )
                size = attribute["size"]
                data[key] = {
                    "address": value,
                    "type": size,
                }

    print(json.dumps(data, indent=2))


main()
