from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wether_sl(city: str):
    # Инициализация браузера
    browser = webdriver.Chrome()

    try:
        # Переходим на сайт погоды Яндекса
        browser.get("https://yandex.ru/pogoda")

        # Ожидаем загрузки поля ввода города
        input_city = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mini-suggest-form__input.mini-suggest__input"))
        )

        # Вводим название города
        input_city.send_keys(city)

        # Ожидаем появления списка предложений и кликаем на первое предложение
        suggestions = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "mini-suggest__item-link"))
        )

        if suggestions:
            suggestions[0].click()
        else:
            return 'Не знаю такого города, но уверен погода там прекрасная'

        # Ожидаем загрузки страницы с прогнозом для выбранного города
        town = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[@class='title title_level_1 header-title__title']"))
        ).text

        # Извлекаем температуру, облачность и ощущаемую температуру
        temp_now = browser.find_element(By.XPATH,
                                        "//div[@class='temp fact__temp fact__temp_size_s']/span[@class='temp__value temp__value_with-unit']").text
        prochee_pogoda = browser.find_element(By.CSS_SELECTOR, ".link__feelings.fact__feelings")
        oblaka_now = prochee_pogoda.find_element(By.CLASS_NAME, "link__condition").text
        oshush_now = prochee_pogoda.find_element(By.CLASS_NAME, "temp__value").text

        # Формируем итоговый результат
        result = (f'{town}\nСейчас {temp_now}\n{oblaka_now}\nОщущается как {oshush_now}\n\n'
                  f'🙃 Если это не твой город, то постарайся написать его так, чтобы яндекс его понял')

        return result

    except:
        return f"Произошла ошибка, но я уверен, что погода то, что надо!"

    finally:
        # Закрываем браузер в любом случае
        browser.quit()


""" 
    Новый парсер на BeautifulSoup, так как выделенный сервер не позволит работать selenium
"""


import requests
from bs4 import BeautifulSoup

def weather_bs(city: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.meteoservice.ru/"
    }

    # Формируем URL для поиска города
    search_url = f"https://www.meteoservice.ru/location/search?q={city}"

    try:
        # Запрос к странице поиска
        search_response = requests.get(search_url, headers=headers)
        search_soup = BeautifulSoup(search_response.text, "html.parser")
        if 'overview' in search_response.url:
            weather_url = search_response.url.replace("overview", 'now')
        else:

            # Ищем первую ссылку на страницу погоды
            first_result = search_soup.find('div', class_="row align-middle margin-bottom-1").find('a')['href']
            first_result = first_result.replace("overview", 'now')

            # Получаем URL страницы погоды для города
            weather_url = "https://www.meteoservice.ru" + first_result

        # Запрос к странице с погодой
        weather_response = requests.get(weather_url, headers=headers)
        weather_soup = BeautifulSoup(weather_response.text, "html.parser")

        # Получаем температуру
        temp_now = weather_soup.select_one(".temperature .value").text

        # Получаем описание погоды (облачность, осадки и т. д.)
        oblaka_now = weather_soup.select(".callout .row .small-12 .margin-bottom-0")[0].text
        # Получаем "ощущается как"
        oshush_now = weather_soup.select_one(".feeled-temperature .value").text
        # Получаем "Влажность"
        vlazhnost = weather_soup.find('span', string='Влажность').find_next('div', class_='h5 margin-bottom-0').text.strip()
        # Получаем "Ветер"
        veter = weather_soup.find('span', string='Ветер').find_next('div', class_='h5 margin-bottom-0').text
        veter = " ".join(veter.split())

        # Формируем итоговый результат
        result = (
            f"{city}\nСейчас {temp_now}\n{oblaka_now}\nОщущается как {oshush_now}\nВлажность {vlazhnost}\nВетер {veter}\n\n"
            "🙃 Если это не твой город, попробуй написать его точнее!"
        )

        return result

    except Exception as e:
        return f"Произошли технические шоколадки🍫🍫🍫\n\nНо я уверен, что погода отличная! ☀️"

