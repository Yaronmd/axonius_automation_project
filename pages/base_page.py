from typing import Optional
from playwright.sync_api import Page,Locator,expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from helpers.logger import logger

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        """Navigate to a given URL."""
        self.page.goto(url)


    def fill_text(self, locator: Locator, text: str,press_enter:bool=False):
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

    def get_element_text(self, locator: Locator,timeout=10000) -> str:
        """Get the text content of an element."""
        try:
            locator.first.wait_for(state="visible",timeout=timeout)
            text =locator.text_content()
            logger.info(f"Success to get text:{text}")
            return text
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while waiting for text in locator {locator} to become visible.")
            return None
        except Exception as e:
            logger.error(f"Error getting locator {locator}: {str(e)}")
            return None

    def is_element_visible(self, locator: Locator,timeout=10000) -> bool:
        """Check if an element is visible."""
        try:
            locator.wait_for(state="visible",timeout=timeout)
            return locator.is_visible()
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while waiting locator {locator} to become visible.")
            return None
        except Exception as e:
            logger.error(f"Error getting locator {locator}: {str(e)}")
            return None

    def get_list_of_all_inner_texts_in_elements(self,locator: Locator,timeout=10000)->Optional[list]:
        try:
            locator.first.wait_for(state="visible",timeout=timeout)
            all_inner_texts = []
            all_items = locator.all()
            for item in all_items:
                all_inner_texts.append(item.all_inner_texts())
            return all_inner_texts
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while waiting for locator {locator} to become visible.")
            return None
        except Exception as e:
            logger.error(f"Error getting locator {locator}: {str(e)}")
            return None
         