from flask import Flask, request, jsonify
from flask.helpers import make_response
from yaml.tokens import AnchorToken
from scripts.lib import tools

# Local Databases (-> Move to Mongo)
AGENT_DB = r'database\agents.yml'
ENVIRONMENT_DB = r'database\envDB.yml'
ACTIONS_DB = r'database\actions.yml'

AgentDB = tools.get_content(AGENT_DB)
EnvironmentDB = tools.get_content(ENVIRONMENT_DB)
ActionDB = tools.get_content(ACTIONS_DB)

# Helpers/Validators 
get_agent = lambda agent_uuid: AgentDB.get(agent_uuid)
get_environment = lambda env_uuid: EnvironmentDB.get(env_uuid)

# Server Setup
app = Flask(__name__)
app.config['DEBUG'] = True

# Agents Routes Config
@app.route('/agents', methods=['GET'])
def get_all_agents():
    return make_response(jsonify(AgentDB), 200)

@app.route('/agents/<agent_uuid>', methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
def configure_agents(agent_uuid):
    agent_cfg = get_agent(agent_uuid)

    if request.method == 'GET': 
        if agent_cfg: return make_response(jsonify(agent_cfg), 200)
        return make_response(jsonify({'Message': f'Agent Not Found - {agent_uuid}'}), 404)

    elif request.method == 'POST': 
        if agent_cfg: return make_response(jsonify({'Message': f'Agent Already Exists - {agent_uuid}'}), 400)
        AgentDB.update({agent_uuid: request.get_json()})
        tools.save_content(AGENT_DB, AgentDB)
        return make_response(jsonify(AgentDB[agent_uuid]), 201)

    elif request.method == 'DELETE': 
        if not agent_cfg: return make_response(jsonify({'Message': f'Agent Not Found - {agent_uuid}'}), 404) 
        del AgentDB[agent_uuid]
        tools.save_content(AGENT_DB, AgentDB)
        return make_response(jsonify(AgentDB), 204)
    
    elif request.method == 'PUT': 
        response_code = 200 if agent_cfg else 201
        AgentDB[agent_uuid] = request.get_json()
        tools.save_content(AGENT_DB, AgentDB)
        return make_response(jsonify(AgentDB[agent_uuid]), response_code)

    elif request.method == 'PATCH': 
        if agent_cfg: 
            for key, values in request.get_json().items(): AgentDB[agent_uuid][key] = values
            tools.save_content(AGENT_DB, AgentDB)
            return make_response(jsonify(AgentDB[agent_uuid]), 200)
        else: 
            return make_response(jsonify({'Message': f'Agent Not Found - {agent_uuid}'}), 404) 

@app.route('/environment', methods=['GET', 'POST'])
def get_action(): 
    if request.method == 'GET': 
        if len(EnvironmentDB) > 0: 
            response = make_response(jsonify(EnvironmentDB[0]), 200)
            del EnvironmentDB[0]
            tools.save_content(ENVIRONMENT_DB, EnvironmentDB)
            return response
        else: 
            return make_response(jsonify({'Message': f'The Environment has not updated the state yet'}), 404) 
              
    elif request.method == 'POST': 
        EnvironmentDB.append(request.get_json())
        tools.save_content(ENVIRONMENT_DB, ENVIRONMENT_DB)
        return make_response(jsonify(EnvironmentDB), 200)

'''
@app.route('/environment/<env_uuid>', methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
def configure_environment(env_uuid):
    env_cfg = get_environment(env_uuid)

    if request.method == 'GET': 
        if env_cfg: return make_response(jsonify(env_cfg), 200)
        return make_response(jsonify({'Message': f'Environment Not Found - {env_uuid}'}), 404)

    elif request.method == 'POST': 
        if env_cfg: return make_response(jsonify({'Message': f'Environment Already Exists - {env_uuid}'}), 400)
        EnvironmentDB.update({env_uuid: request.get_json()})
        tools.save_content(ENVIRONMENT_DB, EnvironmentDB)
        return make_response(jsonify(EnvironmentDB[env_uuid]), 201)

    elif request.method == 'DELETE': 
        if not env_cfg: return make_response(jsonify({'Message': f'Environment Not Found - {env_uuid}'}), 404) 
        del EnvironmentDB[env_uuid]
        tools.save_content(ENVIRONMENT_DB, EnvironmentDB)
        return make_response(jsonify(EnvironmentDB), 204)
    
    elif request.method == 'PUT': 
        response_code = 200 if env_cfg else 201
        EnvironmentDB[env_uuid] = request.get_json()
        tools.save_content(ENVIRONMENT_DB, EnvironmentDB)
        return make_response(jsonify(EnvironmentDB[env_uuid]), response_code)

    elif request.method == 'PATCH': 
        if env_cfg: 
            for key, values in request.get_json().items(): EnvironmentDB[env_uuid][key] = values
            tools.save_content(ENVIRONMENT_DB, EnvironmentDB)
            return make_response(jsonify(EnvironmentDB[env_uuid]), 200)
        else: 
            return make_response(jsonify({'Message': f'Environment Not Found - {env_uuid}'}), 404) 
'''

@app.route('/action', methods=['GET', 'POST'])
def get_action(): 
    if request.method == 'GET': 
        if len(ActionDB) > 0: 
            response = make_response(jsonify(ActionDB[0]), 200)
            del ActionDB[0]
            tools.save_content(ACTIONS_DB, ActionDB)
            return response
        else: 
            return make_response(jsonify({'Message': f'No Action Found'}), 404) 

    elif request.method == 'POST': 
        ActionDB.append(request.get_json())
        tools.save_content(ACTIONS_DB, ActionDB)
        return make_response(jsonify(ActionDB), 200)

if __name__ == "__main__":
    app.run()