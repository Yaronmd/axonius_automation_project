from playwright.sync_api import Page,Locator,expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from helpers.logger import logger

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        """Navigate to a given URL."""
        self.page.goto(url)


    def fill_text(self, locator: Locator, text: str,press_enter:bool=False, timeout: float = 10000):
        """Fill text into an input field."""
        try:
            locator.fill(value=text)
            logger.info(f"Filled locator {locator} with text: {text}")
            if press_enter:
                locator.press("Enter")
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while waiting for locator {locator} to become visible.")
            raise
        except Exception as e:
            logger.error(f"Error filling text in locator {locator}: {str(e)}")
            raise

    def click_element(self, locator: Locator):
        """Click an element."""
        try:
            locator.click()
            logger.info(f"Success to click on locator: {locator}")
            return True
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while waiting for locator {locator} to become visible.")
            return False
        except Exception as e:
            logger.error(f"Error filling text in locator {locator}: {str(e)}")
            return False

    def get_element_text(self, locator: Locator) -> str:
        """Get the text content of an element."""
        return locator.text_content()

    def is_element_visible(self, locator: Locator) -> bool:
        """Check if an element is visible."""
        return  locator.is_visible()
