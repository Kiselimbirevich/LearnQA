import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime

class TestUsetEdit(BaseCase):
    def test_edit_unauthorized_user(self):
        response = requests.put(
            f"https://playground.learnqa.ru/api/user/2",
            data={"firstName": datetime.now().strftime("%m%d%Y%H%M%S")}
        )
        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "error",
            "Auth token not supplied",
            f"Unexpected response: {response.content}"
        )

    def test_edit_user_with_another_credentials(self):
        data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        created_user_id = int(response1.json()["id"])

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{created_user_id - 1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": datetime.now().strftime("%m%d%Y%H%M%S")}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "This user can only edit their own data.",
            f"Unexpected response, gor {response3.content}"
        )

    def test_edit_email_without_symbol(self):
        data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id = self.get_json_value(response1, "id")

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": f'{datetime.now().strftime("%m%d%Y%H%M%S")}example.com'}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Invalid email format",
            f"Unexpected response, gor {response3.content}"
            )

    def test_edit_firstName_with_one_symbol(self):
        data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id = self.get_json_value(response1, "id")

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": "e"}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "The value for field `firstName` is too short",
            f"Unexpected response, gor {response3.content}"
            )

