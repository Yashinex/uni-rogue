import libtcodpy as libtcod

from gameMessages import Message

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items    = []

    def addItem(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'itemAdded' : None,
                'message'   : Message('Your inventory is full!',
                    libtcod.yellow)
            })

        else:
            results.append({
                'itemAdded' : item,
                'message'   : Message('You pick up the {0}'.format(item.name),
                    libtcod.blue)
            })

            self.items.append(item)

        return results

    def use(self, itemEntity, **kwargs):
        results = []

        itemComponent = itemEntity.item

        if itemComponent.useFunction is None:
            results.append({
                'message': Message('You struggle to find a use for the {0}'.format(
                    itemEntity.name), libtcod.yellow)
            })

        else:
            kwargs = {**itemComponent.function_kwargs, **kwargs}

            itemUseResults = itemComponent.useFunction(self.owner, **kwargs)

            for itemUseResult in itemUseResults:
                if itemUseResult.get('consumed'):
                    self.removeItem(itemEntity)

            results.extend(itemUseResults)

        return results

    def removeItem(self, item):
        self.items.remove(item)

    def dropItem(self, item):
        results = []

        item.x = self.owner.x
        item.y = self.owner.y

        self.removeItem(item)
        results.append({
            'itemDropped': item,
            'message'    : Message('You dropped the {0}'.format(item.name),
                libtcod.yellow)
        })

        return results
