from lib.my_requests import MyRequests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import allure

@allure.epic("Registration cases")
class TestUserRegister(BaseCase):
    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    @allure.description("This test successfully creates new user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test attempts to create new user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"unexpected response content {response.content}"

    @allure.description("This test attempts to create new user without @ in e-mail")
    def test_create_user_without_symbol(self):
        email = f'{datetime.now().strftime("%m%d%Y%H%M%S")}example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", f"unexpected response content {response.content}"

    @allure.description("This test attempts to create new user without required parameter")
    @pytest.mark.parametrize("missing_parameter", ["password", "username", "firstName", "lastName", "email"])
    def test_create_user_without_required_parameter(self, missing_parameter):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        data.pop(missing_parameter)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missing_parameter}", f"unexpected response content {response.content}"

    # генераторов не будет
    @allure.description("This test attempts to create new user with 1-symbol username")
    def test_create_user_with_short_username(self):
        email = f'{datetime.now().strftime("%m%d%Y%H%M%S")}@example.com'
        data = {
            'password': '123',
            'username': '1',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", f"unexpected response content {response.content}"

    # генераторов не будет часть 2
    @allure.description("This test attempts to create new user with long username")
    def test_create_user_with_long_username(self):
        email = f'{datetime.now().strftime("%m%d%Y%H%M%S")}@example.com'
        data = {
            'password': '123',
            'username': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopq',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", f"unexpected response content {response.content}"
