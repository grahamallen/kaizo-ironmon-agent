import retro
import os
from actions import DO_NOTHING
import constants
import stateMachine

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

    sm = stateMachine.StateMachine(env)
    sm.run()

    env.render(close=True)

    # Delete the contents of our temp file to clean up
    with open(os.path.join(constants.SCRIPT_DIR, "data_temp.json"), "w") as f:
        f.truncate(0)


if __name__ == "__main__":
    main()
