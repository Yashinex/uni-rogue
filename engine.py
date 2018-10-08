import libtcodpy as libtcod

from entity                 import Entity, getBlockingEntitiesAtLocation
from inputHandlers          import handleKeys
from renderFunctions        import clearAll, renderAll, renderOrder
from mapObjects.gameMap     import gameMap
from fovFunctions           import initializeFOV, recomputeFOV
from gameStates             import gameStates
from components.stats       import stats
from deathFunctions         import killPlayer, killMonster
from gameMessages           import Message, messageLog
from components.inventory   import Inventory

def main():
    # screen size
    screenWidth  = 80
    screenHeight = 80

    # ui elements
    barWidth       = 20
    panelHeight    = 7
    panelDiff      = screenHeight - panelHeight

    # message log
    messageX       = barWidth + 2
    messageWidth   = screenWidth - barWidth - 2
    messageHeight  = panelHeight - 1

    # map size
    mapWidth  = 80
    mapHeight = 58

    # room parameters
    roomMaxSize = 14
    roomMinSize = 6
    maxRooms    = 30

    # monsters
    maxMonstersRoom = 4

    # items
    maxItemsRoom = 2

    # object colors dictionary
    colors = {
        'darkWall'      : libtcod.Color(50, 50, 50),
        'darkGround'    : libtcod.Color(25, 25, 25),
        'lightWall'     : libtcod.Color(100, 100, 100),
        'lightGround'   : libtcod.Color(200, 200, 200),
        'whiteWall'     : libtcod.Color(255, 255, 255)
    }

    # player stats, location, symbol, and color
    playerStats = stats(HP=40,DEF=2,STR=5)
    invStorage  = Inventory(28)
    player      = Entity(0, 0, '@', libtcod.red, 'Player', blocks=True,
        render_order = renderOrder.ACTOR, stats=playerStats)
    
    # npc list; location, symbol, color

    entities = [player]

    # game font
    libtcod.console_set_custom_font('arial10x10.png', 
        libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screenWidth, screenHeight,
        'libtcod tutorial revised', False)

    # creates windows [DO NOT DELETE]
    # console window
    con     = libtcod.console_new(screenWidth,screenHeight)
    # panel window, holds HP and message log
    panel   = libtcod.console_new(screenWidth, panelHeight)

    # creates the game map and initializes its attributes
    game_map = gameMap(mapWidth, mapHeight)
    game_map.makeMap(maxRooms, roomMinSize, roomMaxSize, mapWidth, mapHeight,
        player, entities, maxMonstersRoom, maxItemsRoom)

    # field of view
    fov_algorithm   = 0
    fov_light_walls = True
    fov_radius      = 10
    fov_recompute   = True
    fov_map         = initializeFOV(game_map)

    # message log
    msg_log = messageLog(messageX, messageWidth, messageHeight)

    # mouse, keyboard init
    key   = libtcod.Key()
    mouse = libtcod.Mouse()

    # sets game to player's turn
    gameState = gameStates.PLAYER_TURN
    previousState = gameState

    # game loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE,
            key, mouse)

        if fov_recompute:
            recomputeFOV(fov_map,player.x,player.y,fov_radius,fov_light_walls,
            fov_algorithm)

        # [DO NOT DELETE] renders entities each frame
        renderAll(con, panel, entities, player, game_map, fov_map, 
            fov_recompute, msg_log, screenWidth, screenHeight, barWidth,
            panelHeight, panelDiff, mouse, colors, gameState)

        fov_recompute = False

        # [DO NOT DELETE] refreshes each frame
        libtcod.console_flush()

        # [DO NOT DELETE] clears each frame
        clearAll(con, entities)

        # each turn processes player input
        action = handleKeys(key, gameState)

        # assigns input to an action
        move     = action.get('move')
        wait     = action.get('wait')
        grab     = action.get('grab')
        show     = action.get('showInventory')
        drop     = action.get('drop')
        invIndex = action.get('inventoryIndex')
        exit     = action.get('exit')
        fullscreen = action.get('fullscreen')

        playerTurnResults = []

        # character movement check
        if move and gameState == gameStates.PLAYER_TURN:
            dx, dy = move
            destX = player.x + dx
            destY = player.y + dy

            if not game_map.isBlocked(destX, destY):
                target = getBlockingEntitiesAtLocation(entities,destX,destY)

                if target:
                    attackResults = player.stats.attack(target)
                    playerTurnResults.extend(attackResults)

                else:
                    player.move(dx, dy)

                    fov_recompute = True

                gameState = gameStates.ENEMY_TURN

        # character grab item check
        elif grab and gameState == gameStates.PLAYER_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    grab = player.inventory.addItem(entity)
                    playerTurnResults.extend(grab)

                    break

                else:
                    msg_log.addMessage(Message('There\'s nothing here to pick up.', libtcod.yellow))

        # character inventory check
        if show:
            previousState = gameState
            gameState = gameStates.SHOW_INVENTORY

        # character drop check
        if drop:
            previousState = gameState
            gameState = gameStates.DROP_INVENTORY

        # inventory screen check
        if invIndex is not None and previousState != gameStates.PLAYER_DEAD and invIndex < len(player.inventory.items):
            item = player.inventory.items[invIndex]
            playerTurnResults.extend(player.inventory.use(item))

            if gameState == gameStates.SHOW_INVENTORY:
                playerTurnResults.extend(player.inventory.use(item))

            elif gameState == gameStates.DROP_INVENTORY:
                playerTurnResults.extend(player.inventory.dropItem(item))

        # exit from inputHandlers
        if exit:
            if gameState in (gameStates.SHOW_INVENTORY, gameStates.DROP_INVENTORY):
                gameState = previousState
            else:
                return True

        # fullscreen check
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for playerTurnResult in playerTurnResults:
            message     = playerTurnResult.get('message')
            deadEntity  = playerTurnResult.get('dead')
            itemAdded   = playerTurnResult.get('itemAdded')
            itemUsed    = playerTurnResult.get('consumed')
            itemDropped = playerTurnResult.get('itemDropped')

            if message:
                msg_log.addMessage(message)

            if deadEntity:
                if deadEntity == player:
                    message, gameState = killPlayer(deadEntity)

                else:
                    message = killMonster(deadEntity)

                msg_log.addMessage(message)

            # If you pick up an item...
            if itemAdded:
                entities.remove(itemAdded)

                gameState = gameStates.ENEMY_TURN

            # If you use an item...
            if itemUsed:
                gameState = gameStates.ENEMY_TURN

            # If you drop an item...
            if itemDropped:
                entities.append(itemDropped)

        if gameState == gameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemyTurnResults = entity.ai.takeTurn(player,
                        fov_map, game_map, entities)

                    for enemyTurnResult in enemyTurnResults:
                        message = enemyTurnResult.get('message')
                        deadEntity = enemyTurnResult.get('dead')

                        if message:
                            msg_log.addMessage(message)

                        if deadEntity:
                            if deadEntity == player:
                                message, gameState = killPlayer(deadEntity)

                            else:
                                message = killMonster(deadEntity)

                            msg_log.addMessage(message)

                            if gameState == gameStates.PLAYER_DEAD:
                                break

                    if gameState == gameStates.PLAYER_DEAD:
                        break


            else:
                gameState = gameStates.PLAYER_TURN

if __name__ == '__main__':
    main()
