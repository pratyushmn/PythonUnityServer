import random
from flask import Flask, request, jsonify
import requests
import time

ACTION_URL = 'http://127.0.0.1:5000/action'
ENV_URL = 'http://127.0.0.1:5000/environment'

def get_interaction():
    while True: 
        requestResponse = requests.get(ACTION_URL, params={'env': 'GRID WORLD'})
        if requestResponse.status_code == 200: 
            return requestResponse.json()

def send_reaction(reaction): requests.post(ENV_URL, json=reaction)

class GridWorldEnv():
    def __init__(self, width = 8, height = 8, treasures = [(1, 1)], pits = [(6, 3), (1, 5), (4, 5)]):
        self.width = width
        self.height = width
        self.treasures = set(treasures)
        self.pits = set(pits)
        self.agents = {}
        self.new_obs = set()

    def run(self):
        while True: 
            interaction = get_interaction()
            agent_uuid, action = interaction.get('uuid'), interaction.get('action')
            if action != None:
                self.act(agent_uuid, action)
            else: 
                self.initialize_agent(agent_uuid)
            send_reaction(self.agents[agent_uuid])
            if self.agents[agent_uuid]['done']: del self.agents[agent_uuid]

    def act(self, agent_identifier, action):
        curr_state = self.agents[agent_identifier]['next_state']
        next_state = curr_state

        self.agents[agent_identifier]['reward'] = -0.01
        self.agents[agent_identifier]['done'] = False

        if action == 0: next_state = (min(self.width - 1, curr_state[0] + 1), curr_state[1])        #R
        elif action == 1: next_state = (max(0, curr_state[0] - 1), curr_state[1])                   #L
        elif action == 2: next_state = (curr_state[0], min(self.height - 1, curr_state[1] + 1))     #D
        elif action == 3: next_state = (curr_state[0], max(0, curr_state[1] - 1))                   #U

        if next_state in self.treasures: 
            self.agents[agent_identifier]['reward'] = 1
            self.agents[agent_identifier]['done'] = True
        elif next_state in self.pits: 
            self.agents[agent_identifier]['reward'] = -1
            self.agents[agent_identifier]['done'] = True

        self.agents[agent_identifier]['next_state'] = next_state
        self.agents[agent_identifier]['prev_state'] = curr_state
        self.new_obs.add(agent_identifier)
        self.render(agent_identifier, action=action)

    def initialize_agent(self, agent_identifier, initial_state=None):
        start = initial_state if initial_state else self.rand_point()
        self.agents[agent_identifier] = {
            'prev_state': None,
            'next_state': start, 
            'reward': 0, 
            'done': False,
            'uuid': agent_identifier
        }

    def rand_point(self):
        x = random.randrange(0, self.width)
        y = random.randrange(0, self.height)
        while (x, y) in self.treasures or (x, y) in self.pits:
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)
        return (x, y)
    
    def render(self, agent_uuid, action=None, sleep_for=0.1):
        last_state = self.agents[agent_uuid]['prev_state']
        next_state = self.agents[agent_uuid]['next_state']
        reward = self.agents[agent_uuid]['reward']
        print(f'Agent - {agent_uuid} Last State - {last_state} Action - {action} Next_State - {next_state} Reward - {reward}')
        positions = {self.agents[agent]['next_state']:agent for agent in self.agents}
        print('+---' * self.width + "+")
        for y in range(0, self.height):
            for x in range (0, self.width):
                if (x, y) in positions:
                    print("| " + positions[(x, y)][-1] + " ", end='')
                elif (x, y) in self.treasures:
                    print("| T ", end='')
                elif (x, y) in self.pits:
                    print("| P ", end='')
                else:
                    print("|   ", end='')
            print('|\n' + '+---' * self.width + "+")
        #time.sleep(sleep_for)

if __name__ == "__main__":
    env = GridWorldEnv()
    env.run()