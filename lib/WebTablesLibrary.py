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
        """Open browser and navigate to web tables page"""
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
            print(f"[ERROR] ❌ Failed to open browser or navigate: {e}")
            raise RuntimeError(f"[ERROR] Failed to open browser or navigate to page: {str(e)}")

    def close_browser(self):
        """Close the browser session"""
        if self.driver:
            print("[CLOSE] Closing browser session.")
            self.driver.quit()
        else:
            print("[CLOSE] No active browser session to close.")
        self.driver = None
        self.page = None

    def verify_user_list_table_displayed(self):
        """Verify the user list table is displayed"""
        self._ensure_page_initialized()
        if not self.page.is_user_list_table_displayed():
            raise AssertionError("❌ User list table is not displayed.")
        print("[CHECK] ✅ User list table is visible.")

    def get_header_list(self):
        """Get the list of headers from the table"""
        self._ensure_page_initialized()
        headers = self.page.get_header_list()
        print(f"[DATA] Retrieved headers: {headers}")
        return headers

    def click_add_user(self):
        """Click the Add User button"""
        self._ensure_page_initialized()
        print("[ACTION] Clicking 'Add User' button.")
        self.page.click_add_user()

    def add_user_from_csv(self, file_name, row_index=0):
        """Add a user from CSV data"""
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
        """Verify user is present in the list"""
        self._ensure_page_initialized()
        if not self.page.is_user_present_in_list(username):
            raise AssertionError(f"[ASSERT] ❌ User '{username}' not found in the user list.")
        print(f"[ASSERT] ✅ User '{username}' is present in the user list.")

    def is_browser_open(self):
        """Check if browser is open"""
        status = self.driver is not None and self.page is not None
        print(f"[STATUS] Is browser open? {status}")
        return status