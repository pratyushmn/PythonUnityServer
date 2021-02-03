from flask import Flask
from flask import request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

simple_lib = [
    {
        'id': 0,
        'title': 'AAAAA'
    },
    {
        'id': 1,
        'title': 'BBBBB'
    },
    {
        'id': 2,
        'title': 'CCCCC'
    }
]

@app.route("/")
def home():
    return "Welcome to ECE231!"

@app.route("/a", methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error"
    results = []

    for entry in simple_lib:
        if entry['id'] == id:
            results.append(entry)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)