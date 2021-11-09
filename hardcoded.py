from actions import (
    DO_NOTHING,
    PRESS_UP,
    PRESS_DOWN,
    PRESS_LEFT,
    PRESS_RIGHT,
    PRESS_A,
    PRESS_B,
    PRESS_START,
    PER_MOVE,
    push,
    tap,
)
import constants


def menu_to_bedroom(env):
    # TODO: Break out the selection of gender, name, and rival name
    # so that the names are not just AAAAAAAA every time.
    info = push(env, DO_NOTHING)
    while info["mapLocation"] != constants.BEDROOM_MAP_NUM:
        info = tap(env, PRESS_A)


def get_item_from_PC(env):
    info = {}
    while info == {} or info["xPos"] < 5 * PER_MOVE or info["yPos"] < 4 * PER_MOVE:
        info = push(env, PRESS_LEFT)
        info = push(env, PRESS_UP)

    push(env, PRESS_A, numSteps=7)
    push(env, PRESS_B, numSteps=5)

    # Show Item
    # make_move(env, DO_NOTHING)
    # make_move(env, PRESS_START)
    # make_move(env, PRESS_A)
    # make_move(env, DO_NOTHING)


def leave_bedroom(env):
    push(env, PRESS_DOWN)
    push(env, PRESS_RIGHT, numSteps=6)
    push(env, PRESS_DOWN)
    push(env, PRESS_RIGHT, numSteps=3)
    push(env, PRESS_UP, numSteps=2)
    push(env, PRESS_LEFT)


def say_hi_to_mom_on_the_way_out(env):
    push(env, PRESS_LEFT)
    push(env, PRESS_DOWN, numSteps=2)
    push(env, PRESS_LEFT)
    info = push(env, PRESS_A)
    while info["hasDialog"]:
        info = push(env, PRESS_A)
    push(env, PRESS_DOWN, numSteps=4)
    push(env, PRESS_LEFT, numSteps=5)
    push(env, PRESS_DOWN)


def get_up_until_picking_starter(env):
    # Walk to the right until just before the mailbox
    info = push(env, PRESS_RIGHT, numSteps=7)

    # Walk up to trigger Oak into saving us
    info = push(env, PRESS_UP, numSteps=8)

    # Follow him to the lab by continuing through dialog
    while info["xPos"] != 0 and info["yPos"] != 8 * PER_MOVE:
        if info["hasDialog"] == 1:
            info = push(env, PRESS_A)
        if info["hasDialog"] == 0:
            info = push(env, DO_NOTHING)

    # Wait until he's done talking for a few "nothing" inputs in a row
    nothingInputs = 0
    while nothingInputs < 6:
        if info["hasDialog"] == 1:
            info = push(env, PRESS_A)
            nothingInputs = 0
        if info["hasDialog"] == 0:
            info = push(env, DO_NOTHING)
            nothingInputs += 1
    push(env, PRESS_DOWN)
    push(env, PRESS_DOWN)
    push(env, PRESS_RIGHT)
