
from helpers.parse_helper import format_dates, get_highest_rated_and_chepest
from helpers.write_to_file_helper import log_results_to_temp_folder
import pytest


@pytest.mark.parametrize("destination, expected_adults", [
    ("Tel Aviv-Yafo", 2),
])
def test_number_1(main_page,navigate_to_airbnb_page,destination, expected_adults):
    
    # Set destination and choose a random checkin/out date within current months
    main_page.set_destination(destination=destination)
    start_date,end_date = main_page.set_random_checkin_and_checkout_between_current_months()
    assert start_date is not None and end_date is not None, "start_date or end_date is None"
    
    # select who comming and validate
    main_page.click_who_button()
    main_page.guest_panel.validate_labels_and_hints()
    main_page.set_guests(adults=expected_adults)
    assert int(main_page.guest_panel.get_adult_value()) == expected_adults
    
    # apply search
    main_page.click_search_button()
    
    # apply filters by aprtment
    main_page.click_filter_button()
    main_page.filter_panel.filter_by_aprtment()
   
    # Validate location selected, check-in/out dates, number of guests
    main_page.validate_selected_location(destination)
    assert main_page.get_selected_checkin_out() == format_dates(start_date=start_date,end_date=end_date)
    assert main_page.get_number_of_selected_guests() == main_page.guest_panel.get_count_total_gust_str()
    
    # Get list of all places
    list_of_places = main_page.get_list_of_places()
    assert list_of_places is not None
    # Get highest rated and chepeast
    highest_rated,chepeast=get_highest_rated_and_chepest(places=list_of_places)
    
    log_results_to_temp_folder(file_name="test_number_1",cheapest_result=chepeast,highest_rated=highest_rated)

@pytest.mark.parametrize("destination, expected_adults, expected_childs, country_name, phone_number", [
    ("Tel Aviv-Yafo", 2, 1, "Israel", "0545651550"),
])
def test_number_2(reserve_page,place_page,main_page,navigate_to_airbnb_page,destination,expected_adults,expected_childs,country_name,phone_number):
    
    # Set destination and choose a random checkin/out date within current months
    main_page.set_destination(destination=destination)
    start_date,end_date = main_page.set_random_checkin_and_checkout_between_current_months()
    assert start_date is not None and end_date is not None, "start_date or end_date is None"
    
    # select who comming and validate
    main_page.click_who_button()
    main_page.guest_panel.validate_labels_and_hints()
    main_page.set_guests(adults=expected_adults,children=expected_childs)
    assert int(main_page.guest_panel.get_adult_value()) == expected_adults
    assert int(main_page.guest_panel.get_children_value()) == expected_childs
    
    # apply search
    main_page.click_search_button()
    
    # apply filters by aprtment
    main_page.click_filter_button()
    main_page.filter_panel.filter_by_aprtment()
    main_page.validate_selected_location(destination)
    
    # Validate location selected, check-in/out dates, number of guests
    assert main_page.get_selected_checkin_out() == format_dates(start_date=start_date,end_date=end_date)
    assert main_page.get_number_of_selected_guests() == main_page.guest_panel.get_count_total_gust_str()
    
    # Get list of all places
    list_of_places = main_page.get_list_of_places()
    assert list_of_places is not None
    highest_rated,chepeast=get_highest_rated_and_chepest(places=list_of_places)
    
    # select place validate and save resrevtion to log
    main_page.select_place(place=highest_rated)
    place_page.validate_selcted_place(place=highest_rated,start_date=start_date,end_date=end_date,number_of_guests=3)
    place_page.save_resrevtion_to_log()
    
    # reserve and validate 
    place_page.click_reserve()
    reserve_page.validate_reseverion_detail(highest_rated,start_date,end_date,number_of_guests=[expected_childs,expected_adults])
    
    # select country and set phone number
    reserve_page.select_country_code(country_name)
    reserve_page.set_phone_number(phone_number)
    log_results_to_temp_folder(file_name="test_number_2",cheapest_result=chepeast,highest_rated=highest_rated)
    