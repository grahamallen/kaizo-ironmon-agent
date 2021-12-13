from actions import (
    DO_NOTHING,
    PRESS_UP,
    PRESS_DOWN,
    PRESS_LEFT,
    PRESS_RIGHT,
    PRESS_A,
    PRESS_B,
    PRESS_START,
    push,
    tap,
)
import constants


def menu_to_bedroom(env):
    # TODO: Break out the selection of gender, name, and rival name
    # so that the names are not just AAAAAAAA every time.
    info = push(env, DO_NOTHING)

    while info["map_number"] == constants.BEGINNING_MENU_MAP_NUM:
        info = tap(env, PRESS_A)
    return info


def get_item_from_PC(env):
    push(env, PRESS_LEFT, numSteps=2)
    push(env, PRESS_UP, numSteps=4)
    push(env, PRESS_LEFT, numSteps=4)
    push(env, PRESS_UP)
    push(env, PRESS_A, numSteps=7)
    return push(env, PRESS_B, numSteps=5)


def leave_bedroom(env):
    push(env, PRESS_DOWN)
    push(env, PRESS_RIGHT, numSteps=6)
    push(env, PRESS_DOWN)
    push(env, PRESS_RIGHT, numSteps=3)
    push(env, PRESS_UP, numSteps=2)
    return push(env, PRESS_LEFT)


def say_hi_to_mom_on_the_way_out(env):
    push(env, PRESS_LEFT)
    push(env, PRESS_DOWN, numSteps=2)
    push(env, PRESS_LEFT)
    info = push(env, PRESS_A)
    while info["has_dialog"]:
        info = push(env, PRESS_A)
    push(env, PRESS_DOWN, numSteps=4)
    push(env, PRESS_LEFT, numSteps=5)
    return push(env, PRESS_DOWN)


def get_up_until_picking_starter(env):
    # Walk to the right until just before the mailbox
    info = push(env, PRESS_RIGHT, numSteps=7)

    # Walk up to trigger Oak into saving us
    info = push(env, PRESS_UP, numSteps=8)

    # Follow him to the lab by continuing through dialog
    i = 0
    while i < 10:
        if info["has_dialog"] == 1:
            info = push(env, PRESS_A)
        else:
            info = push(env, DO_NOTHING)
            i += 1

    # Wait until he's done talking for a few "nothing" inputs in a row
    nothingInputs = 0
    while nothingInputs < 6:
        if info["has_dialog"] == 1:
            info = push(env, PRESS_A)
            nothingInputs = 0
        if info["has_dialog"] == 0:
            info = push(env, DO_NOTHING)
            nothingInputs += 1
    return info


def pick_left_starter(env):
    # Show off middle
    push(env, PRESS_DOWN)
    push(env, PRESS_RIGHT, numSteps=3)
    look_at_starter(env)

    # Show off right (opponent's pokemon)
    push(env, PRESS_RIGHT)
    look_at_starter(env)

    # Pick left (our pokemon)
    push(env, PRESS_LEFT, numSteps=2)
    pick_starter(env)

    return prepare_starter_for_battle(env)


def pick_mid_starter(env):
    # Show off right
    push(env, PRESS_DOWN)
    push(env, PRESS_RIGHT, numSteps=4)
    look_at_starter(env)

    # Show off left (opponent's pokemon)
    push(env, PRESS_LEFT, numSteps=2)
    look_at_starter(env)

    # Pick mid (our pokemon)
    push(env, PRESS_RIGHT)
    pick_starter(env)

    push(env, PRESS_LEFT)
    return prepare_starter_for_battle(env)


def pick_right_starter(env):
    # Show off left
    push(env, PRESS_DOWN)
    push(env, PRESS_RIGHT, numSteps=2)
    look_at_starter(env)

    # Show off mid (opponent's pokemon)
    push(env, PRESS_RIGHT)
    look_at_starter(env)

    # Pick right (our pokemon)
    push(env, PRESS_RIGHT)
    pick_starter(env)

    push(env, PRESS_LEFT, numSteps=2)
    return prepare_starter_for_battle(env)


def look_at_starter(env):
    tap(env, PRESS_UP)
    info = push(env, PRESS_A)
    while info["has_dialog"] == 1:
        info = push(env, PRESS_B)
    return info


def pick_starter(env):
    tap(env, PRESS_UP)
    info = push(env, PRESS_A)
    while info["has_dialog"] == 1:
        # TODO: break out naming portion to do something more interesting than AAAAAAAAA
        info = push(env, PRESS_A)

    # Wait for rival to talk about his pokemon
    nothingInputs = 0
    while nothingInputs < 3:
        if info["has_dialog"] == 1:
            info = push(env, PRESS_A)
            nothingInputs = 0
        if info["has_dialog"] == 0:
            info = push(env, DO_NOTHING)
            nothingInputs += 1

    push(env, PRESS_DOWN)
    return push(env, PRESS_LEFT)


def prepare_starter_for_battle(env):
    push(env, PRESS_DOWN)
    # Look up the starter
    info = push(env, PRESS_START)
    info = push(env, PRESS_A)
    while info["menu_index"] != 0:
        info = push(env, PRESS_A)

    # Look at the stats
    push(env, PRESS_A, numSteps=2)
    push(env, DO_NOTHING, numSteps=2)
    push(env, PRESS_RIGHT)
    push(env, DO_NOTHING, numSteps=2)
    push(env, PRESS_RIGHT)
    push(env, DO_NOTHING, numSteps=2)
    push(env, PRESS_B)

    # Remove held item
    push(env, PRESS_DOWN)
    push(env, PRESS_A)
    push(env, PRESS_DOWN)
    push(env, PRESS_A)
    info = push(env, PRESS_B, 4)

    # TODO: Look up what the held item was and consider adding it back if it's a berry
    # or using it if it's a ppup or ppmax
    return info


def run_from_wild_pkmn(env):
    push(env, PRESS_B, numSteps=3)
    push(env, PRESS_RIGHT)
    push(env, PRESS_DOWN)
    return push(env, PRESS_A)
