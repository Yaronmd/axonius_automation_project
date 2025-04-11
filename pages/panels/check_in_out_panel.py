
import calendar
import random
from pages.base_page import BasePage
from datetime import datetime,timedelta
from typing import Optional
from helpers.logger import logger
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


def get_current_and_next_month_from_today() -> tuple:
    """Get today's date and the end of the next month."""
    today = datetime.today()
    
    if today.month == 12:
        start_of_next_month = datetime(today.year + 1, 1, 1)
    else:
        start_of_next_month = datetime(today.year, today.month + 1, 1)
    
    # Calculate the last day of the next month
    end_of_next_month = start_of_next_month + timedelta(days=31)
    end_of_next_month = end_of_next_month.replace(day=1) - timedelta(days=1)
    
    return today, end_of_next_month

def get_random_start_date_for_two_months() -> datetime:
    """Generate a random start date within the next two months, starting from today."""
    today, end_of_next_month = get_current_and_next_month_from_today()
    
   
    random_days = random.randint(0, (end_of_next_month - today).days)
    
    # Return the random start date within the range
    random_start_date = today + timedelta(days=random_days)
    
    return random_start_date

def get_random_end_date_for_two_months(start_date: datetime) -> datetime:
    """Generate a random end date, which is at least one day after the start date, within the next two months."""
    today, end_of_next_month = get_current_and_next_month_from_today()
    
    end_date = start_date + timedelta(days=random.randint(1, 30))  # End date is at least 1 day after start
    
    # Check if the end date falls within the current two months range, else regenerate
    while end_date < today or end_date > end_of_next_month:
        # Regenerate if the date is outside the current range
        end_date = start_date + timedelta(days=random.randint(1, 30))
    
    return end_date


class CheckInOutPanel(BasePage):
    
    next_month_button_path = "button[aria-label='Move forward to switch to the next month.']"
    
    current_month_title_path = "xpath=(//*[@data-testid='structured-search-input-field-dates-panel']//h2)[1]"
    next_month_title_path = "xpath=(//*[@data-testid='structured-search-input-field-dates-panel']//h2)[2]"
    
    
    def __init__(self, page):
        super().__init__(page)
        self.page = page
    
    def get_current_displayed_month(self) -> str:
        """Get the current displayed month (e.g., 'April 2025')."""
        month_locator = self.page.locator(self.current_month_title_path)
        current_month = month_locator.text_content().strip()
        return current_month
    
    def get_next_displayed_month(self) -> str:
        """Get the next displayed month (e.g., 'May 2025')."""
        month_locator = self.page.locator(self.next_month_title_path)
        next_month = month_locator.text_content().strip()
        return next_month
    
    def click_next_month_button(self):
        """Click the 'Next' button to move to the next month on the calendar."""
        next_button = self.page.locator(self.next_month_button_path)
        if not self.click_element(next_button):
            return False
            
    
    
    def select_date_checkin_or_checkout(self, date: str):
        path_to_date = f"xpath=//button[@data-state--date-string='{date}']"
        return self.click_element(self.page.locator(path_to_date))

    def select_random_checkin_and_checkout(self):
        """Select random check-in and check-out dates on the calendar."""
       
        start_date = get_random_start_date_for_two_months()
        end_date = get_random_end_date_for_two_months(start_date)
        
        logger.info(f"Start Date: {start_date.strftime("%Y-%m-%d")}")
        logger.info(f"End Date: {end_date.strftime("%Y-%m-%d")}")


        # Select start and end dates
        if self.select_date_checkin_or_checkout(date=start_date.strftime("%Y-%m-%d")) and \
            self.select_date_checkin_or_checkout(date=end_date.strftime("%Y-%m-%d")):
            logger.info(f"Success select start date:'{start_date}' and end date:'{end_date}'")
            return start_date, end_date
        
        return None

            
        
   
    