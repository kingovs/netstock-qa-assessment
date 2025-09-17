# Base test config via pytest

import pytest
from playwright.sync_api import Page, sync_playwright
from datetime import datetime, timedelta


@pytest.fixture(scope="function")
def custom_page():
    """Custom page fixture that guarantees headed mode"""
    with sync_playwright() as p:
        browser = p.firefox.launch(
            headless=False,
            slow_mo=1000
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        yield page
        browser.close()


def generate_unique_phone():
    """Generate unique phone number for test identification"""
    timestamp = str(int(datetime.now().timestamp()))[-6:]  # Last 6 digits of timestamp
    return f"TEST{timestamp}"


def find_available_room_dates(room_type=1, check_api=False):
    """
    Simple function to find available dates for a room type
    
    Returns:
        tuple: (checkin_date, checkout_date) as strings in YYYY-MM-DD format
    """
    # Default fallback dates (current working approach)
    base_date = datetime.now() + timedelta(days=1)  # Tomorrow
    checkin = base_date.strftime("%Y-%m-%d")
    checkout = (base_date + timedelta(days=1)).strftime("%Y-%m-%d")
    
    if check_api:
        print(f"Checking API for Room {room_type} availability...")
        try:
            import requests
            
            # Simple API check - look for bookings on our proposed dates
            api_url = f"https://restful-booker.herokuapp.com/booking?checkin={checkin}"
            response = requests.get(api_url, timeout=5)
            
            if response.status_code == 200:
                bookings = response.json()
                if bookings:  # If bookings found, try next day
                    print(f"Found {len(bookings)} booking(s) on {checkin}, trying next day...")
                    base_date = base_date + timedelta(days=1)
                    checkin = base_date.strftime("%Y-%m-%d")
                    checkout = (base_date + timedelta(days=1)).strftime("%Y-%m-%d")
                    print(f"Using {checkin} to {checkout} instead")
                else:
                    print(f"No conflicts found for {checkin}")
            else:
                print(f"API check failed (status {response.status_code}), using fallback dates")
                
        except Exception as e:
            print(f"API check failed ({e}), using fallback dates")
    
    print(f"Selected dates for Room {room_type}: {checkin} to {checkout}")
    return checkin, checkout


def navigate_to_booking_page(page: Page, room_type=1, check_api=False):
    """
    Navigate to reservation page with optional room availability checking
    UNCHANGED behavior when called without parameters
    """
    if check_api:
        # Using Room Availability Checker
        checkin, checkout = find_available_room_dates(room_type, check_api=True)
        reservation_url = f"https://automationintesting.online/reservation/{room_type}?checkin={checkin}&checkout={checkout}"
        print(f"Using API-checked dates for Room {room_type}: {reservation_url}")
    else:
        # Fallback Logic
        print("Using fallback date strategy...")
        base_date = datetime.now() + timedelta(days=30)  # 30 days in future
        checkin = base_date.strftime("%Y-%m-%d")
        checkout = (base_date + timedelta(days=1)).strftime("%Y-%m-%d")
        reservation_url = f"https://automationintesting.online/reservation/{room_type}?checkin={checkin}&checkout={checkout}"
    
    print(f"Using dates: {checkin} to {checkout}")
    
    #
    page.goto(reservation_url)
    page.wait_for_timeout(2000)
    
    print("Clicking Reserve Now to reveal booking form...")
    reserve_button = page.locator("button:has-text('Reserve Now')").first
    reserve_button.click()
    page.wait_for_timeout(2000)
    
    print("Booking form should now be visible")


def fill_booking_form(page: Page, firstname="John", lastname="Doe", email="john.doe@example.com", phone=None):
    """Fill booking form using exact selectors discovered from exploration"""
    # Generate unique phone if not provided
    if phone is None:
        phone = generate_unique_phone()
    
    print(f"Filling booking form - Name: {firstname} {lastname}, Email: {email}, Phone: {phone}")
    
    # Use exact selectors from the exploration
    page.locator("input[name='firstname']").fill(firstname)
    page.locator("input[name='lastname']").fill(lastname)
    
    # Only fill email if provided (for missing email test)
    if email:
        page.locator("input[name='email']").fill(email)
    
    page.locator("input[name='phone']").fill(phone)
    
    print("Form filled successfully")
    page.wait_for_timeout(1000)
    
    return phone  


def submit_booking_form(page: Page):
    """Submit the booking form"""
    print("Submitting booking form...")
    
    # Use the exact selector from page analyzer
    submit_button = page.locator("button.btn.btn-primary.w-100.mb-3")
    submit_button.click()
    
    page.wait_for_timeout(2000)
    print("Form submitted")