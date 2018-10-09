import libtcodpy as libtcod

from gameStates import gameStates

def handleKeys(key, gameState):
    if gameState == gameStates.PLAYER_TURN:
        return handlePlayerTurnKeys(key)

    elif gameState == gameStates.PLAYER_DEAD:
        return handlePlayerDeadKeys(key)

    elif gameState in (gameStates.SHOW_INVENTORY,gameStates.DROP_INVENTORY):
        return handleInventoryKeys(key)

    return {}

def handleInventoryKeys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventoryIndex': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit menu
        return {'exit': True}

    return {}

def handlePlayerTurnKeys(key):
    key_char = chr(key.c)

    # Linear movement
    if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8 :
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
        return {'move': (1, 0)}
    
    # Diagonal movement
    elif key.vk == libtcod.KEY_KP7 or (key.vk == libtcod.KEY_UP 
        and key.vk == libtcod.KEY_LEFT):
        return {'move': (-1, -1)}
    elif key.vk == libtcod.KEY_KP9 or (key.vk == libtcod.KEY_UP 
        and key.vk == libtcod.KEY_RIGHT):
        return {'move': (1, -1)}
    elif key.vk == libtcod.KEY_KP1 or (key.vk == libtcod.KEY_DOWN
        and key.vk == libtcod.KEY_LEFT):
        return {'move': (-1, 1)}
    elif key.vk == libtcod.KEY_KP3 or (key.vk == libtcod.KEY_DOWN 
        and key.vk == libtcod.KEY_RIGHT):
        return {'move': (1, 1)}

    # User actions
    # grab item
    if key_char == 'g':
        return {'grab': True}

    # drop item
    if key_char == 'd':
        return {'drop': True}

    # check inventory
    elif key_char == 'i':
        return {'showInventory': True}

    # wait [TODO]
    elif key.vk == libtcod.KEY_KP5:
        return {'wait': (0,0)}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handlePlayerDeadKeys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'showInventory': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}
