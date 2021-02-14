import random
from flask import Flask, request, jsonify
import requests
import time

ENVIRONMENT_URL = 'http://127.0.0.1:5000/environment' 
ACTION_URL = 'http://127.0.0.1:5000/action'

def send_action(env, agent_uuid, action): 
    payload = {'uuid': str(agent_uuid), 'env': env}
    if action != None: payload['action'] = action
    response = requests.post(ACTION_URL, json=payload)

def get_observation(env, agent_uuid): 
    while True: 
        response = requests.get(ENVIRONMENT_URL, params={'uuid': agent_uuid})
        if response.status_code == 200: 
            responseJson = response.json()
            state = responseJson['next_state']
            reward = responseJson['reward']
            done = responseJson['done']
            return state, reward, done

class env():
    def __init__(self, env_name, agent_id):
        self.env_name = env_name
        self.agent_id = agent_id

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