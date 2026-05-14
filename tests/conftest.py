import json
import os
import pytest
import allure
from pathlib import Path


def load_cases(filename: str) -> list:
    """Load test_cases array from fixtures/<filename>."""
    base = Path(__file__).parent.parent
    with open(base / "fixtures" / filename, encoding="utf-8") as f:
        return json.load(f)["test_cases"]


@pytest.fixture(scope="session")
def settings():
    base = Path(__file__).parent.parent
    with open(base / "config" / "settings.json", encoding="utf-8") as f:
        data = json.load(f)
    data["base_url"] = os.getenv("BASE_URL", data["base_url"])
    return data


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1280, "height": 800}}


@pytest.fixture(autouse=True)
def tracing(context, request):
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    trace_path = f"reports/traces/{request.node.name}.zip"
    Path("reports/traces").mkdir(parents=True, exist_ok=True)
    context.tracing.stop(path=trace_path)
    allure.attach.file(
        trace_path,
        name="playwright-trace",
        attachment_type=allure.attachment_type.ZIP,
    )


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    rep = yield
    setattr(item, f"rep_{rep.when}", rep)
    return rep


@pytest.fixture(autouse=True)
def screenshot_on_failure(page, request):
    yield
    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        Path("screenshots").mkdir(exist_ok=True)
        path = f"screenshots/FAIL_{request.node.name}.png"
        page.screenshot(path=path)
        allure.attach.file(path, attachment_type=allure.attachment_type.PNG)
