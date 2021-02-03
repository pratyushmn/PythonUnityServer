import random
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

class GridWorldEnv():
    def __init__(self, width = 8, height = 8, treasures = [(1, 1)], pits = [(2, 3), (4, 4), (7, 8)]):
        # self.app = Flask(__name__)
        # self.app.config["DEBUG"] = True

        self.width = width
        self.height = width
        self.treasures = treasures
        self.pits = pits
        self.agents = {}
        self.new_obs = set()

    def step(self, agent_identifier, action):
        next_state = self.act(agent_identifier, action)
        reward = 0
        done = False

        if next_state in self.treasures:
            reward = 1
            done = True
        elif next_state in self.pits:
            reward = -1
            done = True

        self.new_obs.add(agent_identifier)
        self.agents[agent_identifier] = (next_state, reward, done)
    
    @app.route("/o", methods=['GET'])
    def observe(self):
        if 'id' in request.args:
            agent_identifier = request.args['id']
            if agent_identifier in self.new_obs:
                self.new_obs.remove(agent_identifier)
                info = {}
                info["next_state"] = self.agents[agent_identifier][0]
                info["reward"] = self.agents[agent_identifier][1]
                info["done"] = self.agents[agent_identifier][2]
                return jsonify(info)
        
        return None

    def act(self, agent_identifier, action):
        curr_state = self.agents[agent_identifier][0]

        if action == 0: curr_state = (min(self.width - 1, curr_state[0] + 1), curr_state[1])
        elif action == 1: curr_state = (max(0, curr_state[0] - 1), curr_state[1])
        elif action == 2: curr_state = (curr_state[0], min(self.height - 1, curr_state[1] + 1))
        elif action == 3: curr_state = (curr_state[0], max(0, curr_state[1] - 1))

        return curr_state

    def initialize_agent(self, agent_identifier, initial_state=None):
        if initial_state:
            self.agents[agent_identifier] = (initial_state, 0, False)
        else:
            initial_state = self.rand_point()
            self.agents[agent_identifier] = (initial_state, 0, False)

        return initial_state

    def rand_point(self):
        x = random.randrange(0, self.width)
        y = random.randrange(0, self.height)

        while (x, y) not in self.treasures and (x, y) not in self.pits:
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)
        
        return (x, y)

if __name__ == "__main__":
    app.run(debug=True)