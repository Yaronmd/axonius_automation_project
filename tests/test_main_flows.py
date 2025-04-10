
def test_number_1(main_page,navigate_to_airbnb_page):
    
    main_page.set_destination(destination="Tel Aviv-Yafo")
    main_page.click_who_button()
    main_page.guest_panel.validate_labels_and_hints()
    main_page.set_guests(adults=2)
    assert main_page.guest_panel.get_adult_value() == 2
    

    
    