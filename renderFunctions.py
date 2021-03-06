import libtcodpy as libtcod

from enum       import Enum
from gameStates import gameStates
from menus      import inventoryMenu

# Sets order of rendering
class renderOrder(Enum):
    CORPSE = 1
    ITEM   = 2
    ACTOR  = 3

# Hover-over Mouse
def getNamesUnderMouse(mouse, entities, fovMap):
    (x, y) = (mouse.cx, mouse.cy)

    # gets the names of everything at location of mouse IF in FOV
    names = [entity.name for entity in entities
        if entity.x == x and entity.y == y and
        libtcod.map_is_in_fov(fovMap, entity.x, entity.y)]

    # joins all the names and returns them
    names = ', '.join(names)
    return names.capitalize()

# Renders UI Components
def renderUI(panel, x, y, totalWidth, name, value, maximum, barColor,
    backColor):
    # computes the bar width with respect to total bar size
    barWidth = int(float(value)/maximum*totalWidth)

    # set up the bar's background UI
    libtcod.console_set_default_background(panel, backColor)
    libtcod.console_rect(panel, x, y, totalWidth, 1, False,
        libtcod.BKGND_SCREEN)

    # set up the actual bar's UI
    libtcod.console_set_default_background(panel, barColor)
    if barWidth > 0:
        libtcod.console_rect(panel, x, y, barWidth, 1, False,
            libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x+totalWidth/2), y,
        libtcod.BKGND_NONE, libtcod.CENTER,
        '{0}: {1}/{2}'.format(name, value, maximum))

def renderAll(con, panel, entities, player, gameMap, fovMap, 
    fovRecompute, msg_log, screenWidth, screenHeight, barWidth,
    panelHeight, panelDiff, mouse, colors, gameState):
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

    libtcod.console_blit(con, 0,0, screenWidth, screenHeight, 0,0,0)

    # render the UI bars i.e. HP, mana, stamina, etc.
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # print game messages @ 1 line / turn
    y = 1
    for message in msg_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, msg_log.x, y,
            libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    renderUI(panel, 1, 1, barWidth, 'HP', player.stats.HP,
        player.stats.maxHP, libtcod.darker_red, libtcod.darker_gray)

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE,
        libtcod.LEFT, getNamesUnderMouse(mouse, entities, fovMap))

    libtcod.console_blit(panel, 0, 0, screenWidth, panelHeight, 0, 0,
        panelDiff)

    if gameState in (gameStates.SHOW_INVENTORY, gameStates.DROP_INVENTORY):
        if gameState == gameStates.SHOW_INVENTORY:
            inventoryTitle = 'Press the key to use an item or ESC to cancel.\n'
        else:
            inventoryTitle = 'Press the key to drop an item or ESC to cancel.\n'

        inventoryMenu(con,inventoryTitle,player.inventory,50,screenWidth,screenHeight)

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
