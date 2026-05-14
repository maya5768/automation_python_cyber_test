# Automation Project – TutorialsNinja E2E

End-to-End automation tests for [tutorialsninja.com/demo](https://tutorialsninja.com/demo) using Python, Playwright, and Page Object Model.

## Architecture

```
automation_python_cyber_test/
├── pages/                  ← Page Object Model
│   ├── base_page.py        ← shared base class
│   ├── home_page.py        ← search
│   ├── login_page.py       ← login / register
│   ├── search_results_page.py  ← results + paging (XPath)
│   ├── product_page.py     ← add to cart + variants
│   └── cart_page.py        ← cart total assertion
├── tests/
│   ├── conftest.py         ← fixtures (browser, tracing, screenshots)
│   ├── test_login.py
│   ├── test_search.py
│   └── test_cart.py
├── fixtures/               ← test data (Data-Driven)
│   ├── login_data.json
│   ├── search_data.json
│   └── cart_data.json
├── utils/
│   └── price_parser.py     ← "$110.00" → 110.0
├── config/
│   └── settings.json       ← base_url, profiles
├── reports/
├── screenshots/
├── pytest.ini
└── ReadMeAIBugs.md
```

## Prerequisites

- Python 3.10+
- venv with dependencies installed (`playwright`, `pytest`, `allure-pytest`)

## Running the Tests

**Install browser (once):**
```bash
venv\Scripts\playwright install chromium
```

**Run all tests (headless):**
```bash
venv\Scripts\pytest tests\ -v
```

**Run with visible browser:**
```bash
venv\Scripts\pytest tests\ -v --headed
```

**Run with Allure report:**
```bash
venv\Scripts\pytest tests\ -v --alluredir=reports\allure-results
allure generate reports\allure-results -o reports\allure-report --clean
allure open reports\allure-report
```

**ENV variable overrides:**
```bash
BASE_URL=https://tutorialsninja.com/demo/ TEST_EMAIL=me@test.com pytest tests\
```

## Design Principles

| Principle | Implementation |
|-----------|----------------|
| **POM** | one class per page under `pages/` |
| **OOP** | all pages inherit from `BasePage` |
| **SRP** | each class has a single responsibility |
| **Data-Driven** | test cases loaded from `fixtures/*.json` via `@pytest.mark.parametrize` |
| **XPath** | `search_results_page.py` uses relative XPath to extract product links and prices |

## Assumptions & Limitations

- Login: if the test account does not exist, a new account is registered automatically with a unique timestamped email.
- Currency: prices are assumed to be in USD (`$`).
- Cart total: validated against `budget_per_item × number_of_items`.
- Guest checkout is not used; a registered account is required.

## Reports

- **Allure** – `reports/allure-results/` (generated per run)
- **Playwright Trace** – `reports/traces/<test_name>.zip` (open with `playwright show-trace`)
- **Screenshots** – `screenshots/` (saved on failure and after each cart addition)
