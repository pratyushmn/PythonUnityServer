import random
from flask import Flask, request, jsonify
import requests
import time
import numpy as np

ENVIRONMENT_URL = 'http://127.0.0.1:5000/environment' 
ACTION_URL = 'http://127.0.0.1:5000/action'
INFO_URL = 'http://127.0.0.1:5000/info'

def send_action(env, agent_uuid, action): 
    payload = {'uuid': str(agent_uuid), 'env': env}
    if action != None: payload['action'] = action.tolist()
    response = requests.post(ACTION_URL, json=payload)

def get_observation(env, agent_uuid): 
    while True: 
        response = requests.get(ENVIRONMENT_URL, params={'uuid': agent_uuid})
        if response.status_code == 200: 
            responseJson = response.json()
            state = responseJson['next_state']
            reward = responseJson['reward']
            done = responseJson['done']
            return np.array(state), reward, done

def get_info(env):
    while True:
        response = requests.get(INFO_URL, params={'env': env})
        if response.status_code == 200:
            return response.json()

class env():
    def __init__(self, env_name, agent_id):
        self.env_name = env_name
        self.agent_id = agent_id

        info = get_info(self.env_name)
        self.action_space = info['action space']
        self.observation_space = tuple(info['observation space'])

    def reset(self):
        send_action(self.env_name, self.agent_id, None)
        return get_observation(self.env_name, self.agent_id)[0]

    def step(self, action):
        send_action(self.env_name, self.agent_id, action)
        return get_observation(self.env_name, self.agent_id)
    
    def render(self):
        pass

    def close(self):
        pass