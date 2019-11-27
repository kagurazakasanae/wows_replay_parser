from BigWorld.BaseCollection import *
from BigWorld.RibbonType import *

class RibbonCollection(BaseCollection):

    def getMap(self):
        return {0:RIBBON_MAIN_CALIBER, 
         1:RIBBON_TORPEDO, 
         2:RIBBON_BOMB, 
         3:RIBBON_PLANE, 
         4:RIBBON_CRIT, 
         5:RIBBON_FRAG, 
         6:RIBBON_BURN, 
         7:RIBBON_FLOOD, 
         8:RIBBON_CITADEL, 
         9:RIBBON_BASE_DEFENSE, 
         10:RIBBON_BASE_CAPTURE, 
         11:RIBBON_BASE_CAPTURE_ASSIST, 
         12:RIBBON_SUPPRESSED, 
         13:RIBBON_SECONDARY_CALIBER, 
         14:RIBBON_MAIN_CALIBER_OVER_PENETRATION, 
         15:RIBBON_MAIN_CALIBER_PENETRATION, 
         16:RIBBON_MAIN_CALIBER_NO_PENETRATION, 
         17:RIBBON_MAIN_CALIBER_RICOCHET, 
         18:RIBBON_BUILDING_KILL, 
         19:RIBBON_DETECTED, 
         20:RIBBON_BOMB_OVER_PENETRATION, 
         21:RIBBON_BOMB_PENETRATION, 
         22:RIBBON_BOMB_NO_PENETRATION, 
         23:RIBBON_BOMB_RICOCHET}

    def addById(self, itemId, value=1):
        super(RibbonCollection, self).addById(itemId, value)
        itemCode = self.getCodeById(itemId)
        if itemCode == RIBBON_MAIN_CALIBER_PENETRATION or itemCode == RIBBON_MAIN_CALIBER_OVER_PENETRATION or itemCode == RIBBON_MAIN_CALIBER_NO_PENETRATION or itemCode == RIBBON_MAIN_CALIBER_RICOCHET or itemCode == RIBBON_CITADEL:
            super(RibbonCollection, self).add(RIBBON_MAIN_CALIBER, value)
        elif itemCode == RIBBON_BOMB_OVER_PENETRATION or itemCode == RIBBON_BOMB_PENETRATION or itemCode == RIBBON_BOMB_NO_PENETRATION or itemCode == RIBBON_BOMB_RICOCHET:
            super(RibbonCollection, self).add(RIBBON_BOMB, value)


class RibbonCollection_0_7_11(RibbonCollection):

    def addById(self, itemId, value=1):
        super(RibbonCollection_0_7_11, self).addById(itemId, value)
        itemCode = self.getCodeById(itemId)
        if itemCode == RIBBON_CITADEL:
            super(RibbonCollection, self).add(RIBBON_MAIN_CALIBER, -value)


class RibbonCollection_0_8_0(RibbonCollection_0_7_11):

    def getMap(self):
        return {0:RIBBON_MAIN_CALIBER, 
         1:RIBBON_TORPEDO, 
         2:RIBBON_BOMB, 
         3:RIBBON_PLANE, 
         4:RIBBON_CRIT, 
         5:RIBBON_FRAG, 
         6:RIBBON_BURN, 
         7:RIBBON_FLOOD, 
         8:RIBBON_CITADEL, 
         9:RIBBON_BASE_DEFENSE, 
         10:RIBBON_BASE_CAPTURE, 
         11:RIBBON_BASE_CAPTURE_ASSIST, 
         12:RIBBON_SUPPRESSED, 
         13:RIBBON_SECONDARY_CALIBER, 
         14:RIBBON_MAIN_CALIBER_OVER_PENETRATION, 
         15:RIBBON_MAIN_CALIBER_PENETRATION, 
         16:RIBBON_MAIN_CALIBER_NO_PENETRATION, 
         17:RIBBON_MAIN_CALIBER_RICOCHET, 
         18:RIBBON_BUILDING_KILL, 
         19:RIBBON_DETECTED, 
         20:RIBBON_BOMB_OVER_PENETRATION, 
         21:RIBBON_BOMB_PENETRATION, 
         22:RIBBON_BOMB_NO_PENETRATION, 
         23:RIBBON_BOMB_RICOCHET, 
         25:RIBBON_ROCKET_PENETRATION, 
         26:RIBBON_ROCKET_NO_PENETRATION, 
         27:RIBBON_SPLANE}


class RibbonCollection_0_8_5(RibbonCollection_0_8_0):

    def getMap(self):
        return {0:RIBBON_MAIN_CALIBER, 
         1:RIBBON_TORPEDO, 
         2:RIBBON_BOMB, 
         3:RIBBON_PLANE, 
         4:RIBBON_CRIT, 
         5:RIBBON_FRAG, 
         6:RIBBON_BURN, 
         7:RIBBON_FLOOD, 
         8:RIBBON_CITADEL, 
         9:RIBBON_BASE_DEFENSE, 
         10:RIBBON_BASE_CAPTURE, 
         11:RIBBON_BASE_CAPTURE_ASSIST, 
         12:RIBBON_SUPPRESSED, 
         13:RIBBON_SECONDARY_CALIBER, 
         14:RIBBON_MAIN_CALIBER_OVER_PENETRATION, 
         15:RIBBON_MAIN_CALIBER_PENETRATION, 
         16:RIBBON_MAIN_CALIBER_NO_PENETRATION, 
         17:RIBBON_MAIN_CALIBER_RICOCHET, 
         18:RIBBON_BUILDING_KILL, 
         19:RIBBON_DETECTED, 
         20:RIBBON_BOMB_OVER_PENETRATION, 
         21:RIBBON_BOMB_PENETRATION, 
         22:RIBBON_BOMB_NO_PENETRATION, 
         23:RIBBON_BOMB_RICOCHET,
		 24:RIBBON_ROCKET,
         25:RIBBON_ROCKET_PENETRATION, 
         26:RIBBON_ROCKET_NO_PENETRATION, 
         27:RIBBON_SPLANE, 
         28:RIBBON_BULGE, 
         29:RIBBON_BOMB_BULGE, 
         30:RIBBON_ROCKET_BULGE}

    def addById(self, itemId, value=1):
        super(RibbonCollection_0_8_5, self).addById(itemId, value)
        itemCode = self.getCodeById(itemId)
        if itemCode == RIBBON_BULGE:
            super(RibbonCollection_0_8_5, self).add(RIBBON_MAIN_CALIBER, value)
        elif itemCode == RIBBON_BOMB_BULGE:
            super(RibbonCollection_0_8_5, self).add(RIBBON_BOMB, value)
