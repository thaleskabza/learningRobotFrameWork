from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Base class for page objects."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10, poll_frequency=0.5)

    def wait_for_element(self, locator):
        """Wait for an element to be present."""
        return self.wait.until(EC.presence_of_element_located(locator))