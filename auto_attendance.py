import random
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys

# ==== CONFIGURATION ====
LOGIN_URL = "https://hrm.syntracx.com/web/login?redirect=%2Fodoo%3F"
ATTENDANCE_URL = "https://hrm.syntracx.com/odoo/attendances"

EMAIL = os.getenv("ODOO_EMAIL")
PASSWORD = os.getenv("ODOO_PASSWORD")
ACTION = sys.argv[1] if len(sys.argv) > 1 else "auto"  # "checkin", "checkout", or "auto"

def random_delay(minutes=10):
    delay = random.randint(0, minutes * 60)
    print(f"⏳ Waiting {delay // 60} min {delay % 60} sec before {ACTION}...")
    time.sleep(delay)

# ==== SELENIUM SETUP ====
chrome_options = Options()
chrome_options.add_argument("--headless")  # comment this line to see browser during test
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

try:
    random_delay(10)  # Random delay within 10 minutes

    # 1. Open Login Page
    driver.get(LOGIN_URL)
    time.sleep(3)

    # 2. Enter credentials
    driver.find_element(By.NAME, "login").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

    # 3. Go to attendance page
    driver.get(ATTENDANCE_URL)
    time.sleep(5)

    # 4. Click button based on action
    if ACTION.lower() == "checkin":
        driver.find_element(By.XPATH, "//button[span[text()='Check in']]").click()
        print("✅ Checked in successfully.")
    elif ACTION.lower() == "checkout":
        driver.find_element(By.XPATH, "//button[span[text()='Check out']]").click()
        print("✅ Checked out successfully.")
    else:
        # Auto mode: try checkout first, fallback to checkin
        try:
            driver.find_element(By.XPATH, "//button[span[text()='Check out']]").click()
            print("✅ Auto: Checked out.")
        except:
            try:
                driver.find_element(By.XPATH, "//button[span[text()='Check in']]").click()
                print("✅ Auto: Checked in.")
            except:
                print("⚠️ Already checked in or out — no action taken.")

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    driver.quit()