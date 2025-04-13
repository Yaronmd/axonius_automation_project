
from datetime import datetime
from urllib.parse import urljoin
from helpers.logger import logger
import re
def extract_total_price(price_text: str):
        """Extract the total price from the price text (e.g., '₪4,095 total' -> '₪4,095')."""
        match = re.search(r'[₪$€][\d,]+', price_text)
        if match:
            return match.group(0)
        return "N/A"
    
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
        


def parse_places(title_items,subtitle_items,price_items,price_items_per_night,rating_items):
    
    places = {}
    for i,title in enumerate(title_items):
        subtitle = subtitle_items[i] if i < len(subtitle_items) else "N/A"
        price = price_items[i] if i < len(price_items) else "0"
        price_per_night = price_items_per_night[i] if i < len(price_items_per_night) else "0"
        rating = rating_items[i] if i < len(rating_items) else "0.0"
        
        places[i] = {
        'title': title[0],
        'subtitle': subtitle[0],
        'price': extract_total_price(price[0]),
        'price_per_night':price_per_night[0],
        'rating': extract_rating(rating[0])
        }
        logger.info(f"Place {i + 1}: {title}, Rating: {rating}")
    logger.info(f"Extract Places:{places}")
    return places
        
        
def get_highest_rated_and_chepest(places:dict):
    
    for place in places.values():

        place['real_price'] = place["price"]
        price = place["price"].replace('₪', '').replace('$', '').replace('€','').replace(',', '')
        try:
            place['price'] = int(price)
        except ValueError:
            place['price'] = 0  # In case of invalid price, default to 0
    
    
        try:
            place['rating'] = float(place['rating'])
        except ValueError:
            place['rating'] = 0.0 
       
            
    highest_rated = max(places, key=lambda x: places[x]['rating'])
    logger.info(f"highest rated:{places[highest_rated]}")
    
    cheapest = min(places, key=lambda x: places[x]['price'])
    logger.info(f"cheapest:{places[cheapest]}")
    
    return places[highest_rated],places[cheapest]
            
