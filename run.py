import requests
import argparse
import random
import time
from env import GridWorldEnv

class Agent():
    def __init__(self, agent_identifier, env_address):
        self.id = agent_identifier
        self.env_address = env_address
        pass

    def select_action(self, state):
        return random.randrange(0, 4)
    
    def make_observation(self):
        obs = requests.get(self.env_address + "/o?id={}".format(self.id))

        while not obs:
            time.sleep(1)
            obs = requests.get(self.env_address + "/o?id={}".format(self.id))

        return obs["next_state"], obs["reward"], obs["done"]


if __name__ == '__main__':
    # Command Line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", type=str, default=None, help="Server address")
    args = parser.parse_args()

    num_eps = 5
    env = GridWorldEnv()
    agent = Agent("test", args.address)

    for i in range(num_eps):
        env.initialize_agent("test")

        done = False
        curr_state, _, _ = agent.make_observation()
        print("Start State: {}".format(curr_state))

        while not done:
            action = agent.select_action(curr_state)
            env.step(agent.id, action)
            curr_state, reward, done = agent.make_observation()
            print("Action: {}, Next State: {}".format(action, curr_state))






