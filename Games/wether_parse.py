from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wether_prs(city: str):
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
