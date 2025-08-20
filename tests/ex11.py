import requests

def test_cookie():
    url_for_test = "https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(url_for_test)
    cookies = {}
    for cookie in response.cookies:
        cookies[cookie.name] = cookie.value

    print(cookies)

    assert "HomeWork" in cookies, "HomeWork не найден"
    assert cookies["HomeWork"] == "hw_value", "Куки не корректен"