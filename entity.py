import math
import libtcodpy as libtcod

from renderFunctions import renderOrder

class Entity:
    """
    A generic object to represent something, i.e. players, enemies, items, etc.
    """

    def __init__(self, x, y, char, color, name, blocks=False, render_order = renderOrder.CORPSE,
        stats=None, ai=None, item=None, inventory=None):

        # create attributes for an Entity, i.e. item/player/npc
        self.x              = x
        self.y              = y
        self.char           = char
        self.color          = color
        self.name           = name
        self.blocks         = blocks
        self.render_order   = render_order
        self.stats          = stats
        self.ai             = ai
        self.item           = item
        self.inventory      = inventory

        # gives ownership of particular things to entity
        if self.stats:
            self.stats.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

    def move(self, dx, dy):
        # Move the entity some amount
        self.x += dx
        self.y += dy

    # calculates distance b/w target and entity, and moves towards target
    def moveToward(self, targetX, targetY, gameMap, entities):
        dx = targetX - self.x
        dy = targetY - self.y
        distance = math.sqrt(dx**2 + dy**2)

        dx = int(round(dx/distance))
        dy = int(round(dy/distance))

        if not (gameMap.isBlocked(self.x+dx,self.y+dy) or
        getBlockingEntitiesAtLocation(entities,self.x+dx,self.y+dy)):
            self.move(dx,dy)

    def moveAStar(self, target, gameMap, entities):
        width = gameMap.width
        height = gameMap.height
        # Create a FOV map that has the dimensions of the map
        fov = libtcod.map_new(width, height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(gameMap.height):
            for x1 in range(gameMap.width):
                libtcod.map_set_properties(fov, x1, y1,
                    not gameMap.tiles[x1][y1].blockSight,
                    not gameMap.tiles[x1][y1].blocked)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.moveToward(target.x, target.y, gameMap, entities)

            # Delete the path to free memory
        libtcod.path_delete(my_path)

    def distanceTo(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx**2 + dy**2)

def getBlockingEntitiesAtLocation(entities, destX, destY):
    for entity in entities:
        if entity.blocks and entity.x == destX and entity.y == destY:
            return entity

    return None
