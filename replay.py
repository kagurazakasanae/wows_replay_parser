import os, re, json, struct, io, zlib, utils, pickle, model, sys
from Crypto.Cipher import Blowfish
from BigWorld import *

BLOWFISH_KEY = b')\xb7\xc9\t8?\x84\x88\xfa\x98\xecN\x13\x19y\xfb'

class ReplayFile(object):
    def __init__(self, fileName):
        self._fileName = fileName
        self.arena_info = {}
        self.world = None
        self.version = ''
        
    def parse(self):
        self.arena_info = {}
        self.world = None
        if not os.path.exists(self._fileName):
            raise Exception("File not exists")
        else:
            with open(self._fileName, 'rb') as (f):
                f.seek(4)
                blocks_count = struct.unpack('i', f.read(4))[0]
                if blocks_count != 1:
                    raise Exception("blocks_count != 1")
                block_size = struct.unpack('i', f.read(4))[0]
                self.arena_info = json.loads(f.read(block_size).decode())
                self.version = '.'.join(re.split('[^0-9]+', self.arena_info['clientVersionFromExe']))
                self.world = BigWorldFabric.createFromVersion(self.arena_info['clientVersionFromExe'])
                if self.world is None:
                    raise Exception("world is None")
                decrypted_data = self.decrypt_blowfish_data(f.read())
                try:
                    unzipped_data = zlib.decompress(decrypted_data)
                except zlib.error:
                    raise Exception("zlib.error")
                stream = io.BytesIO(unzipped_data)
                while stream.readable():
                    base_packet = BigWorldPacket(stream)
                    if not base_packet.inited:
                        break
                    self.world.processPacket(base_packet)
                    
    def unit_test(self):
        pass
        
    def get_arenainfo(self):
        return self.arena_info

    def get_battleResult(self):
        return self.world.battleresult
    
    def get_battleDuration(self):
        return self.world.battleDuration
    
    def get_players(self):
        return self.world.players
        
    def get_damage(self):
        return self.world.damage.getItems()
        
    def get_spotting_damage(self):
        return self.world.spotting_damage.getItems()
        
    def get_potential_damage(self):
        return self.world.potential_damage.getItems()
        
    def get_own_player(self):
        return self.world.own_player
        
    def get_commanderSkills(self):
        return self.world.crewSkills
        
    def get_flags(self):
        return self.world.flags
        
    def get_camo(self):
        return self.world.camo
        
    def get_ribbons(self):
        return self.world.ribbons.getItems()

    def get_chats(self):
        return self.world.chat

    def get_ribbon_map(self):
        ret = {}
        map = self.world.ribbons.getMap()
        for x in map:
            ret[map[x]] = x
        return ret
	
    def get_fleet(self):
        return self.world.fleetteams
        
    def convert_crewSkills(self, skillsId, crewId):
        crewSkills = list('.. .. .. ..;.. .. .. ..;.. .. .. ..;.. .. .. ..;')
        defaultSkills = model.crew[str(crewId)]['Skills']
        i = int(skillsId)
        for skillId in defaultSkills:
            if i & 2 ** (int(skillId) - 1):
                column = defaultSkills[skillId]['column']
                tier = defaultSkills[skillId]['tier']
                crewSkills[(tier - 1) * 12 + column + column // 2] = '!'
        return crewSkills

    def decrypt_blowfish_data(self, ori_data, type=0):
        previous_block_Q = None
        cl = Blowfish.new(BLOWFISH_KEY)
        de_data = cl.decrypt(ori_data[8:])
        l = len(de_data)
        decrypted_data = io.BytesIO()
        for index in range(0, l, 8):
            decrypted_block = de_data[index:index + 8]
            decrypted_block_Q, = struct.unpack('Q', decrypted_block)
            if previous_block_Q is not None:
                decrypted_block_Q ^= previous_block_Q
                decrypted_block = struct.pack('Q', decrypted_block_Q)
            previous_block_Q = decrypted_block_Q
            decrypted_data.write(decrypted_block)
        if type == 0:
            return decrypted_data.getvalue()
        else:
            return decrypted_data
    
class BigWorldPacket(object):

    def __init__(self, stream):
        self.inited = False
        #print 'Pos:',stream.tell()
        b = stream.read(4)
        if len(b) != 4:
            return
        self.size, = struct.unpack('I', b)
        self.type, = struct.unpack('I', stream.read(4))
        self.time, = struct.unpack('f', stream.read(4))
        self.data = stream.read(self.size)
        self.inited = True

        
class BigWorldFabric(object):
    @staticmethod
    def createFromVersion(version):
        version = BigWorldFabric.versiontuple(version)
        map = json.load(open(sys.path[0]+'/db/replay.json', 'r'))
        for map_version in map:
            start_version = BigWorldFabric.versiontuple(map_version['from'])
            end_version = BigWorldFabric.versiontuple(map_version['to'])
            if version >= start_version:
                if version <= end_version:
                    class_ = map_version['big_world']
                    #print('createFromVersion', version, start_version, end_version, class_)
                    if class_ is not None:
                        world = globals()[class_](map_version)
                        return world

    @staticmethod
    def versiontuple(v):
        return tuple(map(int, re.split('[^0-9]+', v)[0:3]))
        

class BaseObject(object):

    def createMap(self, config):
        result = {}
        for id, method_name in config.items():
            id = int(id)
            method = getattr(self, method_name, None)
            if method is not None:
                result[id] = method

        return result

class BigWorld(BaseObject):

    def __init__(self, config):
        self.type_map = self.createMap(config['packet_type'])
        self.entity_map = self.createMap(config['entity'])
        self.avatar = self.createAvatar(config['avatar'])
        self.vehicle_config = config['vehicle']
        self.battle_logic_config = config['battle_logic']
        self.damage_model = config['damage_model']
        self.ribbon_model = config['ribbon_model']
        self.ship_id = config['ship_id']
        self.ship_config_id = config['ship_config_id']
        self.base_ship = utils.safe_cast_by_key(config, 'base_ship', int, 0)
        self.entities = {}
        self.time = 0.0
        self.battleStartTime = 0.0
        self.battleEndTime = 0.0
        self.playerDeathTime = 0.0
        self.damage = self.createDamage()
        self.spotting_damage = self.createDamage()
        self.potential_damage = self.createDamage()
        self.ribbons = self.createRibbon()
        self.basePlayerEntityId = 0
        self.baseShipEntityId = 0
        self.baseShipArtillery = False
        self.baseShipTorpedoes = False
        self.guns = {}
        self.torps = {}
        self.own_player = {}
        self.players = {}
        self.players_map = {}
        self.fleetteams = {}
        self.chat = []
        self.consumablesPrice = 0
        self.camo = ''
        self.flags = []
        self.commanderId = None
        self.crewSkills = None
        self.battleresult = -1

    def processPacket(self, base_packet):
        self.time = base_packet.time
        if base_packet.type in self.type_map:
            self.type_map[base_packet.type](base_packet.data)

    def createDamage(self):
        #return globals()['DamageCollection'].DamageCollection
        return getattr(globals()['DamageCollection'], self.damage_model)()

    def createRibbon(self):
        return getattr(globals()['RibbonCollection'], self.ribbon_model)()

    def createAvatar(self, config):
        return BigWorldAvatar(self, config)

    def createVehicle(self, data):
        return BigWorldVehicle(self, self.vehicle_config)

    def createBattleLogic(self, data):
        return BigWorldBattleLogic(self, self.battle_logic_config)

    def onBasePlayerCreate(self, data):
        entity_id, = struct.unpack('i', data[0:4])
        type, = struct.unpack('h', data[4:6])
        subdata = data[6:]
        self.basePlayerEntityId = entity_id

    def enterEntity(self, data):
        entity_id, = struct.unpack('i', data[0:4])
        space_id, = struct.unpack('i', data[4:8])
        vehicle_id, = struct.unpack('i', data[8:12])
        #print 'enterEntity ', entity_id, space_id, vehicle_id

    def createEntity(self, data):
        entity_id, = struct.unpack('i', data[0:4])
        type, = struct.unpack('h', data[4:6])
        space_id, vehicle_id, x, y, z, yaw, pitch, roll, sub_data_len = struct.unpack('iiffffffi', data[6:42])
        sub_data = data[42:]
        if type in self.entity_map:
            self.entities[entity_id] = self.entity_map[type](sub_data)
        prop_count, = struct.unpack('B', sub_data[0:1])
        re_pattern = '^\\x{:02x}'.format(prop_count)
        for prop_num in range(0, prop_count):
            if self.ship_config_id >= 0 and prop_num == self.ship_config_id:
                re_pattern += '\\x{:02x}(\\x01.+)'.format(prop_num)
                continue
            if self.ship_id >= -1 and prop_num == self.ship_id:
                re_pattern += '\\x{:02x}(....)'.format(prop_num)
                continue
            re_pattern += '\\x{:02x}(.+?)'.format(prop_num)

        re_pattern += '$'
        re_exec = re.compile(re_pattern, re.DOTALL)
        if not re_exec:
            return
        re_match = re_exec.match(sub_data)
        if not re_match:
            return
        isBaseShip = 0
        commanderId = None
        crewSkills = None
        shipData = None
        for prop_num in range(1, prop_count + 1):
            prop_value = re_match.group(prop_num)
            prop_value_len = len(prop_value)
            if prop_value_len == 16:
                (crewSkills,) = struct.unpack('I', prop_value[4:8])
                (commanderId,) = struct.unpack('I', prop_value[12:16])
            if prop_value_len == 4:
                (d,) = struct.unpack('I', prop_value)
                if d == self.basePlayerEntityId:
                    isBaseShip += 1
            if prop_value_len > 6:
                (flag,) = struct.unpack('B', prop_value[0:1])
                if flag == 1:
                    (shipId,) = struct.unpack('I', prop_value[1:5])
                    (configLen,) = struct.unpack('B', prop_value[5:6])
                    if prop_value_len == configLen + 6:
                        shipData = prop_value[1:]
                    try:
                        self.players[self.players_map[entity_id - 1]['nickName']]['commanderId'] = commanderId
                        self.players[self.players_map[entity_id - 1]['nickName']]['crewSkills'] = crewSkills
                    except:
                        pass
                    if isBaseShip == 1 and shipData is not None:
                        self.commanderId = commanderId
                        self.crewSkills = crewSkills
                        self.onBaseShip(entity_id, shipId, shipData)

    def onBaseShip(self, entity_id, shipId, config):
        self.baseShipEntityId = entity_id
        shipId, = struct.unpack('I', config[0:4])
        len, = struct.unpack('B', config[4:5])
        shipId = str(shipId)
        artillery = {}
        if shipId in model.ships:
            if 'artillery' in model.ships[shipId]:
                artillery = model.ships[shipId]['artillery']
        torpedoes = {}
        if shipId in model.ships:
            if 'torpedoes' in model.ships[shipId]:
                torpedoes = model.ships[shipId]['torpedoes']
        offset = 5
        counter, = struct.unpack('I', config[offset:offset + 4])
        offset += 4
        i = 0
        while i < counter:
            unitId, = struct.unpack('I', config[offset:offset + 4])
            offset += 4
            i += 1
            if not unitId:
                continue
            unitId = str(unitId)
            if unitId in artillery:
                self.baseShipArtillery = artillery[unitId]
            elif unitId in torpedoes:
                self.baseShipTorpedoes = torpedoes[unitId]

        counter, = struct.unpack('I', config[offset:offset + 4])
        offset += 4
        i = 0
        while i < counter:
            unitId, = struct.unpack('I', config[offset:offset + 4])
            offset += 4
            i += 1
            if not unitId:
                continue
            unitId = str(unitId)
            if unitId in model.items:
                pass

        counter, = struct.unpack('I', config[offset:offset + 4])
        offset += 4
        i = 0
        while i < counter:
            unitId, = struct.unpack('I', config[offset:offset + 4])
            offset += 4
            i += 1
            if not unitId:
                continue
            unitId = str(unitId)
            if unitId in model.items:
                if model.items[unitId]['type'] == 'Camouflage':
                    try:
                        self.camo = model.items[str(unitId)]['name']
                    except:
                        self.camo = unitId
                elif model.items[unitId]['type'] == 'Flags':
                    try:
                        self.flags.append(model.items[str(unitId)]['name'])
                    except:
                        self.flags.append(unitId)

        offset += 4
        #print('unknown', config[offset:].encode('hex'))
        if self.base_ship != 1:
            while 1:
                counter, = struct.unpack('I', config[offset:offset + 4])
                offset += 4
                if counter == 0:
                    break
                offset += 4
                if counter == 1:
                    offset += 4
                    break

        #print(config[offset:].encode('hex'))
        counter, = struct.unpack('I', config[offset:offset + 4])
        offset += 4
        i = 0
        while i < counter:
            try:
                unitId, = struct.unpack('I', config[offset:offset + 4])
            except struct.error:
                break

            offset += 4
            i += 1
            if not unitId:
                continue
            unitId = str(unitId)
            if unitId in model.items:
                if 'price' in model.items[unitId]:
                    self.consumablesPrice += model.items[unitId]['price']
                #print('Consumables?', counter, model.items[unitId])

    def entityProperty(self, data):
        entity_id, = struct.unpack('I', data[0:4])
        subtype, = struct.unpack('I', data[4:8])
        subdata = data[8:]
        if entity_id in self.entities:
            self.entities[entity_id].setProperty(entity_id, subtype, subdata)
        elif self.avatar:
            self.avatar.setProperty(entity_id, subtype, subdata)

    def callEntityMethod(self, data):
        entity_id, = struct.unpack('I', data[0:4])
        subtype, = struct.unpack('I', data[4:8])
        subdata = data[8:]
        if entity_id in self.entities:
            self.entities[entity_id].callMethod(entity_id, subtype, subdata)
        elif self.avatar:
            self.avatar.callMethod(entity_id, subtype, subdata)


class BigWorldEntity(BaseObject):

    def __init__(self, world, config):
        self.world = world
        self.method_map = self.createMap(config['method']) if 'method' in config else {}
        self.property_map = self.createMap(config['property']) if 'property' in config else {}
        self.call_count = {}

    def callMethod(self, entity_id, type, data):
        if type in self.method_map:
            self.method_map[type](entity_id, data)

    def setProperty(self, entity_id, type, data):
        if type in self.property_map:
            self.property_map[type](entity_id, data)


class BigWorldAvatar(BigWorldEntity):

    def __init__(self, world, config):
        super(BigWorldAvatar, self).__init__(world, config)
        self.id_property_map = config['id_property']

    def onChatMessage(self, vehicleId, data):
        message_len, = struct.unpack('I', data[0:4])
        source_id, = struct.unpack('I', data[4:8])
        if source_id in self.world.players_map:
            source = self.world.players_map[source_id]['nickName']
            sourceTeam = self.world.players_map[source_id]['teamId']
            sourceShipId = self.world.players_map[source_id]['shipId']
        else:
            source = 'unknown'
            sourceTeam = -1
            sourceShipId = 0

        if vehicleId in self.world.players_map:
            myTeam = self.world.players_map[vehicleId]['teamId']
        else:
            myTeam = -1
        prefix_len, = struct.unpack('B', data[8:9])
        prefix = data[9:9 + prefix_len]
        text_len, = struct.unpack('B', data[9 + prefix_len:9 + prefix_len + 1])
        text_data = data[9 + prefix_len + 1:9 + prefix_len + 1 + text_len].decode('utf-8', 'ignore')
        self.world.chat.append({'time':int(self.world.time), 
         'from':source, 
         'text':text_data, 
         'ally':1 if myTeam == sourceTeam else 0, 
         'self':1 if vehicleId == source_id else 0, 
         'prefix_len':prefix_len})

    def onRibbon(self, vehicleId, data):
        ribbon_size, = struct.unpack('I', data[0:4])
        if ribbon_size == 1:
            ribbon_id, = struct.unpack('b', data[4:6])
            self.world.ribbons.addById(ribbon_id)

    def onBattleEnd(self, vehicleId, data):
        #print 'onBattleEnd',self.world.time, struct.unpack("BB",data[4:])
        winteamId, winreason = struct.unpack("BB",data[4:])
        self.world.battleresult = 1 if winteamId == self.world.own_player['teamId'] else 0
        self.world.battleEndTime = self.world.time
        battleDuration = round(self.world.battleEndTime - self.world.battleStartTime)
        minutes = int(battleDuration / 60)
        
    def receiveAchivement(self, vehicleId, data):
        playerId, = struct.unpack('I', data[4:8])
        achivementId, = struct.unpack('I', data[8:12])
        self.world.players[self.world.players_map[playerId]['nickName']]['achivements'].append(model.items[str(achivementId)]['name'])

    def receiveVehicleDeath(self, vehicleId, data):
        killerId, = struct.unpack('I', data[8:12]) #entity in even number -> vehicle id , convert to player entity id is -1
        killedId, = struct.unpack('I', data[4:8])
        killerPlayer = self.world.players_map[killerId - 1]
        killedPlayer = self.world.players_map[killedId - 1]
        if killerPlayer['teamId'] != killedPlayer['teamId']:
            self.world.players[killerPlayer['nickName']]['killCount'] += 1
        else:
            self.world.players[killerPlayer['nickName']]['killCount'] -= 1
        self.world.players[killerPlayer['nickName']]['kill'].append(killedPlayer['nickName'])
        self.world.players[killedPlayer['nickName']]['killed'] = killerPlayer['nickName']
        
        if killedId == self.world.baseShipEntityId:
            self.world.playerDeathTime = self.world.time

    def receiveDamageStat(self, vehicleId, data):
        dmg_size, = struct.unpack('I', data[0:4])
        offset = 4
        while True:
            offset = data.find(b'\x80\x02', offset)
            if offset == -1:
                return
            break

        dmg_data = pickle.loads((data[offset:]))

        for key, value in dmg_data.items():
            i, flag = key
            cnt, val = value[0], value[1]
            if flag == 0:
                self.world.damage.setById(i, val)
            elif flag == 2:
                self.world.spotting_damage.setById(i, val)
            elif flag == 3:
                self.world.potential_damage.setById(i, val)
            else:
                #print('BigWorldAvatar::receiveDamageStat dmg_data: {}'.format(dmg_data))
                pass

    def receiveShellInfo(self, vehicleId, data):
        len, = struct.unpack('I', data[0:4])
        ammoId, = struct.unpack('I', data[4:8])

    def onArenaStateReceived(self, entityId, data):
        pos = 0
        while True:
            pos = data.find(b'\x80\x02', pos)
            if pos == -1:
                return
            try:
                playersStates = pickle.loads(data[pos:])
                if type(playersStates) == list:
                    break
            except pickle.UnpicklingError:
                pass

            pos += 1

        for player in playersStates:
            i, entityId = player[self.id_property_map['entityId']] if 'entityId' in self.id_property_map else (0, 0)
            i, clanColor = player[self.id_property_map['clanColor']] if 'clanColor' in self.id_property_map else (0, 0)
            i, clanId = player[self.id_property_map['clanId']] if 'clanId' in self.id_property_map else (0, 0)
            i, nickName = player[self.id_property_map['name']] if 'name' in self.id_property_map else (0, '')
            i, teamId = player[self.id_property_map['teamId']] if 'teamId' in self.id_property_map else (0, -1)
            i, shipId = player[self.id_property_map['shipId']] if 'shipId' in self.id_property_map else (0, 0)
            self.world.players[nickName] = {'clanColor': '#' + struct.pack('>I', clanColor).encode('hex')[2:] if clanId > 0 else ''}
            if entityId:
                self.world.players_map[entityId] = {'nickName':nickName,  'teamId':teamId, 'shipId':shipId}
            for key in self.id_property_map:
                if key != 'name' and key != 'clanColor' and player[self.id_property_map[key]]:
                    if key != 'fleetTeamId' or player[self.id_property_map[key]][1] != 0:
                        self.world.players[nickName][key] = player[self.id_property_map[key]][1]
                if key == 'fleetTeamId' and player[self.id_property_map[key]][1] != 0:
                    try:
                        self.world.fleetteams[player[self.id_property_map[key]][1]].append(nickName)
                    except:
                        self.world.fleetteams[player[self.id_property_map[key]][1]] = [nickName]
            self.world.players[nickName]['killed'] = ''
            self.world.players[nickName]['kill'] = []
            self.world.players[nickName]['killCount'] = 0
            self.world.players[nickName]['achivements'] = []
        self.world.own_player = self.world.players_map[self.world.basePlayerEntityId]


class BigWorldVehicle(BigWorldEntity):

    def shootTorpedo(self, vehicleId, data):
        arg1, = struct.unpack('I', data[0:4])
        x, = struct.unpack('I', data[4:8])
        y, = struct.unpack('I', data[8:12])
        z, = struct.unpack('I', data[12:16])
        arg3, = struct.unpack('I', data[16:20])
        arg4, = struct.unpack('I', data[20:24])
        arg5, = struct.unpack('I', data[24:28])
        arg6, = struct.unpack('B', data[28:29])
        if vehicleId == self.world.baseShipEntityId and self.world.baseShipTorpedoes and arg1 == 25:
            if vehicleId not in self.world.torps:
                self.world.torps[vehicleId] = 0
            for turel, barrels in enumerate(self.world.baseShipTorpedoes):
                if arg6 == turel:
                    pass
                if arg5 == 0:
                    self.world.torps[vehicleId] += barrels
                elif arg5 == 1:
                    self.world.torps[vehicleId] -= barrels
                    self.world.torps[vehicleId] += 2
                elif arg5 > 1:
                    self.world.torps[vehicleId] += 1

    def shootGuns(self, vehicleId, data):
        arg1, = struct.unpack('H', data[0:2])
        if vehicleId == self.world.baseShipEntityId:
            
            if self.world.baseShipArtillery:
                if arg1 == 2:
                    if vehicleId not in self.world.guns:
                        self.world.guns[vehicleId] = 0
                    info, = struct.unpack('H', data[4:6])
                    for turel, barrels in enumerate(self.world.baseShipArtillery):
                        if info >> turel & 1:
                            self.world.guns[vehicleId] += barrels


class BigWorldBattleLogic(BigWorldEntity):

    def setProperty_my(self, entity_id, type, data):
        super(BigWorldBattleLogic, self).setProperty(entity_id, type, data)

    def onTimer(self, entity_id, data):
        length, = struct.unpack('I', data[0:4])
        if length == 2:
            timeLeft, = struct.unpack('H', data[4:6])
            if timeLeft == 0:
                if self.world.battleStartTime == 0.0:
                    self.world.battleStartTime = self.world.time

r = ReplayFile(sys.argv[1])
r.parse()
infolist = {}
infolist['baseinfo'] = r.get_arenainfo()
infolist['own_player'] = r.get_own_player()
infolist['result'] = r.get_battleResult()
infolist['players'] = r.get_players()
infolist['own_player'] = r.get_own_player()
infolist['flags'] = r.get_flags()
infolist['damage'] = r.get_damage()
infolist['ribbons'] = r.get_ribbons()
infolist['ChatList'] = r.get_chats()
infolist['ribbonmap'] = r.get_ribbon_map()
infolist['fleetteams'] = r.get_fleet()
print json.dumps(infolist)