import libtcodpy as libtcod

class basicMonster:
    
    def takeTurn(self,target,fovMap,gameMap,entities):
        results = []

        monster = self.owner

        if libtcod.map_is_in_fov(fovMap, monster.x, monster.y):
            
            if monster.distanceTo(target) >= 2:
                monster.moveAStar(target, gameMap, entities)

            elif target.stats.HP > 0:
                attackResults = monster.stats.attack(target)
                results.extend(attackResults)

        return results
