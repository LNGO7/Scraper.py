from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import os
import json
import tkinter as tk
from tkinter import filedialog


username = os.environ.get('UNOB')
password = os.environ.get('PASSWORD')

# Headless mode (bezi na pozadi)
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

# Otevreni pozadované stránky
odkaz = "https://vav.unob.cz/department/index/121"
driver.get(odkaz)
# Shodí okno do lišty ať furt nevyskakuje stránka
driver.minimize_window()
# Najde login pole a vyplní údaje
username_pole = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
username_pole.send_keys(username)

password_pole = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
password_pole.send_keys(password)

# Klikne na login tlačítko
login_button = driver.find_element(By.CSS_SELECTOR, ".button-background")
login_button.click()

# Find all the <a> elements with "/index" in the href attribute
link_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/index")]')

# List to store the UČO numbers
uco_list = []
import time
# Iterate over the link elements and click on each link
for link_element in link_elements:
    link_url = link_element.get_attribute("href")
    driver.get(link_url)
    
    time.sleep(2)

    page = driver.page_source
    print(page.index("UČO"))
    
    # Find the UČO element
    uco_element = driver.find_element(By.XPATH, '//tr[td[text()="UČO"]]/td[@class="left-align"]')
    
    # Get the UČO number
    uco = uco_element.text.strip()
    
    # Add UČO number to the list
    uco_list.append(uco)
    
    # Go back to the previous page
    driver.back()

# Quit the WebDriver
driver.quit()

# Write UČO numbers to a JSON file
data = {"UČO": uco_list}

with open("uco_numbers.json", "w") as f:
    json.dump(data, f, indent=4)

print("UČO numbers were successfully written to the JSON file.")