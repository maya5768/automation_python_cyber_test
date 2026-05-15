import os
import pytest
import allure
from pages.login_page import LoginPage
from tests.conftest import load_cases


class TestLogin:
    @pytest.mark.parametrize("case", load_cases("login_data.json"), ids=lambda c: c["id"])
    @allure.title("Login: {case[id]}")
    def test_login(self, page, case):
        email    = os.getenv("TEST_EMAIL",    case["email"])
        password = os.getenv("TEST_PASSWORD", case["password"])

        login = LoginPage(page)
        if case["expected"] == "success":
            success = login.login_or_register(email, password)
        else:
            success = login.login(email, password)

        if case["expected"] == "success":
            assert success, f"Login should succeed for {email}"
        else:
            assert not success, f"Login should fail for {email}"
            # Verify the site displays an error alert (not just a silent failure)
            assert page.locator("div.alert-danger").count() > 0, \
                f"Expected error alert on failed login for {email}"
