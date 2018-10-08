import libtcodpy as libtcod


def handleKeys(key):

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

    # wait
    elif key.vk == libtcod.KEY_KP5:
        print('You pause for a moment.')
        return {'move': (0,0)}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}
