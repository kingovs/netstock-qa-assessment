# TEST 1: Missing Email

from playwright.sync_api import Page
from conftest import navigate_to_booking_page, fill_booking_form, submit_booking_form


def test_booking_missing_email_shows_error(custom_page: Page):
    """Test that creating a booking without email shows proper error message"""
    
    print("\n" + "="*60)
    print("TEST 1: Creating booking with missing email")
    print("="*60)
    
    # Navigate and fill form
    navigate_to_booking_page(custom_page)
    fill_booking_form(custom_page, firstname="Test", lastname="User", email="", phone="12345678909")
    submit_booking_form(custom_page)
    
    # Simple check for the validation message you can see
    custom_page.wait_for_timeout(3000)
    page_content = custom_page.content().lower()
    
    # Check for the exact message from your screenshot
    has_validation = "must not be empty" in page_content
    
    print(f"Validation message found: {has_validation}")
    
    assert has_validation, "Expected 'must not be empty' validation message"
    print("✓ TEST PASSED: Email validation works")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])