"""
Simplified configuration for Playwright tests - Fast version
"""
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


def navigate_to_booking_page(page: Page):
    """Navigate directly to reservation page with future dates (fast version)"""
    print("Using future dates for booking...")
    
    # Use simple future dates instead of API checking for speed
    from datetime import datetime, timedelta
    base_date = datetime.now() + timedelta(days=30)  # 30 days in future
    checkin = base_date.strftime("%Y-%m-%d")
    checkout = (base_date + timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"Using dates: {checkin} to {checkout}")
    
    # Go to room 1 reservation page with future dates
    reservation_url = f"https://automationintesting.online/reservation/1?checkin={checkin}&checkout={checkout}"
    page.goto(reservation_url)
    page.wait_for_timeout(2000)
    
    # Click "Reserve Now" to reveal the booking form
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
    
    return phone  # Return the phone number for tracking


def submit_booking_form(page: Page):
    """Submit the booking form"""
    print("Submitting booking form...")
    
    # Use the exact selector from page analyzer
    submit_button = page.locator("button.btn.btn-primary.w-100.mb-3")
    submit_button.click()
    
    page.wait_for_timeout(2000)
    print("Form submitted")


def check_for_error_messages(page: Page):
    """Look for error messages on the page"""
    error_messages = []
    
    # Look for common error message patterns
    error_selectors = [
        ".alert-danger",
        ".error", 
        ".invalid-feedback",
        "[class*='error']",
        ".text-danger",
        ".alert",
        ".notification"
    ]
    
    for selector in error_selectors:
        try:
            elements = page.locator(selector).all()
            for element in elements:
                if element.is_visible():
                    text = element.text_content()
                    if text and text.strip():
                        error_messages.append(text.strip())
        except:
            continue
    
    # Check for HTML5 validation on required fields
    try:
        # Check if email field shows validation error
        email_field = page.locator("input[name='email']")
        if email_field.is_visible():
            # Check if field is marked as invalid
            validation_message = email_field.evaluate("el => el.validationMessage")
            if validation_message:
                error_messages.append(f"Email validation: {validation_message}")
    except:
        pass
    
    # Check for browser console errors (JavaScript errors)
    try:
        # Check if there are any console error messages visible
        page.wait_for_timeout(1000)  # Wait a moment for any async errors
        
        # Look for the application error shown in the browser
        app_error = page.locator("text=Application error").first
        if app_error.is_visible():
            error_messages.append("Application error: client-side exception occurred")
            
        # Also check for any network/API errors in the page content
        if "exception has occurred" in page.content().lower():
            error_messages.append("JavaScript exception occurred during form submission")
            
    except:
        pass
    
    return error_messages


def check_for_success_messages(page: Page):
    """Look for success confirmation messages"""
    success_messages = []
    
    # Wait for any async operations to complete
    page.wait_for_timeout(3000)
    
    success_selectors = [
        ".alert-success",
        ".success",
        ".confirmation",
        "[class*='success']",
        ".text-success"
    ]
    
    for selector in success_selectors:
        try:
            elements = page.locator(selector).all()
            for element in elements:
                if element.is_visible():
                    text = element.text_content()
                    if text and text.strip():
                        success_messages.append(text.strip())
        except:
            continue
    
    # Check for booking confirmation indicators
    try:
        # Look for booking reference numbers or confirmation text
        page_content = page.content().lower()
        if any(phrase in page_content for phrase in ["booking confirmed", "reservation confirmed", "thank you"]):
            success_messages.append("Booking confirmation detected in page content")
    except:
        pass
    
    return success_messages