import retro
import os
import hardcoded
from actions import DO_NOTHING, push
import constants

IS_RANDOMIZED = False


def main():
    retro.data.Integrations.add_custom_path(
        os.path.join(constants.SCRIPT_DIR, "custom_integrations")
    )

    gameFolder = "FireRed-GbAdvance"
    if IS_RANDOMIZED:
        gameFolder += "Randomizer"

    env = retro.make(
        gameFolder,
        state="start_screen",
        inttype=retro.data.Integrations.ALL,
        use_restricted_actions=retro.Actions.ALL,
        info=os.path.join(constants.SCRIPT_DIR, "data.json"),
    )
    env.reset()
    env.step(DO_NOTHING)

    hardcoded.menu_to_bedroom(env)
    hardcoded.get_item_from_PC(env)
    hardcoded.leave_bedroom(env)
    hardcoded.say_hi_to_mom_on_the_way_out(env)
    hardcoded.get_up_until_picking_starter(env)

    push(env, DO_NOTHING)
    push(env, DO_NOTHING)
    push(env, DO_NOTHING)

    env.render(close=True)


if __name__ == "__main__":
    main()
