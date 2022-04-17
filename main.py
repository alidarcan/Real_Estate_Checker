from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

header = {
    "Accept-Language": "tr,en-US;q=0.9,en;q=0.8,bg;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}
response = requests.get(URL, headers=header)
soup = BeautifulSoup(response.text, "html.parser")
addresses_raw = soup.select(selector=".list-card-addr")
prices_raw = soup.select(selector=".list-card-price")
links_raw = soup.select(selector=".list-card-link.list-card-img")

addresses = [address.text for address in addresses_raw]
prices = [int(((price.text.split("/")[0]).replace(",", "")).replace("$", "").split("+")[0]) for price in prices_raw]
links_unchecked = [link.get("href") for link in links_raw]
links = []

for link in links_unchecked:
    check_url = "https://www.zillow.com"
    if check_url in str(link):
        links.append(link)
    else:
        link = check_url + str(link)
        links.append(link)
links = links[:-1]
# estate_dict = {}
# for n in range(len(addresses)):
#     estate_dict[n] = {}
#     estate_dict[n]["address"] = addresses[n]
#     estate_dict[n]["price"] = prices[n]
#     estate_dict[n]["link"] = links[n]

service = Service(executable_path='/Users/alida/OneDrive/Desktop/100 Days Of Code/Chrome Driver/chromedriver')
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe3oNhl23f5_47eGEDj4xaWzzNpoh0pKOGcoQqQ-zoHAMqRWA/viewform"
driver = webdriver.Chrome(service=service)

for n in range(len(addresses)):
    driver.get(FORM_URL)
    time.sleep(2)

    input_address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    input_address.send_keys(addresses[n])
    input_price.send_keys(prices[n])
    input_link.send_keys(links[n])
    submit_button.click()
