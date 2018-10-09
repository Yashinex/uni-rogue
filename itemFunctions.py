import libtcodpy as libtcod

from gameMessages import Message

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.stats.HP == entity.stats.maxHP:
        results.append({
            'consumed' : False,
            'message'  : Message('You are already at full health.', libtcod.yellow)
        })

    else:
        entity.stats.heal(amount)

        if entity.stats.HP >= entity.stats.maxHP:
            entity.stats.HP = entity.stats.maxHP

        results.append({
            'consumed' : True,
            'message'  : Message('Your wounds start to feel better.', libtcod.yellow)
        })

    return results
