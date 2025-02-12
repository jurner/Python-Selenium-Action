from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
#import tempfile
import time
import os
import xlrd
import pandas as pd

# Install chromedriver if needed
chromedriver_autoinstaller.install()

#temp_dir = tempfile.mkdtemp()
download_dir = "/tmp/selenium_downloads"
os.makedirs(download_dir, exist_ok=True)
chrome_options = webdriver.ChromeOptions()
# Add experimental options to force download location
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_dir,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
})

options = [
    # Remove "--headless" to see the browser in action
    # "--headless",  
    #f"--user-data-dir={temp_dir}",
    "--disable-gpu",
    "--window-size=1920,1200",
]

for option in options:
    chrome_options.add_argument(option)
    
driver = webdriver.Chrome(options=chrome_options)

username = "contact@brewdaz.ch"
password = "Nr1erppw"

try:
    driver.get("https://app.abaninja.ch")
    time.sleep(5)
    
    email_field = driver.find_element(By.ID, "username")
    email_field.send_keys(username)

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    login_button = driver.find_element(By.ID, "kc-login")
    login_button.click()

    time.sleep(5)
    print("Logged in, current page title:", driver.title)
    
    driver.get("https://app.abaninja.ch/accounting/account-statement/150452/1000")
    time.sleep(5)

    button = driver.find_element(By.CSS_SELECTOR, "button.v-btn.secondary .mdi-microsoft-excel")
    button.click()

    time.sleep(5)
    
    downloaded_files = os.listdir(download_dir)
    excel_file = [f for f in downloaded_files if f.endswith(".xls")][0]
    file_path = os.path.join(download_dir, excel_file)
    workbook = xlrd.open_workbook(file_path, ignore_workbook_corruption=True)
    df = pd.read_excel(workbook)
    date_pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    
    df_clean = df[df['Valuta'].str.match(date_pattern, na=False)]
    print(df_clean.head())

finally:
    # Clean up
    driver.quit()
    for f in os.listdir(download_dir):
        os.remove(os.path.join(download_dir, f)) 
