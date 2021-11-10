from actions import DO_NOTHING, push
import hardcoded
import random


class StateMachine:
    def __init__(self, env):
        self.env = env

    def run(self):
        info = push(self.env, DO_NOTHING)
        gotStarter = False

        while gotStarter == False or info["pkmn1HP"] >= 0:
            info = push(self.env, DO_NOTHING)

            # TODO: add branch for picking gender and for picking name

            if not gotStarter:
                hardcoded.menu_to_bedroom(self.env)
                hardcoded.get_item_from_PC(self.env)
                hardcoded.leave_bedroom(self.env)
                hardcoded.say_hi_to_mom_on_the_way_out(self.env)
                hardcoded.get_up_until_picking_starter(self.env)

                starterPos = random.randint(1, 3)
                if starterPos == 1:
                    hardcoded.pick_left_starter(self.env)
                elif starterPos == 2:
                    hardcoded.pick_mid_starter(self.env)
                else:
                    hardcoded.pick_right_starter(self.env)
                gotStarter = True

            if info["isInBattle"]:
                if info["isInWildPkmnBattle"]:
                    hardcoded.run_from_wild_pkmn(self.env)
                else:
                    # TODO: Add in any sort of logic for what to do here instead of mashing A
                    info = hardcoded.mash_A(self.env)

            if info["hasDialog"]:
                # It's probably fine to mash A whenever you see dialog, right?
                info = hardcoded.mash_A(self.env)

        push(self.env, DO_NOTHING)
        push(self.env, DO_NOTHING)
        push(self.env, DO_NOTHING)
