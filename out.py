import copy
import datetime
import httpx
import orjson
import random
import spade


class user(spade.agent.Agent):
    def __init__(self, jid, password, backup_method = None, backup_queue = None, backup_url = None, backup_period = 60, backup_delay = 0, logger = None, **kwargs):
        super().__init__(jid, password, verify_security=False)
        if logger: logger.debug(f'[{jid}] Received parameters: jid: {jid}, password: {password}, backup_method: {backup_method}, backup_queue: {backup_queue}, backup_url: {backup_url}, backup_period: {backup_period}, backup_delay: {backup_delay}, kwargs: {kwargs}')
        self.logger = logger
        self.backup_method = backup_method
        self.backup_queue = backup_queue
        self.backup_url = backup_url
        self.backup_period = backup_period
        self.backup_delay = backup_delay
        self.connections = kwargs.get("connections", [])
        self.msgRCount = self.limit_number(kwargs.get("msgRCount", 0))
        self.msgSCount = self.limit_number(kwargs.get("msgSCount", 0))
        self.counter = self.limit_number(kwargs.get("counter", 0))
        self.num_seen_photos = self.limit_number(kwargs.get("num_seen_photos", 0))
        self.friends = kwargs.get("friends", [])
        self.numbers = kwargs.get("numbers", [])
        self.datum = UUID.uuid__init()
        if self.logger: self.logger.debug(f'[{self.jid}] Class dict after initialization: {self.__dict__}')
    
    @property
    def connCount(self):
        return self.limit_number(len(self.connections))
    
    def limit_number(self, value):
        return float(max(-2147483648, min(value, 2147483647)))
    
    def get_json_from_spade_message(self, msg):
        return orjson.loads(msg.body)
    
    def get_spade_message(self, receiver_jid, body):
        msg = spade.message.Message(to=receiver_jid)
        body["sender"] = str(self.jid)
        msg.metadata["type"] = body["type"]
        msg.metadata["performative"] = body["performative"]
        msg.body = str(orjson.dumps(body), encoding="utf-8")
        return msg
    
    def setup(self):
        if self.backup_method is not None:
            BackupBehaviour_template = spade.template.Template()
            BackupBehaviour_template.set_metadata("reserved", "no_message_match")
            self.add_behaviour(self.BackupBehaviour(start_at=datetime.datetime.now() + datetime.timedelta(seconds=self.backup_delay), period=self.backup_period), BackupBehaviour_template)
        initialize_template = spade.template.Template()
        initialize_template.set_metadata("reserved", "no_message_match")
        self.add_behaviour(self.initialize(), initialize_template)
        facebook_activity_template = spade.template.Template()
        facebook_activity_template.set_metadata("reserved", "no_message_match")
        self.add_behaviour(self.facebook_activity(period=30), facebook_activity_template)
        read_posts_template = spade.template.Template()
        read_posts_template.set_metadata("type", "facebook_post")
        read_posts_template.set_metadata("performative", "query")
        self.add_behaviour(self.read_posts(), read_posts_template)
        if self.logger: self.logger.debug(f'[{self.jid}] Class dict after setup: {self.__dict__}')
    
    class BackupBehaviour(spade.behaviour.PeriodicBehaviour):
        def __init__(self, start_at, period):
            super().__init__(start_at=start_at, period=period)
            self.http_client = httpx.AsyncClient(timeout=period)
        
        async def run(self):
            data = {
                "__timestamp__": int(datetime.datetime.timestamp(datetime.datetime.utcnow())),
                "jid": str(self.agent.jid),
                "type": "user",
                "floats": {
                    "msgRCount": self.agent.msgRCount,
                    "msgSCount": self.agent.msgSCount,
                    "connCount": self.agent.connCount,
                    "counter": self.agent.counter,
                    "num_seen_photos": self.agent.num_seen_photos,
                },
                "enums": {
                },
                "connections": {
                    "connections": self.agent.connections,
                    "friends": self.agent.friends,
                },
                "messages": {
                },
                "float_lists": {
                    "numbers": self.agent.numbers,
                },
            }
            if self.agent.backup_method == 'http':
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Sending backup data with http: {data}')
                try:
                    await self.http_client.post(self.agent.backup_url, headers={"Content-Type": "application/json"}, data=orjson.dumps(data))
                except Exception as e:
                    if self.agent.logger: self.agent.logger.error(f'[{self.agent.jid}] Backup error type: {e.__class__}, additional info: {e}')
            elif self.agent.backup_method == 'queue':
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Sending backup data with queue: {data}')
                try:
                    await self.agent.backup_queue.coro_put(data)
                except Exception as e:
                    if self.agent.logger: self.agent.logger.error(f'[{self.agent.jid}] Backup error type: {e.__class__}, additional info: {e}')
            else:
                if self.agent.logger: self.agent.logger.warning(f'[{self.agent.jid}] Unknown backup method: {self.agent.backup_method}')
    
    class initialize(spade.behaviour.OneShotBehaviour):
        def initialize_friends(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action initialize_friends')
            
            # float declaration
            max_friends = self.agent.limit_number(0)
            
            # length
            max_friends = self.agent.limit_number(len(self.agent.connections))
            
            # float declaration
            num_friends = self.agent.limit_number(0)
            
            # uniform distribution
            num_friends = self.agent.limit_number(random.uniform(self.agent.limit_number(0), self.agent.limit_number(max_friends)))
            
            # round
            num_friends = self.agent.limit_number(round(self.agent.limit_number(num_friends)))
            
            # subset
            if int(self.agent.limit_number(round(self.agent.limit_number(num_friends)))) <= 0:
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Non-positive subset size (rounded): {int(self.agent.limit_number(round(self.agent.limit_number(num_friends))))}')
                return
            self.agent.friends = [copy.deepcopy(elem) for elem in random.sample(self.agent.connections, min(int(self.agent.limit_number(round(self.agent.limit_number(num_friends)))), int(self.agent.limit_number(len(self.agent.connections)))))]
        
        async def run(self):
            self.initialize_friends()
    
    class facebook_activity(spade.behaviour.PeriodicBehaviour):
        async def post_photos(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action post_photos')
            send = { "type": "facebook_post", "performative": "query", "photos": 0.0, "msg_id": UUID.uuid__init(), }
            
            # float declaration
            num_photos = self.agent.limit_number(0)
            
            # module variable declaration
            to_send_id = UUID.uuid__init()
            
            # uniform distribution
            num_photos = self.agent.limit_number(random.uniform(self.agent.limit_number(21), self.agent.limit_number(37)))
            
            # round
            num_photos = self.agent.limit_number(round(self.agent.limit_number(num_photos)))
            
            # add element
            self.agent.numbers.append(num_photos)
            
            # module instruction GETUUID
            to_send_id = UUID.GETUUID(to_send_id)
            
            # set
            send["photos"] = self.agent.limit_number(num_photos)
            
            # set
            send["msg_id"] = to_send_id
            
            # send
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Send message {send} to {self.agent.friends}')
            for receiver in self.agent.friends:
                await self.send(self.agent.get_spade_message(receiver, send))
                self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)
        
        async def run(self):
            await self.post_photos()
    
    class read_posts(spade.behaviour.CyclicBehaviour):
        def update_seen_photos(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action update_seen_photos')
            
            # add
            self.agent.num_seen_photos = self.agent.limit_number(self.agent.num_seen_photos + self.agent.limit_number(rcv["photos"]))
            
            # module variable declaration
            random_id = UUID.uuid__init()
            
            # module instruction GETUUID
            random_id = UUID.GETUUID(random_id)
            
            # module instruction ISEQ
            if UUID.ISEQ(rcv["msg_id"], random_id):
                
                # clear
                self.agent.friends.clear()
            
            # module instruction ISNEQ
            if UUID.ISNEQ(rcv["msg_id"], random_id):
                
                # add
                self.agent.num_seen_photos = self.agent.limit_number(self.agent.num_seen_photos + self.agent.limit_number(1))
            
            # module instruction SUM
            self.agent.numbers = LISTS.SUM(self.agent.numbers, self.agent.counter)
        
        async def run(self):
            rcv = await self.receive(timeout=100000)
            if rcv:
                rcv = self.agent.get_json_from_spade_message(rcv)
                self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')
                self.update_seen_photos(rcv)
    

import random
import uuid
import numpy


class Agent:
    def __init__(self, jid: str, type: str, connections = None, sim_id: str = ''):
        self.jid = jid
        self.type = type
        self.sim_id = sim_id
        if connections is not None:
            self.connections = connections
        else:
            self.connections = []
    
    def add_connection(self, connection: str):
        self.connections.append(connection)
    def to_dict(self):
        return {
            'jid': self.jid,
            'type': self.type,
            'connections': self.connections,
            'sim_id': self.sim_id
            }


def generate_graph_structure(domain, sim_id=""):
    agent_types = []
    _num_user = 150
    tmp = ['user'] * _num_user
    agent_types.extend(tmp)
    num_agents = _num_user
    random.shuffle(agent_types)
    if sim_id == "":
        random_id = str(uuid.uuid4())[:5]
    else:
        random_id = sim_id
    m0 = 5
    m = 3
    jids = [f"{i}_{random_id}@{domain}" for i in range(num_agents)]
    connection_lists = []
    next_agent_idx = 0
    init_jids = random.choices(jids, k=m0)
    for jid in init_jids:
        copy = init_jids.copy()
        copy.remove(jid)
        connection_lists.append(copy)
    next_agent_idx += m0
    for i in range(m0, num_agents):
        to_connect = []
        ids = list(range(next_agent_idx))
        while len(to_connect) < m:
            weights = [len(connection_lists[i]) for i in ids]
            to_connect.append(random.choices(ids, weights=weights)[0])
            ids.remove(to_connect[-1])
        to_connect_jids = [jids[i] for i in to_connect]
        connection_lists.append(to_connect_jids)
        for id in to_connect:
            connection_lists[id].append(jids[next_agent_idx])
        next_agent_idx += 1
    agents = []
    for i in range(num_agents):
        agents.append({
            "jid": jids[i],
            "type": agent_types[i],
            "connections": connection_lists[i],
            "sim_id": random_id,
        })
    return agents



# Module: UUID
# Simple module to use uuids.
# Provides functionality to utilise uuids.
# targets: spade
# Introduces one type: uuid.
# Instructions:
# GETUUID will generate a new uuid and store it in the declared variable.
# ISEQ will compare two uuids and return true if they are equal.
# ISNEQ will compare two uuids and return true if they are not equal.

import uuid


def GETUUID(a):
    return str(uuid.uuid4())


def ISEQ(a, b):
    if a == b:

        return True

    return False


def ISNEQ(a, b):
    if a != b:

        return True

    return False


def TEST(a, b):
    return a




# Module: LISTS
# targets: spade
# Instructions:
# GETUUID will generate a new uuid and store it in the declared variable.
# ISEQ will compare two uuids and return true if they are equal.
# ISNEQ will compare two uuids and return true if they are not equal.


def SUM(a, dst):
    return sum(a)


