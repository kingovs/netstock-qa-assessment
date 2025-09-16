"""
Simplified test for missing email validation using exact selectors
"""
from playwright.sync_api import Page
from conftest import navigate_to_booking_page, fill_booking_form, submit_booking_form, check_for_error_messages


def test_booking_missing_email_shows_error(custom_page: Page):
    """Test that creating a booking without email shows proper error message"""
    
    print("\n" + "="*60)
    print("TEST 1: Creating booking with missing email")
    print("="*60)
    
    # Step 1: Navigate to booking form
    navigate_to_booking_page(custom_page)
    
    # Step 2: Fill form WITHOUT email
    print("Filling form without email...")
    fill_booking_form(
        custom_page,
        firstname="Test",
        lastname="User", 
        email="",  # Empty email to test validation
        phone="12345678909"
    )
    
    # Pause to see the filled form
    custom_page.wait_for_timeout(3000)
    
    # Step 3: Submit the form
    submit_booking_form(custom_page)
    
    # Step 4: Check for error messages
    print("Checking for error messages...")
    custom_page.wait_for_timeout(2000)
    
    error_messages = check_for_error_messages(custom_page)
    
    print(f"Found {len(error_messages)} error message(s):")
    for i, message in enumerate(error_messages, 1):
        print(f"  Error {i}: {message}")
    
    # Final pause to see the result
    custom_page.wait_for_timeout(3000)
    
    # Test assertion
    assert len(error_messages) > 0, "Expected error message for missing email, but none found"
    
    # Check if error is email-related
    email_related_error = any("email" in msg.lower() for msg in error_messages)
    if email_related_error:
        print("✓ Email-related error message found")
    else:
        print("! Generic error message found")
    
    print("✓ TEST PASSED: Error message appeared for missing email")
    print("="*60)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])