import libtcodpy as libtcod

from random                 import randint
from entity                 import Entity
from mapObjects.tile        import tile
from mapObjects.rectangle   import rect
from components.ai          import basicMonster
from components.item        import Item
from components.stats       import stats
from renderFunctions        import renderOrder
from itemFunctions          import heal

class gameMap:

    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.tiles  = self.initializeTiles()

    def initializeTiles(self):
        tiles = [[tile(True) for y in range(self.height)]
        for x in range(self.width)]

        return tiles

    # Generates randomized room layouts
    def makeMap(self, maxRooms, roomMinSize, roomMaxSize, mapWidth, mapHeight,
        player, entities, maxMonstersRoom, maxItemsRoom):
        
        rooms = []
        numRooms = 0

        r = randint(0, maxRooms)

        for i in range(r):
            # randomize width and height
            w = randint(roomMinSize,roomMaxSize)
            h = randint(roomMinSize,roomMaxSize)
            # random position in map bounds
            x = randint(0, mapWidth - w - 1)
            y = randint(0, mapHeight - h - 1)

            # rect class makes rectangles easier to work with
            newRoom = rect(x,y,w,h)

            # run thru other rooms and see if they intersect
            for otherRoom in rooms:
                if newRoom.intersect(otherRoom):
                    break

            # this runs if there are no intersections, i.e. valid room
            else:
                # paint to map's tiles
                self.createRoom(newRoom)

                # center coordinates of newRoom
                (newX, newY) = newRoom.center()

                # first room, i.e. player start position
                if numRooms == 0:
                    player.x = newX
                    player.y = newY

                # other rooms
                # need connections to other rooms
                else:
                    # center coordinates of previous room
                    (prevX, prevY) = rooms[numRooms - 1].center()

                    # random 0 or 1
                    if randint(0,1) == 1:
                        # horz then vert
                        self.createHorzTunnel(prevX,newX,prevY)
                        self.createVertTunnel(prevY,newY,prevX)

                    else:
                        # vert then horz
                        self.createVertTunnel(prevY,newY,prevX)
                        self.createHorzTunnel(prevX,newX,prevY)

                self.placeEntities(newRoom, entities, maxMonstersRoom,
                    maxItemsRoom)

                # append new room to list
                rooms.append(newRoom)
                numRooms += 1


    def createRoom(self, room):
        # go through tiles in rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].blockSight = False

    def createHorzTunnel(self,x1,x2,y):
        for x in range(min(x1,x2),max(x1,x2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].blockSight = False

    def createVertTunnel(self,y1,y2,x):
        for y in range(min(y1,y2),max(y1,y2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].blockSight = False

    def placeEntities(self, room, entities, maxMonstersRoom,
        maxItemsRoom):
        # random number of monsters
        numMonsters = randint(0, maxMonstersRoom)
        numItems    = randint(0, maxItemsRoom)

        for i in range(numMonsters):
            # choose a random location in the room
            x = randint(room.x1+1, room.x2-1)
            y = randint(room.y1+1, room.y2-1)

            # creates a monster
            if not any([entity for entity in entities 
                if entity.x == x and entity.y == y]):

                # percentage tables
                if randint(0,100) < 80:
                    monsterStats = stats(HP=20, DEF=0, STR=3)
                    componentAI = basicMonster()

                    monster = Entity(x,y,'O',libtcod.desaturated_green,
                        'Ork', blocks=True, render_order=renderOrder.ACTOR,
                        stats=monsterStats, ai=componentAI)

                else:
                    monsterStats = stats(HP=30, DEF=1, STR=4)
                    componentAI = basicMonster()

                    monster = Entity(x,y,'T',libtcod.darker_green,
                        'Troll', blocks=True, render_order=renderOrder.ACTOR,
                        stats=monsterStats, ai=componentAI)

                entities.append(monster)

        for i in range(numItems):
            x = randint(room.x1+1, room.x2-1)
            y = randint(room.y1+1, room.y2-1)

            if not any([entity for entity in entities if entity.x==x and entity.y==y]):
                itemComponent = Item(useFunction=heal, amount=5)
                item = Entity(x, y, '*', libtcod.red, 'Health Potion',
                    render_order=renderOrder.ITEM, item=itemComponent)

                entities.append(item)

    def isBlocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
