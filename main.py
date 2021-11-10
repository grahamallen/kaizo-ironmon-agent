import retro
import os
import hardcoded
from actions import DO_NOTHING, push
import constants
import stateMachine

IS_RANDOMIZED = True


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


if __name__ == "__main__":
    main()
