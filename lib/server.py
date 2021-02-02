from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to ECE231!"

@app.route("/hello")
def simple():
    return "Hello, Pratyush!"

    
if __name__ == "__main__":
    app.run(debug=True)