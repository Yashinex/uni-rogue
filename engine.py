import libtcodpy as libtcod

from entity             import Entity, getBlockingEntitiesAtLocation
from inputHandlers      import handleKeys
from renderFunctions    import clearAll, renderAll, renderOrder
from mapObjects.gameMap import gameMap
from fovFunctions       import initializeFOV, recomputeFOV
from gameStates         import gameStates
from components.stats   import stats
from deathFunctions     import killPlayer, killMonster
from gameMessages       import messageLog

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
    roomMaxSize = 10
    roomMinSize = 6
    maxRooms    = 30

    # monsters
    maxMonstersRoom = 3

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
    player = Entity(0, 0, '@', libtcod.red, 'Player', blocks=True,
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
        player, entities, maxMonstersRoom)

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

    # game loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recomputeFOV(fov_map,player.x,player.y,fov_radius,fov_light_walls,
            fov_algorithm)

        # [DO NOT DELETE] renders entities each frame
        renderAll(con, panel, entities, player, game_map, fov_map, 
            fov_recompute, msg_log, screenWidth, screenHeight, barWidth,
            panelHeight, panelDiff, colors)

        fov_recompute = False

        # [DO NOT DELETE] refreshes each frame
        libtcod.console_flush()

        # [DO NOT DELETE] clears each frame
        clearAll(con, entities)

        action = handleKeys(key)

        move = action.get('move')
        exit = action.get('exit')
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

        # exit from inputHandlers
        if exit:
            return True

        # fullscreen check
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for playerTurnResult in playerTurnResults:
            message = playerTurnResult.get('message')
            deadEntity = playerTurnResult.get('dead')

            if message:
                msg_log.addMessage(message)

            if deadEntity:
                if deadEntity == player:
                    message, gameState = killPlayer(deadEntity)

                else:
                    message = killMonster(deadEntity)

                msg_log.addMessage(message)

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
