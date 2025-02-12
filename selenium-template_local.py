from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import tempfile

# Install chromedriver if needed
chromedriver_autoinstaller.install()

temp_dir = tempfile.mkdtemp()
chrome_options = webdriver.ChromeOptions()
options = [
    # Remove "--headless" to see the browser in action
    # "--headless",  
    f"--user-data-dir={temp_dir}",
    "--disable-gpu",
    "--window-size=1920,1200",
]

for option in options:
    chrome_options.add_argument(option)
    
driver = webdriver.Chrome(options=chrome_options)

driver.get('http://github.com')
print(driver.title)
with open('./GitHub_Action_Results.txt', 'w') as f:
    f.write(f"This was written locally: {driver.title}")

driver.quit()  # Don't forget to close the browser 
