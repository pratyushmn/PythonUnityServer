import requests

value = input("> ")

r = requests.get("http://127.0.0.1:5000/a?id={}".format(value))

print(r.text)