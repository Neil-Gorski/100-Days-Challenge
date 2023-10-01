from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime


driver = webdriver.Chrome()
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")



time_start = datetime.now()


store = driver.find_elements(By.CSS_SELECTOR, "#store > div")
print(store)
while True:
    time = datetime.now() - time_start
    if time.seconds >= 3:
        wishlist = []
        store = driver.find_elements(By.CSS_SELECTOR, "#store > div")
        for item in store[:-1]:
            if item.get_attribute('class') != "grayed":
                wishlist.append(item)
        wishlist[-1].click()

        time_start = datetime.now()

    cookie.click()
