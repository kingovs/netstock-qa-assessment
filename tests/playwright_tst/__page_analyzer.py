"""
Minimal page analyzer - analyze pages and navigate URLs
"""
from playwright.sync_api import sync_playwright


def analyze_page(page):
    """Show key elements on current page"""
    print(f"\n{'='*60}")
    print(f"URL: {page.url}")
    print("="*60)
    
    # Show buttons
    buttons = page.locator("button").all()
    if buttons:
        print(f"\nBUTTONS ({len(buttons)}):")
        for i, btn in enumerate(buttons):
            try:
                text = btn.text_content().strip() or "No text"
                visible = btn.is_visible()
                btn_id = btn.get_attribute("id") or ""
                btn_class = btn.get_attribute("class") or ""
                
                print(f"  {i}: '{text}' (visible={visible})")
                if btn_id: print(f"id='{btn_id}'")
                if btn_class: print(f"class='{btn_class[:50]}...'")
            except:
                print(f"  {i}: Error reading button")
    
    # Show inputs
    inputs = page.locator("input").all()
    if inputs:
        print(f"\nINPUTS ({len(inputs)}):")
        for i, inp in enumerate(inputs):
            try:
                input_type = inp.get_attribute("type") or "text"
                placeholder = inp.get_attribute("placeholder") or ""
                name = inp.get_attribute("name") or ""
                input_id = inp.get_attribute("id") or ""
                visible = inp.is_visible()
                
                print(f"  {i}: type='{input_type}' (visible={visible})")
                if placeholder: print(f"placeholder='{placeholder}'")
                if name: print(f"name='{name}'")
                if input_id: print(f"id='{input_id}'")
            except:
                print(f"  {i}: Error reading input")


def run_analyzer():
    """Run page analyzer"""
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        
        print("PAGE ANALYZER")
        
        # Start at booking site
        page.goto("https://automationintesting.online")
        analyze_page(page)
        
        while True:
            print(f"\nOPTIONS:")
            print("1. Analyze current page")
            print("2. Go to URL")
            print("3. Exit")
            
            choice = input("\nEnter choice: ").strip()
            
            if choice == "1":
                analyze_page(page)
                
            elif choice == "2":
                url = input("Enter URL: ").strip()
                try:
                    page.goto(url)
                    page.wait_for_timeout(2000)
                    print(f"Navigated to: {page.url}")
                except Exception as e:
                    print(f"Error: {e}")
                    
            elif choice == "3":
                break
                
            else:
                print("Invalid choice")
        
        browser.close()


if __name__ == "__main__":
    run_analyzer()