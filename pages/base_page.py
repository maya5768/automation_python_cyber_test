import os
from playwright.sync_api import Page


# Base class for all page objects.
# Centralizes shared browser actions so subclasses don't duplicate code.
class BasePage:

    # Receives the Playwright Page object and stores it for use by all subclasses.
    def __init__(self, page: Page):
        self.page = page

    # Navigates to the given URL.
    # Wraps page.goto so navigation behavior can be changed in one place.
    def navigate(self, url: str):
        self.page.goto(url)

    # Takes a screenshot and saves it under screenshots/<name>.png.
    # Called from tests and conftest for failure evidence and debugging.
    def take_screenshot(self, name: str):
        os.makedirs("screenshots", exist_ok=True)
        self.page.screenshot(path=f"screenshots/{name}.png")
