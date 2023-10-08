from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)


driver = webdriver.Chrome(options=options)

driver.get("http://secure-retreat-92358.herokuapp.com/")
fname = driver.find_element(By.NAME, "fName")
fname.send_keys("Neil")
lname = driver.find_element(By.NAME, "lName")
lname.send_keys("Gorski")
email = driver.find_element(By.NAME, "email")
email.send_keys("neil.gorski@msn.com")
singup = driver.find_element(By.CSS_SELECTOR, "button")
singup.click()
