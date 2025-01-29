from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wether_prs(city: str):
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    browser.get("https://yandex.ru/pogoda")
    input_city = browser.find_element(By.CLASS_NAME, "mini-suggest-form__input.mini-suggest__input")
    input_city.send_keys(city)
    sp = browser.find_elements(By.CLASS_NAME, "mini-suggest__item-link")
    if sp:
        sp[0].click()
    else:
        return 'Не знаю такого города, но уверен погода там прекрасная'
    town = browser.find_element(By.XPATH, "//h1[@class='title title_level_1 header-title__title']").text
    temp_now = browser.find_element(By.XPATH, "//div[@class='temp fact__temp fact__temp_size_s']/span[@class='temp__value temp__value_with-unit']").text
    prochee_pogoda = browser.find_element(By.CSS_SELECTOR, ".link__feelings.fact__feelings")
    oblaka_now = prochee_pogoda.find_element(By.CLASS_NAME, "link__condition").text
    oshush_now = prochee_pogoda.find_element(By.CLASS_NAME, "temp__value").text
    rez = f'{town}\nСейчас {temp_now}\n{oblaka_now}\nОщущается как {oshush_now}\n\nЕсли это не твой город, то постарайся написать его так, чтобы яндекс его понял'
    browser.quit()
    return rez




