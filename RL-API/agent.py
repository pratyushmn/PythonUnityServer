import requests
import random
import uuid

from requests.models import Response

ENVIRONMENT_URL = 'http://127.0.0.1:5000/environment' 
ACTION_URL = 'http://127.0.0.1:5000/action'

def initialize(uuid): 
    payload = {
        'agent_uuid': uuid
    }
    respone = requests.post(ACTION_URL, json=payload)

def get_observation(): 
    while True: 
        respone = requests.get(ENVIRONMENT_URL)
        if respone.status_code == 200: 
            responeJson = respone.json()
            state = responeJson['next_state']
            reward = responeJson['reward']
            done = responeJson['done']
            return state, reward, done

if __name__ == '__main__':
    num_eps = 5
    uuid_p = uuid.uuid4() 
    initialize(uuid_p)
    for i in range(num_eps):
        done = False
        curr_state, _, _ = get_observation()
        print(f"Start State: {curr_state}")
        while not done:
            action = random.randrange(0, 4)
            curr_state, reward, done = get_observation
            print("Action: {}, Next State: {}".format(action, curr_state))