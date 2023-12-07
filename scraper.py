from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://duproprio.com/en/search/list?search=true&regions%5B0%5D=1&regions%5B1%5D=10&regions%5B2%5D=11&regions%5B3%5D=114&regions%5B4%5D=115&regions%5B5%5D=12&regions%5B6%5D=13&regions%5B7%5D=14&regions%5B8%5D=15&regions%5B9%5D=16&regions%5B10%5D=17&regions%5B11%5D=2&regions%5B12%5D=257&regions%5B13%5D=3&regions%5B14%5D=31&regions%5B15%5D=4&regions%5B16%5D=5&regions%5B17%5D=6&regions%5B18%5D=7&regions%5B19%5D=8&regions%5B20%5D=9&parent=1&pageNumber=1&sort=-published_at")
button_xpath = '//a[@class="search-results-listings-list__item-image-link "]'
button = driver.find_elements(By.XPATH, button_xpath)
links = [elem.get_attribute('href') for elem in button]

for i, link in enumerate(links, 1):
    driver.get(link)

    phone_elements = driver.find_elements(By.XPATH, '//span[@class="listing-contact__number"]')
    house_type_elements = driver.find_elements(By.XPATH, '//h3[@class="listing-location__title"]')
    city_elements = driver.find_elements(By.XPATH, '//div[@class="listing-location__address"]/h2/span')
    region_elements = driver.find_elements(By.XPATH, '//div[@class="listing-location__address"]/h2/span[2]')
    asking_elements = driver.find_elements(By.XPATH, '//div[@class="listing-box__dotted-row"]/div[contains(text(), "Asking Price")]/following-sibling::div[2]')
    municipal_elements = driver.find_elements(By.XPATH,'//div[@class="listing-box__dotted-row"]/div[contains(text(), "Municipal Assessment")]/following-sibling::div[2]')

    house_type = house_type_elements[0].get_attribute("textContent").replace('\n', '') if house_type_elements else "N/A"
    region = city_elements[0].get_attribute("textContent").replace('\n', '') if city_elements else "N/A"
    city = region_elements[0].get_attribute("textContent").replace('\n', '') if region_elements else "N/A"
    asking = asking_elements[0].get_attribute("textContent").replace('\n', '') if asking_elements else "N/A"
    municipal = municipal_elements[0].get_attribute("textContent").replace('\n', '') if municipal_elements else "N/A"
    url = driver.current_url
    phone = phone_elements[0].get_attribute("textContent").replace('\n', '') if phone_elements else "N/A"

    data = {"URL": url, "House_Type": house_type, "Region": region, "City": city, "Asking_Price": asking, "Municipal_Assessment": municipal, "Phone_Number": phone}

    df = pd.DataFrame([data])
    if i == 1:
        df.to_csv("data.csv", mode='w', index=False, encoding='utf-8')
    else:
        df.to_csv("data.csv", mode='a', header=False, index=False, encoding='utf-8')

driver.quit()
