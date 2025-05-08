import os, time, csv
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pages.web_tables_page import WebTablesPage
from models.user_data import UserData

class WebTablesLibrary:
    """Robot keyword library wrapping WebTablesPage POM."""
    def __init__(self):
        self.driver = None
        self.page = None

    def open_web_tables(self, grid_url='http://selenium-hub:4444/wd/hub', browser='chrome'):
        caps = getattr(DesiredCapabilities, browser.upper())
        self.driver = webdriver.Remote(
            command_executor=grid_url,
            desired_capabilities=caps
        )
        self.page = WebTablesPage(self.driver)
        self.page.navigate_to()

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.page = None

    def verify_user_list_table_displayed(self):
        # ensure page is initialized
        assert self.page is not None, "Browser not opened!"
        assert self.page.is_user_list_table_displayed(), "User list table is not displayed"

    def get_header_list(self):
        assert self.page is not None, "Browser not opened!"
        return self.page.get_header_list()

    def click_add_user(self):
        assert self.page is not None, "Browser not opened!"
        self.page.click_add_user()

    def add_user_from_csv(self, file_name, row_index=0):
        # Determine CSV path relative to project root
        csv_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'resources', 'testdata', file_name
        )
        if not os.path.isfile(csv_path):
            raise FileNotFoundError(f"CSV file not found at {csv_path}")
        with open(csv_path, newline='', encoding='utf-8') as f:
            data = list(csv.DictReader(f))[int(row_index)]
        user = UserData(
            first_name=data.get('FirstName',''),
            last_name=data.get('LastName',''),
            username=f"{data.get('userName','')}_{int(time.time())}",
            password=data.get('Password',''),
            company=data.get('customer',''),
            role=data.get('Role',''),
            email=data.get('Email',''),
            mobile_phone=data.get('CellPhone','')
        )
        # ensure page is initialized
        assert self.page is not None, "Browser not opened!"
        self.page.add_user(user)
        return user.username

    def user_should_be_present_in_list(self, username):
        assert self.page is not None, "Browser not opened!"
        assert self.page.is_user_present_in_list(username), f"User {username} not found in list"