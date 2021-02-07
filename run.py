import requests
import argparse
import random
import time

class Agent():
    def __init__(self, agent_identifier, env_address, **kwargs):
        self.id = agent_identifier
        self.env_address = env_address

        my_dict = kwargs
        requests.post(self.env_address + "/i?id={}".format(self.id), json = my_dict)

    def select_action(self, state):
        action = random.randrange(0, 4)

        my_dict = {}
        my_dict["action"] = action
        requests.post(self.env_address + "/s?id={}".format(self.id), json = my_dict)
        return action
    
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
    agent = Agent("test", args.address)

    for i in range(num_eps):
        done = False
        curr_state, _, _ = agent.make_observation()
        print("Start State: {}".format(curr_state))

        while not done:
            action = agent.select_action(curr_state)
            curr_state, reward, done = agent.make_observation()
            print("Action: {}, Next State: {}".format(action, curr_state))