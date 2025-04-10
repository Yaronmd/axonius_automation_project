
import calendar
import random
from pages.base_page import BasePage
from datetime import datetime,timedelta
from typing import Optional



def get_check_in_today(today: bool) -> str:
    """Return today's date formatted as 'YYYY-MM-DD' if today=True."""
    if today:
        return datetime.today().strftime("%Y-%m-%d")
    return ""

def get_random_check_out_up_to_month() -> str:
    """Generate a random check-out date up to the end of this month or the next month."""
    current_date = datetime.today()

    # Get current month range
    start_current_month, end_current_month = get_month_range(current_date.year, current_date.month)

    # Get next month range
    next_month = current_date.month + 1 if current_date.month < 12 else 1
    next_month_year = current_date.year if current_date.month < 12 else current_date.year + 1
    start_next_month, end_next_month = get_month_range(next_month_year, next_month)

    # Combine the ranges: from now until the end of next month
    random_check_out_date = generate_random_date(start_current_month, end_next_month)

    # Return the check-out date formatted as 'YYYY-MM-DD'
    return random_check_out_date.strftime("%Y-%m-%d")

def get_month_range(year, month):
    """Get the start and end date of the given month."""
    start_date = datetime(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = datetime(year, month, last_day)
    return start_date, end_date

def generate_random_date(start_date, end_date):
    """Generate a random date between start_date and end_date."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)  # Choose a random number of days
    return start_date + timedelta(days=random_days)
class CheckInOutPanel(BasePage):
    
    
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        
    def select_check_in_today(self):
        path = f"//button[@data-state--date-string='{get_check_in_today(today=True)}']"
        
    def select_random_checkout_up_to_month(self):
        path = f"//button[@data-state--date-string='{get_random_check_out_up_to_month()}']"
        
        
    