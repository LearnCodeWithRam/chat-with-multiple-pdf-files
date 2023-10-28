
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

#Extract Text from any web pages.
entry_url = input("Enter Your URL : ")

driver = webdriver.Chrome()
try:
    driver.get(entry_url)
except:
    print(f"Couldn't open {entry_url}")
time.sleep(1)
driver.maximize_window()
text = driver.find_element(By.XPATH, "/html/body").text
all_text = text.replace("\n"," ")
print(all_text)


driver.quit()
