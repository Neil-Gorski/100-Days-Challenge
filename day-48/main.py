from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome browser open afeter program finishes
chrom_options = webdriver.ChromeOptions()
chrom_options.add_experimental_option("detach", True)


driver = webdriver.Chrome(options=chrom_options)
driver.get("https://www.python.org/")

events_dates = driver.find_elements(By.CSS_SELECTOR,".event-widget li time")
events_title = driver.find_elements(By.CSS_SELECTOR,".event-widget li a")
events_dates = [date.get_attribute("datetime").split("T")[0] for date in events_dates]
events_title = [title.text for title in events_title]
events_dict = {}
for i in range(len(events_dates)):
    events_dict[i] = {
        "time": events_dates[i],
        "name": events_title[i]
    }

print(events_dict)
driver.close()
