import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):
    def test_get_user_details_auth_as_another_user(self):
        data = {
            'email': "vinkotov@example.com",
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = requests.get(
        f"https://playground.learnqa.ru/api/user/3",
        headers={"x-csrf-token": token},
        cookies={"auth_sid": auth_sid}
        )

        response_data = response2.json()
        assert set(response_data.keys()) == {"username"}, f"Ожидался только 'username', но есть и другие"
        current_username = self.get_json_value(response2, "username")
        assert current_username !=1, f"Отображается юзернейм под которым была авторизация"