from BigWorld.BaseCollection import *
from BigWorld.DamageType import *

class DamageCollection(BaseCollection):

    def getMap(self):
        return {1:DAMAGE_MAIN_AP, 
         2:DAMAGE_MAIN_HE, 
         3:DAMAGE_AMK_AP, 
         4:DAMAGE_AMK_HE, 
         7:DAMAGE_SHIP_TORPEDO, 
         10:DAMAGE_AVIA_BOMB, 
         11:DAMAGE_AVIA_TORPEDO, 
         16:DAMAGE_FIRE, 
         17:DAMAGE_RAM, 
         19:DAMAGE_SINK}

    def set(self, itemCode, value):
        if itemCode not in self._items:
            super(DamageCollection, self).set(itemCode, value)
            super(DamageCollection, self).add(DAMAGE_ALL, value)
        elif self._items[itemCode] < value:
            prevValue = self.get(itemCode)
            super(DamageCollection, self).set(itemCode, value)
            super(DamageCollection, self).add(DAMAGE_ALL, value - prevValue)


class DamageCollection_0_6_12(DamageCollection):

    def getMap(self):
        return {1:DAMAGE_MAIN_AP, 
         2:DAMAGE_MAIN_HE, 
         3:DAMAGE_AMK_AP, 
         4:DAMAGE_AMK_HE, 
         7:DAMAGE_SHIP_TORPEDO, 
         11:DAMAGE_AVIA_BOMB, 
         12:DAMAGE_AVIA_TORPEDO, 
         17:DAMAGE_FIRE, 
         18:DAMAGE_RAM, 
         20:DAMAGE_SINK}


class DamageCollection_0_6_13(DamageCollection):

    def getMap(self):
        return {1:DAMAGE_MAIN_AP, 
         2:DAMAGE_MAIN_HE, 
         3:DAMAGE_AMK_AP, 
         4:DAMAGE_AMK_HE, 
         7:DAMAGE_SHIP_TORPEDO, 
         10:DAMAGE_AVIA_BOMB_AP, 
         11:DAMAGE_AVIA_BOMB_HE, 
         12:DAMAGE_AVIA_TORPEDO, 
         17:DAMAGE_FIRE, 
         18:DAMAGE_RAM, 
         20:DAMAGE_SINK}

    def set(self, itemCode, value):
        if itemCode not in self._items:
            super(DamageCollection_0_6_13, self).set(itemCode, value)
            if itemCode == DAMAGE_AVIA_BOMB_AP or itemCode == DAMAGE_AVIA_BOMB_HE:
                super(DamageCollection_0_6_13, self).add(DAMAGE_AVIA_BOMB, value)
            elif self._items[itemCode] < value:
                prevValue = self.get(itemCode)
                super(DamageCollection_0_6_13, self).set(itemCode, value)
                if itemCode == DAMAGE_AVIA_BOMB_AP or itemCode == DAMAGE_AVIA_BOMB_HE:
                    super(DamageCollection_0_6_13, self).add(DAMAGE_AVIA_BOMB, value - prevValue)


class DamageCollection_0_8_0(DamageCollection_0_6_13):

    def getMap(self):
        return {1:DAMAGE_MAIN_AP, 
         2:DAMAGE_MAIN_HE, 
         3:DAMAGE_AMK_AP, 
         4:DAMAGE_AMK_HE, 
         7:DAMAGE_SHIP_TORPEDO, 
         10:DAMAGE_AVIA_ROCKET, 
         11:DAMAGE_AVIA_BOMB, 
         12:DAMAGE_AVIA_TORPEDO, 
         17:DAMAGE_FIRE, 
         18:DAMAGE_RAM, 
         20:DAMAGE_SINK, 
         28:DAMAGE_ROCKET}


class DamageCollection_0_8_2(DamageCollection_0_8_0):

    def getMap(self):
        return {1:DAMAGE_MAIN_AP, 
         2:DAMAGE_MAIN_HE, 
         3:DAMAGE_AMK_AP, 
         4:DAMAGE_AMK_HE, 
         7:DAMAGE_SHIP_TORPEDO, 
         10:DAMAGE_AVIA_BOMB_AP, 
         11:DAMAGE_AVIA_BOMB_HE, 
         12:DAMAGE_AVIA_TORPEDO, 
         17:DAMAGE_FIRE, 
         18:DAMAGE_RAM, 
         20:DAMAGE_SINK, 
         27:DAMAGE_AVIA_BOMB, 
         28:DAMAGE_AVIA_ROCKET, 
         32:DAMAGE_MAIN_CS}
