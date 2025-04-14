import time
from typing import List, Optional
from urllib.parse import urljoin
from playwright.sync_api import Page,Locator,expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from helpers.logger import logger

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        """Navigate to a given URL."""
        logger.info(f" Navigate to url:{url}")
        self.page.goto(url)


    def fill_text(self, locator: Locator, text: str,press_enter:bool=False):
        """Fill text into an input field."""
        try:
            locator.fill(value=text)
            logger.info(f"Filled locator {locator} with text: {text}")
            if press_enter:
                locator.press("Enter")
            return True
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while waiting for locator {locator} to become visible.")
            raise
        except Exception as e:
            logger.error(f"Error filling text in locator {locator}: {str(e)}")
            raise

    def click_element(self, locator: Locator,timeout=10000):
        """Click an element."""
        try:
            locator.scroll_into_view_if_needed(timeout=timeout)
            locator.wait_for(state="visible",timeout=timeout)
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
            locator.scroll_into_view_if_needed(timeout=timeout)
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
            locator.scroll_into_view_if_needed(timeout=timeout)
            locator.wait_for(state="visible",timeout=timeout)
            return locator.is_visible()
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while waiting locator {locator} to become visible.")
            return None
        except Exception as e:
            logger.error(f"Error getting locator {locator}: {str(e)}")
            return None
        
    def get_all_inner_text_in_element(self,locator: Locator,timeout=10000)->Optional[list]:
        try:
            locator.first.wait_for(state="visible",timeout=timeout)
            return locator.all_inner_texts()
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while waiting for locator '{locator}' to become visible.")
            return None
        except Exception as e:
            logger.error(f"Error getting locator {locator}: {str(e)}")
            return None
    
    def get_all_text_contents_in_element(self,locator: Locator,timeout=10000)->Optional[list]:
        try:
            locator.first.scroll_into_view_if_needed(timeout=timeout)
            locator.first.wait_for(state="visible",timeout=timeout)
            return locator.all_text_contents()
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while waiting for locator '{locator}' to become visible.")
            return None
        except Exception as e:
            logger.error(f"Error getting locator {locator}: {str(e)}")
            return None    

    def wait_for_all_elements(self,locator, timeout=5000):
        """
        Wait until all elements matched by the locator are visible.
        """
        start_time = time.time()
        while (time.time() - start_time) * 1000 < timeout:
            count = locator.count()
            if count > 0:
                # Check if each element is visible.
                all_visible = True
                for i in range(count):
                    try:
                        if not locator.nth(i).is_visible(timeout=500):  
                            all_visible = False
                            break
                    except TimeoutError:
                        all_visible = False
                        break
                if all_visible:
                    return locator.all()
            time.sleep(0.2)
        raise TimeoutError(f"Not all elements became visible within {timeout} ms.")



    def get_full_url_from_href(self,relative_url):
        """
        This function combines the base URL of the current page with the relative URL
        to form a complete URL.
        """
        current_url = self.page.url  # Get the current page's URL
        logger.info(current_url)
        full_url = urljoin(current_url, relative_url)  # Combine with the relative URL
        return full_url   
    
    def dismiss_popup(self, trigger_text: str):
        """
        Click the trigger to open the popup and then click the dismiss button inside the popup.
        
        Args:
            trigger_text (str): The text on the element that triggers the popup.        
   
        """
        logger.info("dismiss_popup")
        # Start waiting for popup before clicking.
        with self.page.expect_popup() as popup_info:
            logger.info(f"popup info:{popup_info.value}")
            self.page.get_by_text(trigger_text).click()  # Click the trigger that opens the popup
        popup = popup_info.value
        logger.info(f"popup:{popup}")
        popup.wait_for_load_state("domcontentloaded")
        
        popup.close()
        
     