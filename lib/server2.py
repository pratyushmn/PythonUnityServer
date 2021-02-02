import requests

value = input("> ")

r = requests.get(f"http://127.0.0.1:5000/a?id={value}")

print(r.text)