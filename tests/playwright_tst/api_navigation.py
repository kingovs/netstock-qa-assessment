"""
API-based navigation functions for tests that need conflict-free dates
"""
from playwright.sync_api import Page
from api_helpers import find_available_dates_efficient


def navigate_to_booking_page_with_api_check(page: Page):
    """Navigate to reservation page using efficient API conflict checking"""
    print("Finding conflict-free dates via API...")
    checkin, checkout = find_available_dates_efficient()
    print(f"Using conflict-free dates: {checkin} to {checkout}")
    
    # Go to room 1 reservation page with available dates
    reservation_url = f"https://automationintesting.online/reservation/1?checkin={checkin}&checkout={checkout}"
    page.goto(reservation_url)
    page.wait_for_timeout(2000)
    
    # Click "Reserve Now" to reveal the booking form
    print("Clicking Reserve Now to reveal booking form...")
    reserve_button = page.locator("button:has-text('Reserve Now')").first
    reserve_button.click()
    page.wait_for_timeout(2000)
    
    print("Booking form should now be visible")