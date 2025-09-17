# TEST 2: COMPLETE BOOKING

from playwright.sync_api import Page
from conftest import navigate_to_booking_page, fill_booking_form, submit_booking_form


def test_booking_with_complete_information_success(custom_page: Page):
    """Test complete booking shows confirmation"""
    
    print("\n" + "="*60)
    print("TEST 2: Creating booking with complete information") 
    print("="*60)
    
    # Navigate, fill, and submit
    navigate_to_booking_page(custom_page, room_type=1, check_api=False)
    fill_booking_form(custom_page, firstname="Jane", lastname="Smith", 
                     email="jane@example.com", phone="98765432109")
    submit_booking_form(custom_page)
    
    # Check for confirmation
    custom_page.wait_for_timeout(3000)
    page_content = custom_page.content().lower()
    
    booking_confirmed = "booking confirmed" in page_content
    
    print(f"Booking confirmation found: {booking_confirmed}")
    
    assert booking_confirmed, "Expected 'Booking Confirmed' message but none found"
    print("✓ TEST PASSED: Booking confirmed successfully")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])