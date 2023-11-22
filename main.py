from time import sleep
import bs4
from selenium import webdriver
from selenium.webdriver import Chrome
import parsing


def get_gpu_chars(driver: webdriver.Chrome, url: str):
    driver.get(url+"properties/")
    sleep(3)
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    char_blocks = soup.find_all(
        'li', attrs={'class': 'app-catalog-10ib5jr e14ta1090'})
    chars = dict()
    for block in char_blocks:
        block: bs4.Tag
        if "Основные характеристики" in block.h4.text:
            data = parsing.parse_main(block)
        elif "Память":
            data = parsing.parse_memory(block)
        elif "Охлаждение":
            data = parsing.parse_cooling(block)
        elif "Конструкция":
            data = parsing.parse_construction(block)
        elif "Технологии":
            data = parsing.parse_technologies(block)
        elif "Разъемы":
            data = parsing.parse_sockets(block)
        elif "Питание":
            data = parsing.parse_power(block)
        elif "Особенности":
            data = parsing.parse_extra(block)
        elif "Размеры":
            data = parsing.parse_size(block)
        elif "Дополнительные характеристики":
            data = parsing.parse_guarantee(block)
        else:
            print("skipper")
            continue
        chars = {**chars, **data}
    return chars


def get_product_urls(driver: webdriver.Chrome, start_url: str) -> list[str]:
    product_urls: list[str] = []
    page = 1

    while(True):
        print(f"page {page}:")
        page_url = f"{start_url}?page={page}"
        driver.get(page_url)
        print("sleeping 10")
        sleep(10)
        soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
        tittle_elements: list[bs4.PageElement] = soup.find_all(
            'a', attrs={'class': 'app-catalog-9gnskf e1259i3g0'})
        print("elements collected")
        if not tittle_elements:
            break

        print(len(tittle_elements), type(tittle_elements[0]))
        for e in tittle_elements:
            e: bs4.element.Tag
            relative_url = e.attrs['href']
            product_urls.append("https://www.citilink.ru/"+relative_url)
        page += 1

    return product_urls


def main():

    with Chrome() as driver:
        driver.implicitly_wait(5)
        urls = get_product_urls(
            driver, "https://www.citilink.ru/catalog/videokarty/")


if __name__ == "__main__":
    main()
