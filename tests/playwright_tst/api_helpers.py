"""
API helper functions for RestfulBooker API
"""
import requests
from datetime import datetime, timedelta
import random


def get_auth_token():
    """Get authentication token for API operations"""
    auth_url = "https://restful-booker.herokuapp.com/auth"
    auth_data = {
        "username": "admin", 
        "password": "password123"
    }
    response = requests.post(auth_url, json=auth_data)
    if response.status_code == 200:
        return response.json().get("token")
    return None


def find_available_dates_efficient():
    """Find available dates using API query parameters for efficient conflict checking"""
    from datetime import datetime, timedelta
    
    # Start checking from tomorrow
    base_date = datetime.now() + timedelta(days=1)
    
    for days_ahead in range(60):  # Check up to 60 days ahead
        checkin_date = (base_date + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        checkout_date = (base_date + timedelta(days=days_ahead + 1)).strftime("%Y-%m-%d")
        
        # Use API query parameters to check for conflicts on these specific dates
        if not has_booking_conflict(checkin_date, checkout_date):
            print(f"Found available dates: {checkin_date} to {checkout_date}")
            return checkin_date, checkout_date
    
    # Fallback to far future dates if all near dates are booked
    fallback_base = datetime.now() + timedelta(days=90)
    checkin = fallback_base.strftime("%Y-%m-%d")
    checkout = (fallback_base + timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"Using fallback dates: {checkin} to {checkout}")
    return checkin, checkout


def has_booking_conflict(checkin_date, checkout_date):
    """Check if there are any bookings that conflict with the given dates"""
    try:
        # Check for bookings with checkin on our dates
        checkin_url = f"https://restful-booker.herokuapp.com/booking?checkin={checkin_date}"
        checkin_response = requests.get(checkin_url, timeout=5)
        
        # Check for bookings with checkout on our dates  
        checkout_url = f"https://restful-booker.herokuapp.com/booking?checkout={checkout_date}"
        checkout_response = requests.get(checkout_url, timeout=5)
        
        # If either query returns bookings, there might be a conflict
        checkin_bookings = checkin_response.json() if checkin_response.status_code == 200 else []
        checkout_bookings = checkout_response.json() if checkout_response.status_code == 200 else []
        
        # If we find any bookings, there's a potential conflict
        if checkin_bookings or checkout_bookings:
            print(f"Conflict found for {checkin_date}-{checkout_date}: {len(checkin_bookings + checkout_bookings)} booking(s)")
            return True
        
        return False
        
    except Exception as e:
        print(f"Error checking dates {checkin_date}-{checkout_date}: {e}")
        # If API fails, assume no conflict and continue
        return False


def get_future_dates():
    """Get future dates as fallback"""
    base_date = datetime.now() + timedelta(days=30)
    checkin = base_date.strftime("%Y-%m-%d")
    checkout = (base_date + timedelta(days=1)).strftime("%Y-%m-%d")
    return checkin, checkout


def generate_unique_phone():
    """Generate unique phone number for test identification"""
    timestamp = str(int(datetime.now().timestamp()))[-6:]  # Last 6 digits of timestamp
    return f"TEST{timestamp}"


def find_test_bookings(phone_pattern="TEST"):
    """Find bookings created by tests (containing phone pattern)"""
    response = requests.get("https://restful-booker.herokuapp.com/booking")
    if response.status_code != 200:
        return []
    
    test_bookings = []
    booking_ids = response.json()
    
    for booking_info in booking_ids:
        booking_id = booking_info["bookingid"]
        booking_response = requests.get(f"https://restful-booker.herokuapp.com/booking/{booking_id}")
        
        if booking_response.status_code == 200:
            booking_data = booking_response.json()
            # Check if this looks like a test booking
            if (phone_pattern in str(booking_data.get("additionalneeds", "")) or
                phone_pattern in str(booking_data.get("lastname", "")) or
                "test" in str(booking_data.get("firstname", "")).lower()):
                test_bookings.append(booking_id)
    
    return test_bookings


def delete_booking(booking_id):
    """Delete a specific booking"""
    token = get_auth_token()
    if not token:
        return False
    
    delete_url = f"https://restful-booker.herokuapp.com/booking/{booking_id}"
    headers = {"Cookie": f"token={token}"}
    
    response = requests.delete(delete_url, headers=headers)
    return response.status_code in [200, 201]


def cleanup_test_bookings():
    """Clean up any existing test bookings"""
    test_bookings = find_test_bookings()
    deleted_count = 0
    
    for booking_id in test_bookings:
        if delete_booking(booking_id):
            deleted_count += 1
    
    return deleted_count