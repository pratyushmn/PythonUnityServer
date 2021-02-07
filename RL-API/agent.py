import requests
import random
import uuid

from requests.models import Response

ENVIRONMENT_URL = 'http://127.0.0.1:5000/environment' 
ACTION_URL = 'http://127.0.0.1:5000/action'

def initialize(uuid_p): 
    payload = {
        'agent_uuid': str(uuid_p)
    }
    respone = requests.post(ACTION_URL, json=payload)
    print(respone)

def get_observation(): 
    while True: 
        respone = requests.get(ENVIRONMENT_URL)
        if respone.status_code == 200: 
            responeJson = respone.json()
            state = responeJson['next_state']
            reward = responeJson['reward']
            done = responeJson['done']
            return state, reward, done

def send_action(uuid_p, action): 
    payload = {
        'agent_uuid': str(uuid_p), 
        'action': action
    }
    respone = requests.post(ACTION_URL, json=payload)
    print(respone)

if __name__ == '__main__':
    num_eps = 30
    print("Here")
    uuid_p = uuid.uuid4() 
    for i in range(num_eps):
        initialize(uuid_p)
        done = False
        curr_state, _, _ = get_observation()
        print(f"Start State: {curr_state}")
        while not done:
            action = random.randrange(0, 4)
            send_action(uuid_p, action)
            curr_state, reward, done = get_observation()
            print("Action: {}, Next State: {} {} {}".format(action, curr_state, done, i))
