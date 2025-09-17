# Playwright UI Automation Test Suite

Comprehensive UI automation test suite for the RestfulBooker application using Playwright and Python. Tests booking functionality including form validation, successful bookings, and API-based deletion.

## 📁 Project Structure

```
app/
├── requirements.txt
├── tests/playwright_tst/
│   ├── conftest.py                    # Test configuration and shared utilities
│   ├── __page_analyzer.py            # Interactive page exploration tool
│   ├── i_test_missing_email.py       # Test 1: Missing email validation
│   ├── ii_test_complete_booking.py   # Test 2: Complete booking flow
│   ├── iii_test_booking_deletion.py  # Test 3: API booking deletion
│   ├── iv_run_all_tests.py          # Test suite runner
│   ├── setup.py                     # One-click setup script

│   ├── __pycache__/                  # Python cache (auto-generated)
│   └── .pytest_cache/               # Pytest cache (auto-generated)
```

## 🛠️ Environment Setup

### Option 1: One-Click Setup (Recommended)

```bash
# Download and run the setup script
cd app
python setup.py
```

This will automatically:
- Check Python version compatibility
- Create virtual environment
- Install all dependencies
- Install Playwright Firefox browser
- Verify installation
- Offer to run tests immediately

### Option 2: Manual Setup

#### Prerequisites
- **Python 3.8+**
- **Git** (for version control)
- **Internet connection** (for API calls and web testing)

### 1. Create Virtual Environment

```bash
# Navigate to project root
cd app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers (Firefox used by default)
playwright install firefox
```

### 3. Verify Installation

```bash
# Check Playwright installation
playwright --version

# Run a quick test
cd tests/playwright_tst
python -c "from playwright.sync_api import sync_playwright; print('✓ Playwright ready')"
```

## 📋 Dependencies

The test suite requires the following packages (defined in `requirements.txt`):

```
playwright==1.55.0      # Browser automation framework
pytest-playwright==0.7.1 # Playwright integration for pytest  
pytest==8.4.2           # Test framework
pytest-html==4.1.1      # HTML test reports
requests==2.31.0         # HTTP requests for API testing
```

## 🧪 Test Scripts

### Test 1: `i_test_missing_email.py`
**Purpose**: Validates that the booking form properly handles missing email addresses.

**What it does**:
- Navigates to the booking form
- Fills all fields except email
- Submits the form
- Verifies that a validation message appears

**Expected result**: Test passes if "must not be empty" validation message is displayed.

### Test 2: `ii_test_complete_booking.py`  
**Purpose**: Tests the complete booking flow with all required information.

**What it does**:
- Navigates to the booking form with available dates
- Fills all required fields (firstname, lastname, email, phone)
- Submits the booking
- Checks for "Booking Confirmed" message

**Expected result**: Test passes if booking confirmation is displayed.

### Test 3: `iii_test_booking_deletion.py`
**Purpose**: Tests API-based booking deletion functionality.

**What it does**:
- Retrieves the first available booking ID via API
- Authenticates with the RestfulBooker API
- Deletes the booking using API credentials
- Verifies deletion was successful

**Expected result**: Test passes if a booking is successfully deleted via API.

## 🚀 Running the Tests

```bash
# Navigate to test directory
cd tests/playwright_tst

# Run all tests with one command
python iv_run_all_tests.py
```

This single command will:
- Run all three tests in sequence
- Generate an HTML report automatically
- Show detailed console output
- Handle any test failures gracefully

### Alternative Methods

#### Individual Tests
```bash
# Run specific test
pytest i_test_missing_email.py -v -s
pytest ii_test_complete_booking.py -v -s  
pytest iii_test_booking_deletion.py -v -s
```

#### One-Line Setup and Run
```bash
# From project root - setup and run everything
cd tests/playwright_tst && python -m venv ../../venv && source ../../venv/bin/activate && pip install -r ../../requirements.txt && playwright install firefox && python iv_run_all_tests.py
```

## 🔧 Configuration Options

### Room Types
Tests support different room types (1, 2, 3) by modifying the navigation function:

```python
# Default (Room 1)
navigate_to_booking_page(page)

# Specific room type  
navigate_to_booking_page(page, room_type=2, check_api=False)
```

### API Availability Checking
When the API booking persistence is working properly, enable API-based date checking:


## 🛠️ Utility Scripts

### Page Analyzer: `__page_analyzer.py`
Interactive tool for exploring web page elements:

```bash
python __page_analyzer.py
```

Features:
- Analyze current page elements (buttons, inputs)
- Navigate to different URLs
- Discover selectors for test development

### View Test Reports
```bash
# Generate and view HTML test report
pytest i_test_*.py ii_test_*.py iii_test_*.py --html=test_report.html --self-contained-html
```
