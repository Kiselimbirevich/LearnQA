import requests

resp = requests.get("https://playground.learnqa.ru/api/long_redirect")
print(len(resp.history))
print(resp.url)