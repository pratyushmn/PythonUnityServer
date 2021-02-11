from scripts.QLearner import QLearner
import requests
import torch

from requests.models import Response

ENVIRONMENT_URL = 'http://127.0.0.1:5000/environment' 
ACTION_URL = 'http://127.0.0.1:5000/action'
torch.manual_seed(150)

def get_observation(): 
    while True: 
        respone = requests.get(ENVIRONMENT_URL)
        if respone.status_code == 200: 
            responeJson = respone.json()
            state = responeJson['next_state']
            reward = responeJson['reward']
            done = responeJson['done']
            return state, reward, done

def send_action(agent_uuid, action): 
    payload = {'uuid': str(agent_uuid)}
    if action != None: payload['action'] = action
    respone = requests.post(ACTION_URL, json=payload)

def get_optimal(Q):
    print("\n> Optimal Policy ")
    grid = torch.zeros(8,8)
    for height in range(8): 
        for width in range(8): 
            grid[width][height] = torch.argmax(Q[:,height,width]).item()
            
    blanks = [(1, 1), (6, 3), (1, 5), (4, 5)]
    print('+---' * 8 + "+")
    for x in range(8):
        for y in range (8):
            if (x,y) in blanks: print("|   ", end='')
            else:
                if grid[x][y] == 0: print("| \u2192 ", end='')
                elif grid[x][y] == 1: print("| \u2190 ", end='')
                elif grid[x][y] == 2: print("| \u2193 ", end='')
                elif grid[x][y] == 3: print("| \u2191 ", end='')
        print('|\n' + '+---' * 8 + "+")

if __name__ == '__main__':
    agent = QLearner()
    num_eps = 500
    for i in range(num_eps):
        send_action(agent.uuid, None)
        curr_state, done, _ = get_observation()
        #print(f"Start State: {curr_state}")
        while not done:
            action = agent.make_move(curr_state)
            send_action(agent.uuid, action)
            next_state, reward, done = get_observation()
            curr_state = agent.update(action, curr_state, next_state, reward)
            #print("Action: {}, Next State: {} {} {}".format(action, next_state, done, i))
        print(f"Episode {i} Total R - {agent.total_reward}")
        agent.reset()
    get_optimal(agent.Q)