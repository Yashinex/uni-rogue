import libtcodpy as libtcod

def initializeFOV(gameMap):
    fov_map = libtcod.map_new(gameMap.width, gameMap.height)

    for y in range(gameMap.height):
        for x in range(gameMap.width):
            libtcod.map_set_properties(fov_map, x, y,
            not gameMap.tiles[x][y].blockSight, 
            not gameMap.tiles[x][y].blocked)

    return fov_map

def recomputeFOV(fov_map, x, y, radius, lightWalls = True, algorithm = 0):
    libtcod.map_compute_fov(fov_map, x, y, radius, lightWalls, algorithm)
