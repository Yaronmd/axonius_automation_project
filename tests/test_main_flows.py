
from helpers.parse_helper import format_dates, get_highest_rated_and_chepest
from helpers.write_to_file_helper import log_results_to_temp_folder

def test_number_1(main_page,navigate_to_airbnb_page):
    
    main_page.set_destination(destination="Tel Aviv-Yafo")
    start_date,end_date = main_page.set_random_checkin_and_checkout_between_current_months()
    assert start_date is not None and end_date is not None, "start_date or end_date is None"
    assert main_page.click_who_button()
    assert main_page.guest_panel.validate_labels_and_hints()
    assert main_page.set_guests(adults=2)
    assert int(main_page.guest_panel.get_adult_value()) == 2
    assert main_page.click_search_button()
    assert main_page.validate_selected_location("Tel Aviv-Yafo")
    assert main_page.get_selected_checkin_out() == format_dates(start_date=start_date,end_date=end_date)
    assert main_page.get_number_of_selected_guests() == "2 guests"
    list_of_places = main_page.get_list_of_places()
    assert list_of_places is not None
    highest_rated,chepeast=get_highest_rated_and_chepest(places=list_of_places)
    
    log_results_to_temp_folder(file_name="test_number_1",cheapest_result=chepeast,highest_rated=highest_rated)

def test_number_2(main_page,navigate_to_airbnb_page):
    
    main_page.set_destination(destination="Tel Aviv-Yafo")
    start_date,end_date = main_page.set_random_checkin_and_checkout_between_current_months()
    assert start_date is not None and end_date is not None, "start_date or end_date is None"
    assert main_page.click_who_button()
    assert main_page.guest_panel.validate_labels_and_hints()
    assert main_page.set_guests(adults=2,children=1)
    assert int(main_page.guest_panel.get_adult_value()) == 3
    assert main_page.click_search_button()
    assert main_page.validate_selected_location("Tel Aviv-Yafo")
    assert main_page.get_selected_checkin_out() == format_dates(start_date=start_date,end_date=end_date)
    assert main_page.get_number_of_selected_guests() == "2 guests"
    list_of_places = main_page.get_list_of_places()
    assert list_of_places is not None
    highest_rated,chepeast=get_highest_rated_and_chepest(places=list_of_places)
    
    log_results_to_temp_folder(file_name="test_number_1",cheapest_result=chepeast,highest_rated=highest_rated)
    