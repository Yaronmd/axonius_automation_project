
from datetime import datetime
from urllib.parse import urljoin
from helpers.logger import logger
import re
def parse_price(price_text: str):
        """Extract the total price from the price text (e.g., '₪4,095 total' -> '₪4,095')."""
        match = re.search(r'[₪$€][\d,]+', price_text)
        if match:
            return match.group(0)
        return "N/A"
    
def convert_price_to_int(price:str): 
    price = price.replace('₪', '').replace('$', '').replace('€','').replace(',', '')
    return int(float(price))
      
    
def extract_prices(text: str):
    """
    Extracts the "per night" price and the "total" price from the given text.
    
    For example, from:
      "₪363 night₪363 per night · ₪2,180 total₪2,180 totalShow price breakdown"
    this function returns:
      per_night: "₪363 per night"
      total: "₪2,180 total"
    """
    # Define a pattern that captures:
    #   Group 1: a currency symbol (₪, $, or €) followed by digits (with commas allowed) and "per night"
    #   Group 2: a currency symbol followed by digits (with commas allowed) and "total"
    pattern = r'([₪$€][\d,]+\s+per\s+night).*?([₪$€][\d,]+\s+total)'
    
    # Search for the pattern in the text using re.DOTALL to make sure it spans multiple parts if needed.
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    
    if match:
        per_night = match.group(1).strip()
        total = match.group(2).strip()
        return per_night, total
    else:
        return None, None
    
def extract_rating(rating_text: str) -> str:
    """Extract the rating value from a string like '4.89 out of 5 average rating, 88 reviews'."""
    match = re.match(r'(\d+\.\d+)', rating_text)
    
    if match:
        # Return the matched rating value
        return match.group(0)
    else:
        return "N/A"  # Return "N/A" if no match is found

def format_dates(start_date: datetime, end_date: datetime) -> str:
    

    """Format start and end dates to 'Month Day – Day' or 'Month Day – Month Day' depending on whether they are in the same month."""
    
    # Format the start date as 'Month Day' (e.g., 'May 23') without leading zeros
    start_date_str = start_date.strftime("%b %d").lstrip("0")  # %b gives abbreviated month name, %d gives day
    start_date_str = start_date_str.replace(" 0", " ")  # Remove leading 0 from day

    # Format the end date as 'Month Day' if the start and end dates are in the same month
    if start_date.month == end_date.month:
        # If the start and end dates are in the same month, format as 'Month Day – Day'
        end_date_str = end_date.strftime("%d").lstrip("0")  # Only the day of the month without leading zero
        end_date_str = end_date_str.replace(" 0", " ")  # Remove leading 0 from day
        formatted_dates = f"{start_date_str} – {end_date_str}"
    else:
        # If the start and end dates are in different months, format as 'Month Day – Month Day'
        end_date_str = end_date.strftime("%b %d").lstrip("0")  # Full month and day without leading zero
        end_date_str = end_date_str.replace(" 0", " ")  # Remove leading 0 from day
        formatted_dates = f"{start_date_str} – {end_date_str}"
    
    # Replace the Word Joiner character (if any)
    formatted_dates = formatted_dates.replace('\u2009', ' ')
    
    return formatted_dates

def format_date_range(start_date: datetime, end_date: datetime) -> str:
    """
    Convert start_date and end_date into a formatted string.
    
    If start_date and end_date are in the same month and year, returns:
       "May 8 – 20, 2025"
    
    Otherwise, it returns a full version with both months:
       "May 8 – June 20, 2025"  (if in the same year)
       
    You can adjust the behavior in the else block as needed.
    """
    if start_date.year == end_date.year and start_date.month == end_date.month:
        # Same month and same year, use:
        return f"{start_date.strftime('%b')} {start_date.day} – {end_date.day}, {start_date.year}"
    else:
        # Different month or different year:
        return f"{start_date.strftime('%b')} {start_date.day} – {end_date.strftime('%b')} {end_date.day}, {end_date.year}"


def parse_number_of_guests(guest_str:str):
    match = re.search(r'[\d,]+', guest_str)
    if match:
        return match.group(0)
    return "N/A"
        
        
        
def get_highest_rated_and_chepest(places:list):
    
    for place in places:
        if place.get("total_price"):
            price = place["total_price"]
            price = price.replace('₪', '').replace('$', '').replace('€','').replace(',', '')
            try:
                place['price_number'] = int(price)
            except ValueError:
               continue # In case of invalid price, default to 0
    
       
            
    highest_rated = max(places, key=lambda x: x.get('rating', 0))
    logger.info(f"Highest rated: {highest_rated}")
    
    cheapest = min(places, key=lambda x: x.get('price_number'))
    logger.info(f"Cheapest: {cheapest}")
    
    return highest_rated,cheapest
            
