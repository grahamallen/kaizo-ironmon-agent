# Kazio-Ironmon-Agent
An autonomous expert agent written in Python3 for playing Pokemon Fire Red with [additional difficulty rules](https://pastebin.com/L48bttfz).

## Background
### High Level Design
The goal of this repo is to create an agent which can play through from the beginning of the game to the Hall of Fame achieved after the Elite 4, using a complex [state machine](https://en.wikipedia.org/wiki/Finite-state_machine). The largest states in the state machine will consist of `Battle` and `Overworld`. Under each of these, we will have sub-states like `Poisoned` or `Paralyzed` or `Within Death Range` underneath `Battle` and sub-states like `Poisoned`, `Need To Go To Pokemon Center`, or `Ready For Next Gym` underneath `Overworld`. When reasoning is unnecessary, like at the very beginning of the game up until choosing a starter, the agent can be hardcoded with series of game inputs, rather than depending on the state machine to figure things out.

### Pathing
While it's possible to have the agent map out its surroundings programmatically, a lot of Pokemon game pathing can be completely hardcoded ahead of time. It's likely that there is a subset of paths that would take far less time, computing power, memory, etc to work with than an agent capable of exploration. By keeping track of potential entrances and exits (including via Flight/Surf/etc), we can build a [connected graph](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) where each node is a known place and each connection represents a hardcoded path to get from one place to another. For instance, after choosing a starter, the player must go from Oak's lab to the Viridian Mart. This can be done in a way that hardcodes the path to go through the least amount of grass. Along the way, there may be one-off events added to the hardcoded path (like talking to the mart employee who gives you a Potion) or full nodes added to the graph (like the top strip of grass at the top of Route 1, closest to Viridian City, as a potential place to try and find a new starter).

### Interface
This project uses [Gym Retro](https://retro.readthedocs.io/en/latest/python.html) to read memory directly from the ROM during play. Gym Retro is also used to perform the inputs needed to control the game. To know which memory addresses to read, I used the [Gym Retro Integration UI](https://retro.readthedocs.io/en/latest/integration.html#the-integration-ui). Note that the Gym Retro docs did not include a link to the actual Integration UI at the time that I began working on this project, so I had to use [this download link](https://github.com/openai/retro/releases/tag/f347d7e) instead.

To learn about which memory addresses corresponded to which game features, I looked at this community-defined RAM-map for [high-level memory mapping](https://datacrystal.romhacking.net/wiki/Pok%C3%A9mon_FireRed_and_LeafGreen:RAM_map) and Bulbapedia for resources on [Pokemon Data Structures](https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_(Generation_III)), [Pokemon Data Substructures](https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_substructures_(Generation_III)), and [Character Encoding/Decoding](https://bulbapedia.bulbagarden.net/wiki/Character_encoding_(Generation_III)).

## Kaizo Ironmon Resources
The [rules for Kaizo Ironmon](https://pastebin.com/L48bttfz) are online, and there is a [Kaizo Ironmon discord](https://discord.gg/8Ewwav8W54) for questions and further resources.

## Running the agent
### Prerequisits
#### ROM
To run the agent, you need to get a Pokemon FireRed ROM named `rom.gba` to be saved in `./custom_integrations/FireRed-GbAdvance`. Alternatively, you can save `rom.gba` in `./custom_integrations/FireRed-GbAdvanceRandomizer` if you're doing a randomized run, but make sure to flip the `IS_RANDOMIZED` flag to `True` in `main.py`. 

#### ROM state file
To run the agent, you also need to save a state file using the Gym Retro Integration UI called `start_screen.state`. It doesn't matter exactly where on the start screen, so long as you have not yet pressed start.

#### Python 3
You'll need a version of Python 3 installed that is compatible with [Gym Retro](https://retro.readthedocs.io/en/latest/index.html). Make sure that Python is added to your PATH as well.

### Once prerequisits are met
Run the script by navigating to the repo's folder and then running
```
python main.py
```

## Developing new functionality
### File structure
#### `data.json`
This is where the definition of static memory address locations goes so that the Gym Retro environment can properly extract the memory values that we have defined and bind those values to our variable names. For instance, once the player is loaded into the bedroom, the Gym Retro environment variable (env) will return an `info` struct which contains properties like `has_dialog` and `map_number` because those are the key names for those properties in `data.json`

#### `actions.py`
The way that gym retro handles sending GBA inputs into the ROM while it's running is by using an `actions` array. Based on the configuration we use to load the ROM, and given that we're playing on an emulated GBA, there are 12 possible inputs in the `actions` array. 10 of these inputs correspond to actual GBA buttons: `up`, `down`, `left`, `right`, `a`, `b`, `start`, `select`. The remaining 2 actions do seemingly nothing. For convenience, I have added hardcoded `actions` arrays for each of the 10 button inputs and 1 for doing nothing. It's possible to have multiple button inputs in a given `actions` array, which would consist of boolean `OR`-ing together multiple actions into a new combination.

This file also contains the helper functions for `push`ing buttons (a longer button press) and `tap`ping buttons (a short button press). These methods try to account for the animation delays associated with moving and/or turning by doing a bunch of `DO_NOTHING` actions after the action's animation begins.

This file is where higher-order input functions will live. For example, `navigate_within_room` allows us to tell the game to go to make our current x and y position match a goal x and y, with the most naive linear pathing possible.

#### `constants.py`
This file contains all non-action-related constants like map locations or the directory location the files are running in. In the future, this could be a place to add an in-memory cache of things like statistics for various attacks, total stats (BST) per Pokemon, Pokemon typings, favorable type matchups, etc.

#### `hardcoded.py`
For bits of the game which are always the same, we can hardcode them in this file. Already, there are functions for handling inputs from the beginning of the game through the point where the starter is chosen.

#### `stateMachine.py`
This is where the state machine lives. Inside of a giant while loop that checks the end condition of the run (our main dying), we branch off into other (mostly hardcoded for now) steps to handle getting from the beginning of the game up until the rival fight. After winning the rival fight, the state machine becomes grossly more complicated, so for now we just have it mash the A button whenever it doesn't know what to do.

#### `dynamicRam.py`
Because of some of the memory addresses change as the player enters buildings or gets a pokemon, we need to be able to load these dynamically in some way. Gym Retro allows us to specificy a `data.json` file, which we do on startup, but in order to get the dynamic values to be correct too, we need to reload the memory address map json file each time an event happens that would cause the dynamic addresses to change (i.e. entering/exiting a building, changing main pokemon, etc). We augment the values in `data.json` using the functions in `dynamicRam.py` and then store the new values in `data_temp.json`, which is what later gets loaded during execution into Gym Retro.

#### `setupPkmnJson.py`
Since so much of the memory addrresses that we need to load are repetitive things like the pokemon data structures for the player or an enemy trainer for each of up to six pokemon, this file contains a script for generating the static data structures in a way that can be copied over to `data.json`. At this point, it should no longer be necessary, but it seemed like it couldn't hurt to commit just in case.

#### `logic.py`
For now, this is the place where any code around "what is the best action for our situation" should go. This would be where to put a function for `determining gender or name`, for `deciding which move to use against a given enemy`, or for `deciding whether to try to switch main pokemon` would go.

#### `main.py`
This is currently where the hardcoded functions are invoked. Ideally, this would be a very simple file which sets up the ROM environment object and then passes it off to a state machine to handle everything else.

### Future Goals
- [ ] Be able to read item names in the bag
- [ ] Be able to read starter pokemon name, stat breakdown, moves
- [ ] Be able to read opponent's pokemon name and keep track of moves
- [ ] Map out overworld movement to first trainer in Viridian Forest, while picking up all items along the way and running from any wild pokemon
- [ ] Handle `poisoned` condition in overworld, including using the potion if absolutely necessary
- [ ] Map out Viridian Forest trainer battles
- [ ] Map out path to Rival fight
- [ ] Map out path to Pewter Gym