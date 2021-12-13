# Possible Singular Actions (combo actions like running not listed here)
DO_NOTHING = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
PRESS_RIGHT = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
PRESS_LEFT = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
PRESS_UP = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
PRESS_DOWN = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
PRESS_START = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
PRESS_SELECT = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
PRESS_A = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
PRESS_B = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
PRESS_L = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
PRESS_R = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

# `push` inputs an action several times so that the character actually performs the input as expected in the game.
# For navigating menus, or having the character turn without moving, consider using `tap`
def push(env, action, numSteps=1, shouldRun=True):
    info = {}

    # TODO: handle being able to run. Running seems to take different number of frames
    # depending on whether the character was already running or not, which makes timing trickier
    # than simply uncommenting the below code
    # if (
    #     action == PRESS_UP
    #     or action == PRESS_DOWN
    #     or action == PRESS_LEFT
    #     or action == PRESS_RIGHT
    # ) and shouldRun:
    #     action = OR(action, PRESS_B)

    for _ in range(numSteps):
        for _ in range(10):
            _, _, _, info = env.step(action)
            env.render()

        # print("loc: " + str(info["mapLocation"]))
        # print("x: " + str(info["xPos"]) + " | y: " + str(info["yPos"]))

        for _ in range(100):
            _, _, _, info = env.step(DO_NOTHING)
            env.render()

    return info


# `tap` allows the character to only hit a given button one time, which is useful for
#  changing direction in place or for menuing
def tap(env, action):
    info = {}
    _, _, _, info = env.step(action)
    env.render()
    _, _, _, info = env.step(DO_NOTHING)
    env.render()

    return info


# Mapping movement in this game can generally be completely hardcoded by mapping out
# individually walkable paths and then stringing them together. This function naively
# walks towards a spot by walking directly in a line towards it.
#
# Since the position changes as you enter/exit buildings, this is only to be used for
# navigating within a given room.
def navigate_within_room(env, x=1, y=1, x_goal=1, y_goal=1):
    if x > x_goal:
        push(env, PRESS_LEFT)
    elif x < x_goal:
        push(env, PRESS_RIGHT)

    if y > y_goal:
        push(env, PRESS_UP)
    elif y < y_goal:
        push(env, PRESS_DOWN)


def mash_DOWN(env):
    return push(env, PRESS_DOWN)


def mash_A(env):
    return push(env, PRESS_A, numSteps=5)


def mash_B(env):
    return push(env, PRESS_B, numSteps=5)


# `OR` provides a logical OR of all entries in the two provided actions
# Assumes that actions are the same length
def OR(action1, action2):
    action = []
    for i in range(len(action1)):
        if action1[i] == 1 or action2[i] == 1:
            action.append(1)
        else:
            action.append(0)
    return action
