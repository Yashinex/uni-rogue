import libtcodpy as libtcod

from gameStates         import gameStates
from renderFunctions    import renderOrder

def killPlayer(player):
    player.char  = '#'
    player.color = libtcod.white

    return 'You are dead.', gameStates.PLAYER_DEAD

def killMonster(monster):
    deathMessage = '{0} has died.'.format(monster.name.capitalize())

    monster.char        = '%'
    monster.color       = libtcod.dark_red
    monster.blocks      = False
    monster.stats       = None
    monster.ai          = None
    monster.name        = monster.name + 'remains'
    monster.renderOrder = renderOrder.CORPSE

    return deathMessage
