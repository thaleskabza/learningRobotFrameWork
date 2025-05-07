# runners/test_runner.py
import pytest
from pytest_bdd import scenarios, parsers, given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from datetime import datetime
import os
import csv
from models.user_data import UserData
from pages.web_tables_page import WebTablesPage

# Global variables to share state between steps
current_scenario = None
driver = None
web_tables_page = None
latest_user = None

@pytest.fixture
def setup(request):
    global driver, web_tables_page
    hub_url = os.getenv("SELENIUM_HUB_URL", "http://host.docker.internal:4444/wd/hub")
    
    capabilities = DesiredCapabilities.CHROME.copy()
    driver = webdriver.Remote(command_executor=hub_url, options=webdriver.ChromeOptions())
    
    web_tables_page = WebTablesPage(driver)
    
    def teardown():
        if driver:
            driver.quit()
    
    request.addfinalizer(teardown)
    return driver, web_tables_page

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    if driver:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"error_{scenario.name}_{step.name}_{timestamp}.png"
        driver.save_screenshot(screenshot_name)
        print(f"Screenshot saved as {screenshot_name}")

def get_user_data_from_csv(file_name, row_index):
    users = []
    file_path = f"testdata/{file_name}"
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user = UserData(
                first_name=row['FirstName'],
                last_name=row['LastName'],
                username=row['UserName'],
                password=row['Password'],
                company=row['Company'],
                role=row['Role'],
                email=row['Email'],
                mobile_phone=row['Mobilephone']
            )
            users.append(user)
    return users[row_index]

# Step definitions
@given("User navigate to <url>")
def user_navigate_to(url, setup):
    driver.get(url)
    time.sleep(1)

@then("User should see the user list table with headers:")
def verify_user_list_table_headers(setup, datatable):
    assert web_tables_page.is_user_list_table_displayed(), "User list table is not displayed"
    expected_headers = [row['Header'] for row in datatable]
    actual_headers = web_tables_page.get_header_list()
    assert actual_headers == expected_headers, f"Expected headers {expected_headers} but got {actual_headers}"

@when("User click <button_text>")
def user_click_button(button_text, setup):
    if button_text.lower() == "add user":
        web_tables_page.click_add_user()
    else:
        driver.find_element(By.XPATH, f"//button[contains(text(),'{button_text}')]").click()
    time.sleep(1)

@when("User add a user with data:")
def add_user_with_data(setup, datatable):
    for row in datatable:
        user = UserData(
            first_name=row['firstName'],
            last_name=row['lastName'],
            username=f"{row['userName']}_{int(time.time())}",
            password=row['password'],
            company=row['customer'],
            role=row['role'],
            email=row['email'],
            mobile_phone=row['cellPhone']
        )
        global latest_user
        latest_user = user
        
        web_tables_page.click_add_user()
        web_tables_page.add_user(user)
        web_tables_page.click_save_button()
    time.sleep(1)

@then("User should see the user <username> in the user list with details:")
def verify_user_in_list(username, setup, datatable):
    assert web_tables_page.is_user_present_in_list(username), f"User {username} not found"
    
    rows = driver.find_elements(By.CSS_SELECTOR, "table.smart-table.table-striped tbody tr")
    row_elem = next((r for r in rows if username in r.text), None)
    assert row_elem is not None, f"Row for user {username} not found"
    
    expected_data = datatable[0]
    cells = row_elem.find_elements(By.TAG_NAME, "td")
    
    assert cells[0].text == expected_data['First Name']
    assert cells[1].text == expected_data['Last Name']
    assert cells[2].text == username
    assert cells[3].text == expected_data['Customer']
    assert cells[4].text == expected_data['Role']
    assert cells[5].text == expected_data['E-mail']
    assert cells[6].text == expected_data['Cell Phone']
    time.sleep(1)

@given("User load user data from CSV file <file_name> row <row_index>")
def load_user_data_from_csv(file_name, row_index, setup):
    global latest_user
    latest_user = get_user_data_from_csv(file_name, int(row_index))
    time.sleep(1)

@when("User add the latest user")
def add_latest_user(setup):
    web_tables_page.click_add_user()
    web_tables_page.add_user(latest_user)
    time.sleep(1)

@then("User should see the latest user in the user list")
def verify_latest_user_in_list(setup):
    assert web_tables_page.is_user_present_in_list(latest_user.username), \
        f"Latest user not found: {latest_user.username}"
    time.sleep(1)

@when("I pause for one minute")
def pause_for_one_minute(setup):
    time.sleep(60)