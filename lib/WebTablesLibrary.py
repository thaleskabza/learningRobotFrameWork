# lib/WebTablesLibrary.py

import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pages.web_tables_page import WebTablesPage
from models.user_data import UserData

class WebTablesLibrary:
    """Robot keyword library wrapping WebTablesPage POM."""
    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self):
        self.driver = None
        self.page = None
        print("[INIT] WebTablesLibrary initialized. Browser not opened yet.")

    def _ensure_page_initialized(self):
        if not self.driver or not self.page:
            raise RuntimeError("❌ Browser is not opened or page object is not initialized.")

    def open_web_tables(self, grid_url='http://selenium-hub:4444/wd/hub', browser='chrome'):
        print(f"[OPEN] Attempting to open browser at: {grid_url} using: {browser.upper()}")
        try:
            caps = getattr(DesiredCapabilities, browser.upper())
            self.driver = webdriver.Remote(
                command_executor=grid_url,
                desired_capabilities=caps
            )
            self.driver.maximize_window()
            self.page = WebTablesPage(self.driver)
            self.page.navigate_to()
            print("[OPEN] ✅ Browser opened and navigated to the Web Tables page.")
        except Exception as e:
            raise RuntimeError(f"[ERROR] Failed to open browser or navigate to page: {str(e)}")

    def close_browser(self):
        if self.driver:
            print("[CLOSE] Closing browser session.")
            self.driver.quit()
        else:
            print("[CLOSE] No active browser session to close.")
        self.driver = None
        self.page = None

    def verify_user_list_table_displayed(self):
        self._ensure_page_initialized()
        if not self.page.is_user_list_table_displayed():
            raise AssertionError("❌ User list table is not displayed.")
        print("[CHECK] ✅ User list table is visible.")

    def get_header_list(self):
        self._ensure_page_initialized()
        headers = self.page.get_header_list()
        print(f"[DATA] Retrieved headers: {headers}")
        return headers

    def click_add_user(self):
        self._ensure_page_initialized()
        print("[ACTION] Clicking 'Add User' button.")
        self.page.click_add_user()

    def add_user_from_csv(self, file_name, row_index=0):
        self._ensure_page_initialized()
        csv_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'resources', 'testdata', file_name
        )

        if not os.path.isfile(csv_path):
            raise FileNotFoundError(f"[ERROR] ❌ CSV file not found at: {csv_path}")

        print(f"[DATA] Reading user data from: {csv_path}, row: {row_index}")
        with open(csv_path, newline='', encoding='utf-8') as f:
            data = list(csv.DictReader(f))[int(row_index)]

        user = UserData(
            first_name=data.get('FirstName', ''),
            last_name=data.get('LastName', ''),
            username=f"{data.get('userName', '')}_{int(time.time())}",
            password=data.get('Password', ''),
            company=data.get('customer', ''),
            role=data.get('Role', ''),
            email=data.get('Email', ''),
            mobile_phone=data.get('CellPhone', '')
        )

        self.click_add_user()
        self.page.add_user(user)
        print(f"[ADD] ✅ User added with username: {user.username}")
        return user.username

    def user_should_be_present_in_list(self, username):
        self._ensure_page_initialized()
        if not self.page.is_user_present_in_list(username):
            raise AssertionError(f"[ASSERT] ❌ User '{username}' not found in the user list.")
        print(f"[ASSERT] ✅ User '{username}' is present in the user list.")

    def is_browser_open(self):
        status = self.driver is not None and self.page is not None
        print(f"[STATUS] Is browser open? {status}")
        return status

    def validate_user_list_table(self, expected_headers):
        """
        Validate that the user list table is displayed and that the headers
        exactly match the expected_headers list (including 'Action').
        """
        self._ensure_page_initialized()

        # 1) ensure the table is visible
        if not self.page.is_user_list_table_displayed():
            raise AssertionError("❌ User list table is not displayed.")
        print("[CHECK] ✅ User list table is visible.")

        # 2) fetch the actual headers
        actual_headers = self.page.get_header_list()
        print(f"[DATA] Retrieved headers for validation: {actual_headers}")

        # 3) ensure 'Action' header is present
        if 'Action' not in actual_headers:
            raise AssertionError("❌ 'Action' header is missing.")
        print("[CHECK] ✅ 'Action' header is present.")

        # 4) full-list comparison
        if list(actual_headers) != list(expected_headers):
            raise AssertionError(
                f"[ASSERT] Header mismatch.\n"
                f"  Actual:   {actual_headers}\n"
                f"  Expected: {expected_headers}"
            )
        print("[ASSERT] ✅ Header list matches expected list.")
