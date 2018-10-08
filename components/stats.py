# [TODO] Add more stats
import libtcodpy as libtcod

from gameMessages import Message

class stats:
    def __init__(self,HP,DEF,STR):
        self.maxHP = HP
        self.HP = HP
        self.DEF = DEF
        self.STR = STR

    def takeDamage(self, amount):
        results = []

        self.HP -= amount

        if self.HP <= 0:
            results.append({'dead': self.owner})

        return results

    def attack(self, target):
        results = []

        damage = self.STR - target.stats.DEF

        if damage > 0:
            results.append({'message':
                Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(),target.name,str(damage)), libtcod.white)})
            results.extend(target.stats.takeDamage(damage))

        else:
            results.append({'message':
                Message('{0} strikes {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})
        
        return results
