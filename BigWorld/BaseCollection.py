class BaseCollection(object):
    __qualname__ = 'BaseCollection'
    
    def __init__(self):
        self._type_map = self.getMap()
        self._items = { }

    
    def getMap(self):
        return { }

    
    def setById(self, itemId, value):
        itemCode = self.getCodeById(itemId)
        if itemCode:
            self._items[itemCode] = value
        else:
            print('BaseCollection::setById(unknown: itemId {}, value {}'.format(itemId, value))

    
    def addById(self, itemId, value = (1,)):
        itemCode = self.getCodeById(itemId)
        if itemCode:
            self.add(itemCode, value)
        else:
            print('BaseCollection::addById(unknown: itemId {}, value {}'.format(itemId, value))

    
    def getCodeById(self, itemId):
        if itemId in self._type_map:
            return self._type_map[itemId]
        return None

    
    def set(self, itemCode, value):
        self._items[itemCode] = value

    
    def add(self, itemCode, value = (1,)):
        if itemCode not in self._items:
            self._items[itemCode] = 0
        self._items[itemCode] += value

    
    def get(self, itemCode):
        if itemCode in self._items:
            return self._items[itemCode]
        return None

    
    def getItems(self):
        return self._items



