from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

import sys
import os
import json

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# driver = webdriver.Chrome(resource_path('./driver/chromedriver.exe'))

driver = webdriver.Chrome(ChromeDriverManager().install())

# chrome_driver_path = "./chromedriver"
# driver = webdriver.Chrome(chrome_driver_path)

base_url = "https://hrms.reckon.com.hk/en/Account/LogOn"

driver.get(base_url)
wait = WebDriverWait(driver, 30)

# Extract JSON meta data
f = open("./meta_data.json")

meta_data = json.load(f)

blockUIs = meta_data["blockUI_elements"]
login_credentials = meta_data["credentials"]
login_xpath = meta_data["login"]
dashboard_xpath = meta_data["dashboard"]
audit_log_xpath = meta_data["audit_log_page"]
calendar_xpath = meta_data["calendar"]

if len(login_credentials["username"]) <= 0 or len(login_credentials["password"]) <= 0 or len(login_credentials["company_domain"]) <= 0:
    print("Please check meta_data.json (Username / Company Domain / Password invalid)")
    driver.close()
else:
    # Fill in sign-in credentials
    driver.find_element(By.XPATH, login_xpath["username_input"]).send_keys(login_credentials["username"])
    driver.find_element(By.XPATH, login_xpath["company_domain_input"]).send_keys(login_credentials["company_domain"])
    driver.find_element(By.XPATH, login_xpath["password_input"]).send_keys(login_credentials["password"])

    # Submit login request
    driver.find_element(By.XPATH, login_xpath["submit_btn"]).click()

    # Wait for BlockUI to be invisible
    wait.until(EC.invisibility_of_element_located((By.XPATH, blockUIs["blockUI"])))
    wait.until(EC.invisibility_of_element_located((By.XPATH, blockUIs["blockUIPage"])))

    # Navigate to the security tab
    driver.find_element(By.XPATH, dashboard_xpath["security_tab"]).click()

    # Wait for BlockUI to be invisible
    wait.until(EC.invisibility_of_element_located((By.XPATH, blockUIs["blockUI"])))
    wait.until(EC.invisibility_of_element_located((By.XPATH, blockUIs["blockUIPage"])))

    # Navigate to the audit log page
    driver.find_element(By.XPATH, dashboard_xpath["audit_log_btn"]).click()

    # wait for BlockUI to be invisible
    wait.until(EC.invisibility_of_element_located((By.XPATH, blockUIs["blockUI"])))
    wait.until(EC.invisibility_of_element_located((By.XPATH, blockUIs["blockUIPage"])))

    # click and wait for options dropdown to show
    options_xpath = audit_log_xpath["options_dropdown"]

    driver.find_element(By.XPATH, options_xpath["dropdown"]).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, options_xpath["deselect_all"])))

    driver.find_element(By.XPATH, options_xpath["deselect_all"]).click()
    driver.find_element(By.XPATH, options_xpath["option_1"]).click()
    driver.find_element(By.XPATH, options_xpath["option_2"]).click()
    driver.find_element(By.XPATH, options_xpath["option_3"]).click()
    driver.find_element(By.XPATH, options_xpath["option_4"]).click()

    # setting up month and date xpath variables
    month_xpath = calendar_xpath["month"]

    month = meta_data["settings"]["month"]
    date_row = meta_data["settings"]["start_row"]
    date_column = meta_data["settings"]["start_col"]

    for i in range(meta_data["settings"]["no_of_days"]):
        print("Loop Started")

        if date_column == 7:
            date_column = 1
            date_row += 1
        else:
            if i != 0:
                date_column += 1

        date_xpath = f'/html/body/div[3]/table/tbody/tr[{date_row}]/td[{date_column}]'

        # click txtFromDate input value
        wait.until(EC.presence_of_element_located((By.XPATH, audit_log_xpath["fromDate_input"])))
        wait.until(EC.element_to_be_clickable((By.XPATH, audit_log_xpath["fromDate_input"])))
        driver.find_element(By.XPATH, audit_log_xpath["fromDate_input"]).click()

        # wait for txtFromDate calendar to be visible
        wait.until(EC.visibility_of_element_located((By.XPATH, calendar_xpath['visibility_check'])))
        
        # wait for dropdown to be clickable
        # click dropdown to reveal dropdown options (Month)
        wait.until(EC.element_to_be_clickable((By.XPATH, month_xpath["dropdown"])))
        driver.find_element(By.XPATH, month_xpath["dropdown"]).click()

        # pick month
        # wait.until(EC.element_to_be_clickable((By.XPATH, month_xpath['jan'])))
        driver.find_element(By.XPATH, month_xpath[month]).click()

        # pick date
        # wait.until(EC.element_to_be_clickable((By.XPATH, date_xpath)))
        driver.find_element(By.XPATH, date_xpath).click()

        # click "Search"
        driver.find_element(By.XPATH, audit_log_xpath["search_btn"]).click()

        # wait 30mins for blockUI to disappear
        longWait = WebDriverWait(driver, 1800)
        longWait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, blockUIs["cssSelector"])))

        # click "Generate"
        driver.find_element(By.XPATH, audit_log_xpath["generate_btn"]).click()

        longWait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, blockUIs["iframeSelector"])))
        longWait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, blockUIs["cssSelector"])))

        # see if no record dialog pops up
        try:
            no_record_btn = driver.find_element(By.CSS_SELECTOR, audit_log_xpath["no_record_btn"])
            no_record_btn.click()

        except NoSuchElementException:
            print("No Records Moving Forward")

        print(f'Done {i + 1}')

    driver.close()
