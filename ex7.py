import requests
from json import JSONDecodeError

# Первый вопрос
print(requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type").text)

# Второй вопрос
print(requests.patch("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":"PATCH"}).text)

# Третий запрос
print(requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method":"GET"}).text)

# Цикл

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
all_methods = ["GET", "POST", "PUT", "DELETE"]

for i in all_methods:
    for n in all_methods:
        if i == "GET":
            rq = requests.get(url, params={"method":n})
        if i == "POST":
            rq = requests.post(url, data={"method": n})
        if i == "PUT":
            rq = requests.put(url, data={"method": n})
        if i == "DELETE":
            rq = requests.delete(url, data={"method": n})

        try:
            json_resp = rq.json()
        except JSONDecodeError:
            print(f"{i} and method:{n} возвращает НЕ JSON, в payload: {rq.text}")
            continue

        if i != n and "success" in rq.json():
            print(f'Данная комбинация {i} и method:{n} возвращает "success"')
        elif i == n and "success" not in rq.json():
            print(f'Данная комбинация {i} и method:{n} НЕ возвращает "success"')