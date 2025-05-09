# pages/web_tables_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from models.user_data import UserData
from selenium.webdriver.support.ui import WebDriverWait


class WebTablesPage(BasePage):
    """Page Object Model for the Web Tables page."""

    URL = "http://www.way2automation.com/angularjs-protractor/webtables/"

    locators = {
        "table": (
            By.CSS_SELECTOR,
            'table.smart-table.table-striped[table-title="Smart Table example"]'
        ),
        "modal_backdrop": (
            By.CLASS_NAME,
            "modal-backdrop"
        ),
        "add_user": (
            By.XPATH,
            "//button[contains(.,' Add User')]"
        ),
        "firstName": (
            By.NAME,
            "FirstName"
        ),
        "lastName": (
            By.NAME,
            "LastName"
        ),
        "userName": (
            By.NAME,
            "UserName"
        ),
        "password": (
            By.NAME,
            "Password"
        ),
        "company_aaa": (
            By.XPATH,
            "//label[contains(text(),'Company AAA')]/input"
        ),
        "company_bbb": (
            By.XPATH,
            "//label[contains(text(),'Company BBB')]/input"
        ),
        "role": (
            By.NAME,
            "RoleId"
        ),
        "email": (
            By.NAME,
            "Email"
        ),
        "cellPhone": (
            By.NAME,
            "Mobilephone"
        ),
        "save": (
            By.XPATH,
            "//button[contains(@class,'btn-success') and normalize-space(text())='Save']"
        ),
        "close_button": (
            By.XPATH,
            "//button[contains(@class,'btn-danger') and normalize-space(text())='Close']"
        ),
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def navigate_to(self):
        """Navigate to the Web Tables page."""
        print("[PAGE] Navigating to Web Tables page...")
        try:
            self.driver.get(self.URL)
            self.wait_for_element(self.locators["table"])
            print("[PAGE] Page loaded successfully.")
        except Exception as e:
            print(f"[PAGE] Failed to navigate: {str(e)}")
            raise

    def is_user_list_table_displayed(self) -> bool:
        """Check if the user list table is displayed."""
        print("[PAGE] Checking if user list table is displayed.")
        try:
            element = self.wait_for_element(self.locators["table"])
            return element.is_displayed()
        except Exception as e:
            print(f"[PAGE] Table not displayed: {str(e)}")
            return False

    def get_header_list(self):
        """Retrieve the table headers."""
        print("[PAGE] Retrieving header list.")
        try:
            header_elems = self.driver.find_elements(
                By.CSS_SELECTOR,
                "tr.smart-table-header-row th span.header-content"
            )
            headers = [h.text.strip() for h in header_elems if h.text.strip()]
            print(f"[PAGE] Headers found: {headers}")
            return headers
        except Exception as e:
            print(f"[PAGE] Failed to retrieve headers: {str(e)}")
            return []

    def click_add_user(self):
        """Click the 'Add User' button after waiting for modal to clear."""
        print("[PAGE] Clicking 'Add User' button.")
        try:
            # Wait for any existing modal backdrop to disappear
            try:
                WebDriverWait(self.driver, 3).until_not(
                    EC.presence_of_element_located(self.locators["modal_backdrop"])
                )
                print("[PAGE]  Modal backdrop cleared.")
            except Exception:
                print("[PAGE] No modal backdrop or timeout ignored.")

            button = self.wait.until(EC.element_to_be_clickable(self.locators["add_user"]))
            button.click()

            # Wait for first name field to be visible
            self.wait.until(EC.visibility_of_element_located(self.locators["firstName"]))
            print("[PAGE] Add User modal is visible.")
        except Exception as e:
            print(f"[PAGE] Failed to click Add User: {str(e)}")
            raise

    def add_user(self, user: UserData):
        """Add a user to the table."""
        print(f"[PAGE] Adding user: {user}")
        try:
            self.wait_for_element(self.locators["firstName"]).send_keys(user.first_name)
            self.wait_for_element(self.locators["lastName"]).send_keys(user.last_name)
            self.wait_for_element(self.locators["userName"]).send_keys(user.username)
            self.wait_for_element(self.locators["cellPhone"]).send_keys(user.mobile_phone)

            if user.password:
                self.wait_for_element(self.locators["password"]).send_keys(user.password)
            if user.email:
                self.wait_for_element(self.locators["email"]).send_keys(user.email)

            # Select the company radio button dynamically
            cust_locator = (
                By.XPATH,
                f"//label[contains(normalize-space(),'{user.company}')]/input"
            )
            self.wait.until(EC.element_to_be_clickable(cust_locator)).click()

            # Select role from dropdown
            role_select = Select(self.wait_for_element(self.locators["role"]))
            role_select.select_by_visible_text(user.role)

            # Save user
            self.wait.until(EC.element_to_be_clickable(self.locators["save"])).click()
            print(f"[PAGE] User '{user.username}' saved successfully.")
        except Exception as e:
            print(f"[PAGE] Failed to add user: {str(e)}")
            raise

    def is_user_present_in_list(self, username: str) -> bool:
        """Check if a user is present in the table."""
        print(f"[PAGE] Verifying presence of user '{username}' in table.")
        try:
            rows = self.driver.find_elements(
                By.CSS_SELECTOR,
                "table.smart-table.table-striped tbody tr"
            )
            found = any(username in row.text for row in rows)
            print(f"[PAGE] User found: {found}")
            return found
        except Exception as e:
            print(f"[PAGE] Failed to verify user presence: {str(e)}")
            return False
