from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


EMAIL = "harrymax042@gmail.com"
PASSWORD = "Dev.hamza45@"
LOGIN_URL = "https://hamza20.odoo.com/web/login?redirect=%2Fodoo%3F"
ATTENDANCE_URL = "https://hamza20.odoo.com/odoo/attendances"

options = Options()
# options.add_argument("--headless")  # Optional for running in background
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

try:
    print("🔐 Logging in...")
    driver.get(LOGIN_URL)
    wait.until(EC.visibility_of_element_located((By.NAME, "login"))).send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    wait.until(EC.url_changes(LOGIN_URL))
    print("🌐 Navigating to attendance page...")
    driver.get(ATTENDANCE_URL)

    # 1️⃣ Open the dot menu dropdown
    print("➡️ Opening dropdown menu...")
    dot_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'dropdown-toggle') and .//i[@aria-label='Attendance']]")))
    dot_dropdown.click()

    time.sleep(1)  # slight pause to let dropdown appear

    # 2️⃣ Click Check Out or Check In
    try:
        print("🔍 Checking for 'Check out'...")
        check_out = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Check out')]]")))
        check_out.click()
        print("✅ Checked out successfully.")
    except:
        print("🔍 Checking for 'Check in'...")
        check_in = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Check in')]]")))
        check_in.click()
        print("✅ Checked in successfully.")

    driver.save_screenshot("final_screenshot.png")
    print("📸 Screenshot saved.")

except Exception as e:
    print("❌ Error occurred:", e)

finally:
    driver.quit()
