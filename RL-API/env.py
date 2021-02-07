import random
from flask import Flask, request, jsonify
import requests

ACTION_URL = 'http://127.0.0.1:5000/action'
ENV_URL = 'http://127.0.0.1:5000/environment'

class GridWorldEnv():
    def __init__(self, width = 8, height = 8, treasures = [(1, 1)], pits = [(2, 3), (4, 4), (7, 8)]):
        self.width = width
        self.height = width
        self.treasures = treasures
        self.pits = pits
        self.agents = {}
        self.new_obs = set()

    def run(self):
        while True:
            r = requests.get(ACTION_URL)

            if r:
                agent_uuid = r.get("agent_uuid", None)
                action = r.get("action", None)

                if not agent_uuid: return

                if not action:
                    self.initialize_agent(agent_uuid)
                    output = {}
                    output["next_state"] = self.agents[agent_uuid][0]
                    output["reward"] = self.agents[agent_uuid][1]
                    output["done"] = self.agents[agent_uuid][2]

                    requests.post(ENV_URL, data=output)
                else:
                    next_state = self.act(agent_uuid, action)
                    reward = 0
                    done = False

                    if next_state in self.treasures:
                        reward = 1
                        done = True
                    elif next_state in self.pits:
                        reward = -1
                        done = True

                    self.new_obs.add(agent_uuid)
                    self.agents[agent_uuid] = (next_state, reward, done)

                    output = {}
                    output["next_state"] = next_state
                    output["reward"] = reward
                    output["done"] = done

                    requests.post(ENV_URL, data=output)
    
    # def observe(self):
    #     if 'id' in request.args:
    #         agent_identifier = request.args['id']
    #         if agent_identifier in self.new_obs:
    #             self.new_obs.remove(agent_identifier)
    #             info = {}
    #             info["next_state"] = self.agents[agent_identifier][0]
    #             info["reward"] = self.agents[agent_identifier][1]
    #             info["done"] = self.agents[agent_identifier][2]
    #             return jsonify(info)
        
    #     return None

    def act(self, agent_identifier, action):
        curr_state = self.agents[agent_identifier][0]

        if action == 0: curr_state = (min(self.width - 1, curr_state[0] + 1), curr_state[1])
        elif action == 1: curr_state = (max(0, curr_state[0] - 1), curr_state[1])
        elif action == 2: curr_state = (curr_state[0], min(self.height - 1, curr_state[1] + 1))
        elif action == 3: curr_state = (curr_state[0], max(0, curr_state[1] - 1))

        return curr_state

    def initialize_agent(self, agent_identifier, initial_state=None):
        agent_identifier = request.args['id'] if 'id' in request.args else None

        if not agent_identifier:
            return

        info = request.get_json()
        initial_state = info.get("initial_state", None)

        if initial_state:
            self.agents[agent_identifier] = (initial_state, 0, False)
        else:
            initial_state = self.rand_point()
            self.agents[agent_identifier] = (initial_state, 0, False)

    def rand_point(self):
        x = random.randrange(0, self.width)
        y = random.randrange(0, self.height)

        while (x, y) not in self.treasures and (x, y) not in self.pits:
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)
        
        return (x, y)

if __name__ == "__main__":
    env = GridWorldEnv()
    env.run()