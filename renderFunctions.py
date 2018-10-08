from enum import Enum

import libtcodpy as libtcod

class renderOrder(Enum):
    CORPSE = 1
    ITEM   = 2
    ACTOR  = 3

def renderAll(con, entities, player, gameMap, fovMap, fovRecompute, 
    screenWidth, screenHeight, colors):
    # Draw tiles in the gameMap
    if fovRecompute:
        for y in range(gameMap.height):
            for x in range(gameMap.width):
                visible = libtcod.map_is_in_fov(fovMap, x, y)
                wall = gameMap.tiles[x][y].blockSight

                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y,
                            colors.get('lightWall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y,
                            colors.get('lightGround'), libtcod.BKGND_SET)

                    gameMap.tiles[x][y].explored = True

                elif gameMap.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y,
                            colors.get('darkWall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y,
                            colors.get('darkGround'), libtcod.BKGND_SET)

    # Draw entities in the list
    entities_in_order = sorted(entities,key=lambda x: x.render_order.value)

    for entity in entities_in_order:
        drawEntity(con, entity, fovMap)

    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.console_print_ex(con, 1, screenHeight-2, libtcod.BKGND_NONE,
        libtcod.LEFT, 'HP: {0:02}/{1:02}'.format(player.stats.HP,
            player.stats.maxHP))

    libtcod.console_blit(con, 0,0, screenWidth, screenHeight, 0,0,0)

def clearAll(con, entities):
    for entity in entities:
        clearEntity(con,entity)

def drawEntity(con, entity, fovMap):
    if libtcod.map_is_in_fov(fovMap, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con,entity.x,entity.y,entity.char,
            libtcod.BKGND_NONE)

def clearEntity(con, entity):
    # erase the char that represents the object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
