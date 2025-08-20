# он же ex19
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def test_deleting_user_number_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = MyRequests.delete("/user/2", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "error",
            "Auth token not supplied",
            f"unexpected error: {response.content}"
        )

    def test_delete_just_created_user(self):
        # register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1,"id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # delete

        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)

        # get
        response4 = MyRequests.get(
            f"/user/{user_id}"
        )

        Assertions.assert_code_status(response4, 404)
        Assertions.assert_text(
            response4,
            "User not found"
        )

    def test_delete_user_with_another_credentials(self):
        data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=data)
        created_user_id = int(response1.json()["id"])

        response2 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = MyRequests.delete(
            f"https://playground.learnqa.ru/api/user/{created_user_id - 1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response3, 404)
        Assertions.assert_text(
            response3,
            "This is 404 error!\n<a href='/'>Home</a>"
        )
