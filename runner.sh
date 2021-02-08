echo ">> Running the Scripts"
echo "Starting the server"
echo "Starting the environment"
echo "Running the agent"

python scripts/server.py &
python scripts/env.py &
python scripts/agent.py &