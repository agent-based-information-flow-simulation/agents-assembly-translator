import copy
import datetime
import json
import random
import httpx
import numpy
import spade


class average_user(spade.agent.Agent):
    def __init__(self, jid, password, connections, backup_url = None, backup_period = 60, backup_delay = 0, logger = None, **kwargs):
        super().__init__(jid, password, verify_security=False)
        if logger: logger.debug(f"[{jid}] Received parameters: jid: {jid}, password: {password}, connections: {connections}, backup_url: {backup_url}, backup_period: {backup_period}, backup_delay: {backup_delay}, kwargs: {kwargs}")
        self.logger = logger
        self.connections = connections
        self.backup_url = backup_url
        self.backup_period = backup_period
        self.backup_delay = backup_delay
        self.msgRCount = kwargs.get("msgRCount", 0)
        self.msgSCount = kwargs.get("msgSCount", 0)
        self.friends = kwargs.get("friends", [])
        if self.logger: self.logger.debug(f"[{self.jid}] Class dict after initialization: {self.__dict__}")
    
    @property
    def connCount(self):
        return len(self.connections)
    
    def get_json_from_spade_message(self, msg):
        return json.loads(msg.body)
    
    def get_spade_message(self, receiver_jid, body):
        msg = spade.message.Message(to=receiver_jid)
        body["sender"] = str(self.jid)
        msg.metadata["type"] = body["type"]
        msg.metadata["performative"] = body["performative"]
        msg.body = json.dumps(body)
        return msg
    
    def setup(self):
        if self.backup_url:
            self.add_behaviour(self.BackupBehaviour(start_at=datetime.datetime.now() + datetime.timedelta(seconds=self.backup_delay), period=self.backup_period))
        self.add_behaviour(self.facebook_activity(period=30))
        if self.logger: self.logger.debug(f"[{self.jid}] Class dict after setup: {self.__dict__}")
    
    class BackupBehaviour(spade.behaviour.PeriodicBehaviour):
        async def run(self):
            data = {
                "jid": str(self.agent.jid),
                "connections": self.agent.connections,
                "connCount": self.agent.connCount,
                "msgRCount": self.agent.msgRCount,
                "msgSCount": self.agent.msgSCount,
                "friends": self.agent.friends,
            }
            if self.agent.logger: self.agent.logger.debug(f"[{self.agent.jid}] Sending backup data: {data}")
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(self.agent.backup_url, json=data)
            except Exception as e:
                if self.agent.logger: self.agent.logger.warn(f"[{self.agent.jid}] Backup error: {e}")
    
    class facebook_activity(spade.behaviour.PeriodicBehaviour):
        async def post_photos(self):
            if self.agent.logger: self.agent.logger.debug(f"[{self.agent.jid}] Run action post_photos")
            send = { "type": "facebook_post", "performative": "query", "photos": 0.0, }
            num_photos = 0
            num_photos = numpy.random.normal(21, 37)
            num_photos = round(num_photos)
            send["photos"] = num_photos
            if self.agent.logger: self.agent.logger.debug(f"[{self.agent.jid}] Send message {send} to self.agent.friends")
            for receiver in self.agent.friends:
                await self.send(self.agent.get_spade_message(receiver, send))
                self.agent.msgSCount += 1
        
        async def run(self):
            await self.post_photos()
    

import random
import uuid
import numpy


def generate_graph_structure(domain):
    _num_average_user = round(100 / 100 * 150)
    num_agents = _num_average_user
    random_id = str(uuid.uuid4())[:4]
    jids = [f"{i}_{random_id}@{domain}" for i in range(num_agents)]
    agents = []
    next_agent_idx = 0
    for _ in range(_num_average_user):
        num_connections = int(numpy.random.normal(0, 15))
        num_connections = max(min(num_connections, len(jids)), 0)
        agents.append({
            "jid": jids[next_agent_idx],
            "type": "average_user",
            "connections": random.sample(jids, num_connections),
        })
        next_agent_idx += 1
    return agents
