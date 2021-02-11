from numpy import random
import torch
import numpy as np
import uuid

class QLearner(): 
    def __init__(self):  
        self.Q = torch.randn(4, 8, 8)   
        self.gamma = 0.99                  
        self.learning_rate = 0.80
        self.epsilon = 0.35
        self.picked_actions = torch.zeros(4)
        self.confidence = 0.9
        self.current_episode = 0
        self.total_reward = 0
        self.uuid = uuid.uuid4()
    
    def make_move(self, state, exploit=False): 
        if self.current_episode < 4: 
            return self.current_episode 

        if not exploit and np.random.random() <= self.epsilon:
            max_uncertainty, action = None, None
            for index in range(4):
                uncertainty = (self.confidence * np.math.sqrt(np.math.log(self.current_episode) / self.picked_actions[index]))
                if not max_uncertainty or uncertainty > max_uncertainty: 
                    max_uncertainty, action = uncertainty, index
        else:
            action = torch.argmax(self.Q[:, state[0], state[1]]).item()
        return action

    def update(self, action, state, next_state, reward): 
        oldQ = self.Q[action, state[0], state[1]].item()
        futureQ = (self.gamma * torch.max(self.Q[:, next_state[0], next_state[1]]).item())
        self.Q[action, state[0], state[1]] = (1 - self.learning_rate)*oldQ + (self.learning_rate * (reward + futureQ))
        self.picked_actions[action] += 1
        self.current_episode += 1
        self.total_reward += reward
        return next_state

    def reset(self):
        self.current_episode = 0 
        self.picked_actions = torch.zeros(4)
        self.total_reward = 0