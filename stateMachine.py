import actions
import constants
from dynamicRam import augment_data_json
import hardcoded
import random


class StateMachine:
    def __init__(self, env):
        self.env = env

    def run(self):
        # Start with all the hardcoded parts where the inputs do not vary from game to game
        info = actions.push(self.env, actions.DO_NOTHING)

        hardcoded.menu_to_bedroom(self.env)
        hardcoded.get_item_from_PC(self.env)
        hardcoded.leave_bedroom(self.env)
        hardcoded.say_hi_to_mom_on_the_way_out(self.env)
        hardcoded.get_up_until_picking_starter(self.env)

        starterPos = random.randint(1, 3)
        if starterPos == 1:
            info = hardcoded.pick_left_starter(self.env)
        elif starterPos == 2:
            info = hardcoded.pick_mid_starter(self.env)
        else:
            info = hardcoded.pick_right_starter(self.env)

        prevMapBlockAddress = ""
        prevTrainerBlockAddress = ""

        retrievedOakPackage = False
        havePokedex = False
        havePotionFromMartEmployee = False

        # The way to tell whether we are allowed to keep playing is whether our pokemon has lost all of its health or not
        while info["pkmn_1_current_hp"] != 0:
            info = actions.push(self.env, actions.DO_NOTHING)

            # Reload data json with dynamic RAM values augmented into the original as necessary
            if (
                prevMapBlockAddress != info["map_block_address"]
                or prevTrainerBlockAddress != info["trainer_block_address"]
            ):
                self.env.data.load(
                    augment_data_json(info),
                    None,
                )
                info = actions.push(self.env, actions.DO_NOTHING)
                prevMapBlockAddress = info["map_block_address"]
                prevTrainerBlockAddress = info["trainer_block_address"]

            # Begin actual state machine. Are we in a battle or not?
            if info["is_in_battle"]:
                # For now, we assume our starter is good enough, so all wild pokemon fights are just for running away
                if info["is_in_wild_pkmn_battle"]:
                    info = hardcoded.run_from_wild_pkmn(self.env)
                elif info["has_dialog"]:
                    # It's probably fine to mash B whenever you see dialog, right?
                    info = actions.mash_B(self.env)
                else:
                    # TODO: Add in any sort of logic for what to do here instead of mashing A
                    info = actions.mash_A(self.env)

            # Overworld. Where do we need to go next?
            else:
                # Rough outline of StateMachine flowchart:

                # Do we need to go to a pokemon center?
                # Are we allowed to go to a pokemon center (see rules about dungeons)?
                # Are we avoiding trainers or not?
                # Do we need to get into a fight so that we can use an item on our main?

                # What's the next badge that we need?
                # What's the next key item that we need?

                # If we need the Pewter badge:
                # Pallet Town -> Viridian Forest

                # Pallet Town Outside of Oak Lab -> Pallet Town North Entrance
                # Pallet Town North Entrance -> Viridian City South Entrance
                # Do we have the potion from the mart employee?

                # Viridian City South Entrance -> Viridian City Mart
                # hardcoded "talk to mart employee"
                # hardcoded "exit mart"
                # Viridian City Mart -> Viridian City South Entrance
                # Viridian City South Entrance -> Pallet Town North Entrance
                # Pallet Town North Entrance -> Oak Lab

                # Oak's Lab
                if info["current_map"] == constants.OAK_LAB_MAP_NUM:
                    if retrievedOakPackage:
                        # Approach Oak
                        actions.navigate_within_room(
                            self.env, info["x_pos"], info["y_pos"], 6, 0
                        )
                    else:
                        # Leave the lab
                        actions.navigate_within_room(
                            self.env, info["x_pos"], info["y_pos"], 6, 12
                        )
                        actions.mash_DOWN(self.env)

                # Viridian Forest -> End of Viridian Forest

                # End of Viridian Forest -> Rival Battle 2

                # Rival Battle 2 -> Brock

                # Brock -> End of Mt. Moon

                elif info["has_dialog"]:
                    # It's probably fine to mash B whenever you see dialog, right?
                    info = actions.mash_B(self.env)
