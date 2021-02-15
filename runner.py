from scripts.QLearner import QLearner
from agents.a2c import A2CAgent
from scripts.env import env
import requests
import torch
import uuid

torch.manual_seed(10)

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
    agent_id = uuid.uuid4()
    env = env('GRID WORLD', agent_id)
    agent = A2CAgent(env.observation_space, env.action_space, name=agent_id)

    num_eps = 1000
    for i in range(num_eps):
        trajectory = []
        total = 0
        done = False
        curr_state  = env.reset()

        while not done:
            action = agent.choose_action(curr_state)
            next_state, reward, done = env.step(action.numpy())

            total += reward
            trajectory.append((curr_state, action, reward, next_state, done))

        print(f"Episode {i} Total R: {total}")
        agent.store_trajectory(trajectory)
        agent.learn()

    # get_optimal(agent.Q)