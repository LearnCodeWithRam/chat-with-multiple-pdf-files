from selenium.common.exceptions import NoSuchElementException
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

# For Link Extraction.
def extract_links_by_tagName(tag_name):
    links = set()
    try:
        a_elems = driver.find_elements(By.TAG_NAME, tag_name)
        for elem in a_elems:
            link = elem.get_attribute("href")
            if link == "javascript:void(0)":
                continue
            # Remove links to images and various files (if needed)
            # You can customize this part to filter links as desired
            if (
                link.endswith(".png")
                or link.endswith(".json")
                or link.endswith(".txt")
                or link.endswith(".svg")
                or link.endswith(".ipynb")
                or link.endswith(".jpg")
                or link.endswith(".pdf")
                or link.endswith(".mp4")
                or "mailto" in link
                or len(link) > 300
            ):
                continue
            # Remove anchors
            link = link.split("#")[0]
            # Remove parameters
            link = link.split("?")[0]
            # Remove trailing forward slash
            link = link.rstrip("/")
            links.add(link)
        return list(links)
    except:
        return []
    
all_links = extract_links_by_tagName("a")

# Lists of class names
top_nav_class = ["top-navigation", "header-main__slider", "navbar", "navbar-nav", "menu", "nav", "header", "top-bar","CJF7A2"]
left_nav_class = ["left-navigation", "nav-menu", "sideBar"]
collected_links = set()

# Loop through the top navigation class names
for class_name in top_nav_class:
    try:
        element = driver.find_element(By.CLASS_NAME,class_name)
        elements = element.find_elements(By.TAG_NAME,'a')
        for element in elements:
            link = element.get_attribute('href')
            if link:
                link = link.split("#")[0]
                link = link.split("?")[0]
                link = link.rstrip("/")
            if link:
                collected_links.add(link)
    except NoSuchElementException:
        # Handle the case when the class name is not found
        pass

# Loop through the left navigation class names
for class_name in left_nav_class:
    try:
        element = driver.find_element(By.CLASS_NAME,class_name)
        elements = element.find_elements(By.TAG_NAME,'a')
        for element in elements:
            link = element.get_attribute('href')
            if link:
                link = link.split("#")[0]
                link = link.split("?")[0]
                link = link.rstrip("/")
            if link:
                collected_links.add(link)
    except NoSuchElementException:
        # Handle the case when the class name is not found
        pass
Nav_links = set(collected_links)
for l in Nav_links:
    print(l)
#print(Nav_links)
# for link in Nav_links:
#     #print(link)
#     try:
#         driver.get(link)
#     except:
#         print(f"Couldn't open {entry_url}")
#     time.sleep(1)
#     driver.maximize_window()
#     text1 = driver.find_element(By.XPATH, "/html/body").text
#     all_text += text.replace("\n"," ")
#     #print(all_text)

driver.quit()
