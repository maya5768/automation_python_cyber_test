import time
from pages.base_page import BasePage


class LoginPage(BasePage):
    LOGIN_URL    = "https://tutorialsninja.com/demo/index.php?route=account/login"
    REGISTER_URL = "https://tutorialsninja.com/demo/index.php?route=account/register"

    def login(self, email: str, password: str) -> bool:
        self.navigate(self.LOGIN_URL)
        self.page.fill("#input-email", email)
        self.page.fill("#input-password", password)
        self.page.click("input[type='submit'][value='Login']")
        self.page.wait_for_load_state("networkidle")
        return self.page.locator("a[href*='account/logout']").count() > 0

    def register(self, email: str, password: str) -> bool:
        self.navigate(self.REGISTER_URL)
        self.page.fill("#input-firstname", "Test")
        self.page.fill("#input-lastname",  "User")
        self.page.fill("#input-email",     email)
        self.page.fill("#input-telephone", "0501234567")
        self.page.fill("#input-password",  password)
        self.page.fill("#input-confirm",   password)
        self.page.check("input[name='agree']")
        self.page.click("input[value='Continue']")
        self.page.wait_for_load_state("networkidle")
        return "success" in self.page.url

    def login_or_register(self, email: str, password: str) -> bool:
        if self.login(email, password):
            return True
        unique_email = f"test_{int(time.time())}@auto.com"
        self.register(unique_email, password)
        return self.login(unique_email, password)
