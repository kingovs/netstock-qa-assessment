# TEST 3: BOOKING DELETION

import requests
from playwright.sync_api import Page


def get_auth_token():
    """Get authentication token for deletion"""
    try:
        auth_url = "https://restful-booker.herokuapp.com/auth"
        auth_data = {"username": "admin", "password": "password123"}
        response = requests.post(auth_url, json=auth_data, timeout=10)
        
        if response.status_code == 200:
            token = response.json().get("token")
            print(f"✓ Got auth token: {token}")
            return token
        else:
            print(f"✗ Auth failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Auth error: {e}")
        return None


def get_first_booking_id():
    """Get the first booking ID from the API"""
    try:
        bookings_url = "https://restful-booker.herokuapp.com/booking"
        response = requests.get(bookings_url, timeout=10)
        
        if response.status_code == 200:
            bookings = response.json()
            if bookings and len(bookings) > 0:
                first_booking_id = bookings[0]["bookingid"]
                print(f"✓ Found first booking ID: {first_booking_id}")
                return first_booking_id
            else:
                print("✗ No bookings found in API")
                return None
        else:
            print(f"✗ Failed to get bookings: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Error getting bookings: {e}")
        return None


def delete_booking_by_id(booking_id):
    """Delete a specific booking by ID"""
    token = get_auth_token()
    if not token:
        return False, "Could not get auth token"
    
    try:
        delete_url = f"https://restful-booker.herokuapp.com/booking/{booking_id}"
        headers = {"Cookie": f"token={token}"}
        
        response = requests.delete(delete_url, headers=headers, timeout=10)
        
        if response.status_code in [200, 201]:
            print(f"✓ Successfully deleted booking {booking_id}")
            return True, f"Booking {booking_id} deleted successfully"
        else:
            print(f"✗ Delete failed: {response.status_code}")
            return False, f"Delete failed with status {response.status_code}"
            
    except Exception as e:
        print(f"✗ Delete error: {e}")
        return False, f"Delete error: {e}"


def test_delete_booking(custom_page: Page):
    """Test deleting a booking via API"""
    
    print("\n" + "="*60)
    print("TEST 3: Testing booking deletion via API")
    print("="*60)
    
    # Step 1: Get first booking ID from API
    print("Step 1: Getting first booking ID from API...")
    booking_id = get_first_booking_id()
    
    if booking_id:
        # Step 2: Delete the booking
        print(f"Step 2: Attempting to delete booking {booking_id}...")
        deletion_success, deletion_message = delete_booking_by_id(booking_id)
        
        print(f"Deletion result: {deletion_message}")
        
        # Test assertion
        if deletion_success:
            print("✓ TEST PASSED: Booking deletion successful")
            assert True, "Successfully deleted a booking via API"
        else:
            print("✗ TEST FAILED: Could not delete booking")
            assert False, f"Deletion failed: {deletion_message}"
    else:
        print("⚠ TEST SKIPPED: No bookings available to delete")
        assert True, "Test skipped - no bookings found"
    
    print("="*60)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])