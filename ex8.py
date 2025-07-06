import requests
import time

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
body = response.json()

time_seconds = int(body["seconds"])
token = body["token"]
print(f"Ждем {time_seconds} секунд")

time_for_first_check = (time_seconds - 1)
time.sleep(time_for_first_check)
until_ready_check = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token":token})
until_ready_data = until_ready_check.json()
if until_ready_data.get("status") == "Job is NOT ready":
    print ("Текст проверки запроса ДО истечения времени, джоба не готова, как и ожидалось")
else:
    if until_ready_data.get("error") == "No job linked to this token":
        print("Для переданного токена не создавалась задача")
    elif until_ready_data.get("status") == "Job is ready":
        print(f"Джоба выполнена раньше времени, result:{until_ready_data['result']}")
    else:
        print("Проверь бади, тут что-то не то:", until_ready_check.text)

time.sleep(time_seconds - time_for_first_check)
ready_check = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token":token})
ready_data = ready_check.json()
if ready_data.get("status") == "Job is ready" and "result" in ready_data:
    print(f"Проверка после истечения времени, джоба выполнена, {ready_data['result']}")
else:
    print("Какой-то косяк:", ready_check.text)