import libtcodpy as libtcod

from gameStates         import gameStates
from renderFunctions    import renderOrder
from gameMessages       import Message

def killPlayer(player):
    player.char  = '#'
    player.color = libtcod.white

    return Message('You are dead.', libtcod.red), gameStates.PLAYER_DEAD

def killMonster(monster):
    deathMessage = Message('{0} has died.'.format(monster.name.capitalize()),
        libtcod.yellow)

    monster.char        = '%'
    monster.color       = libtcod.dark_red
    monster.blocks      = False
    monster.stats       = None
    monster.ai          = None
    monster.name        = monster.name + 'remains'
    monster.renderOrder = renderOrder.CORPSE

    return deathMessage

