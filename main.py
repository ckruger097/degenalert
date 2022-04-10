from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import send_sms
from random import randrange

DRIVER_PATH = './chromedriver'

coins = {
    "SHADE": "https://kek.tools/t/0x3a3841f5fa9f2c283ea567d5aeea3af022dd2262",
    "BOO": "https://kek.tools/t/0x841fad6eae12c286d1fd18d1d525dffa75c7effe",
    "FTM": "https://kek.tools/t/0x4e15361fd6b4bb609fa63c81a2be19d873717870",
    "ETH": "https://kek.tools/t/0x74b23882a30290451a17c44f4f05243b6b58c76d"
}

coins_price = {
    "SHADE": 2.99,
    "BOO": 22.193,
    "FTM": 1.25,
    "ETH": 3946.29
}


def scrape_price(coin_query):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    wait = WebDriverWait(driver, 20)
    driver.get(coins[coin_query])
    price = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//input[@class="sc-ciSkZP sc-bjHqKj bwSYJA dbQnLk" and @tabindex="2"]')))
    price_value = (price.get_attribute("value"))
    driver.quit()
    if "," in price_value:
        price_value = price_value.replace(",", "")
    print(coin_query, price_value)
    return coin_query, float(price_value)


def percentage_diff(price1, price2):
    diff = abs(price1 - price2) / ((price1 + price2) / 2)
    return diff


def calc_change(token_query, price):
    threshold = 0.075
    old_price = coins_price[token_query]
    minus_threshold = old_price - (old_price * threshold)
    pos_threshold = old_price + (old_price * threshold)
    # update dict for next time
    coins_price[token_query] = price
    diff = percentage_diff(price, old_price)
    if price < minus_threshold:
        return "DOWN ALERT: " + token_query + " has shifted by -" + str(
            diff * 100) + "%. Current price is: " + str(
            round(price, 2))
    elif price > pos_threshold:
        return "UP ALERT: " + token_query + " has shifted by +" + str(diff * 100) + "%. Current price is: " + str(
            round(price, 2))
    else:
        return ""


if __name__ == '__main__':
    while True:
        rand_exec = randrange(600, 1200, 60)
        time.sleep(rand_exec)
        for coin in coins.keys():
            rand_loop = randrange(300, 600, 60)
            token, now_price = scrape_price(coin)
            if now_price == 1:
                print('1 for some reason?')
                continue
            else:
                result = calc_change(token, now_price)
                if result != "":
                    send_sms.send(result)
                else:
                    print("coin didn't shift enough.", coin, coins_price[coin])
            time.sleep(rand_loop)
            #time.sleep(39)
