import os
import json
import constants

substructureOrderByPersonalityMod = {
    "00": "GAEM",
    "01": "GAME",
    "02": "GEAM",
    "03": "GEMA",
    "04": "GMAE",
    "05": "GMEA",
    "06": "AGEM",
    "07": "AGME",
    "08": "AEGM",
    "09": "AEMG",
    "10": "AMGE",
    "11": "AMEG",
    "12": "EGAM",
    "13": "EGMA",
    "14": "EAGM",
    "15": "EAMG",
    "16": "EMGA",
    "17": "EMAG",
    "18": "MGAE",
    "19": "MGEA",
    "20": "MAGE",
    "21": "MAEG",
    "22": "MEGA",
    "23": "MEAG",
}


def loadG(obj, key, offset):
    return


def loadA(obj, key, offset):
    return


def loadM(obj, key, offset):
    return


def loadE(obj, key, offset):
    return


substructureToLoader = {"G": loadG, "A": loadA, "M": loadM, "E": loadE}

dataAddresses = {
    "enemy_pkmn_1_data": 33701964,
    "enemy_pkmn_2_data": 33702064,
    "enemy_pkmn_3_data": 33702164,
    "enemy_pkmn_4_data": 33702264,
    "enemy_pkmn_5_data": 33702364,
    "enemy_pkmn_6_data": 33702464,
    "pkmn_1_data": 33702564,
    "pkmn_2_data": 33702664,
    "pkmn_3_data": 33702764,
    "pkmn_4_data": 33702864,
    "pkmn_5_data": 33702964,
    "pkmn_6_data": 33703064,
}


def augment_data_json(info):
    map_block_addr = info["map_block_address"]
    trainer_block_addr = info["trainer_block_address"]

    temp_file_path = os.path.join(constants.SCRIPT_DIR, "data_temp.json")

    with open(os.path.join(constants.SCRIPT_DIR, "data.json"), "r") as data_file:
        with open(temp_file_path, "w+") as temp_file:
            # If temp already exists, clear the contents
            temp_file.truncate(0)

            data = json.load(data_file)
            temp = data

            make_map_data(temp, map_block_addr)
            make_trainer_data(temp, trainer_block_addr)

            # TODO: once substructure decryption is complete, uncomment this
            # make_pokemon_data(temp, info)

            json.dump(temp, temp_file)

            return temp_file_path


def make_map_data(obj, addr):
    obj["info"]["x_pos"] = {"address": constants.X_POS_SHIFT(addr), "type": "<i2"}

    obj["info"]["y_pos"] = {"address": constants.Y_POS_SHIFT(addr), "type": "<i2"}

    obj["info"]["current_map"] = {"address": constants.CURRENT_MAP(addr), "type": "<i1"}

    obj["info"]["curernt_map_bank"] = {
        "address": constants.CURRENT_MAP_BANK(addr),
        "type": "<i1",
    }


def make_trainer_data(obj, addr):
    obj["info"]["character_name"] = {
        "address": constants.CHARACTER_NAME(addr),
        "type": ">u8",
    }

    obj["info"]["gender"] = {"address": constants.GENDER(addr), "type": "<u1"}

    obj["info"]["trainer_id"] = {"address": constants.TRAINER_ID(addr), "type": "<u2"}

    obj["info"]["secret_id"] = {"address": constants.SECRET_ID(addr), "type": "<u2"}

    obj["info"]["options"] = {"address": constants.OPTIONS(addr), "type": "<u2"}


# TODO: unencrypt the data returned by this via https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_substructures_(Generation_III)
def make_pokemon_data(obj, info):
    for trainer in range(2):
        prefix = ""
        if trainer == 0:
            prefix = "enemy_"

        for pkmn_index in range(6):
            key = prefix + "pkmn_" + str(pkmn_index + 1)

            personality = info[key + "_personality_value"]
            substructureOrder = "{:02d}".format(personality % 24)

            # One of G, A, M, or E
            for i in range(substructureOrder.split().length):
                # Every substructure is 12 bytes long, so increment by 12 * 1-indexed substructure
                offset = dataAddresses[key + "_data"] + 12 * (i + 1)

                part = substructureOrder[i]
                substructureToLoader[part](obj, key, offset)
