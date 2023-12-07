import bs4
from time import sleep
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import parsing
import db


MAX_PAGE_COUNT = 1  # for debug
DEBUG = False
# HEADLESS = False


def get_gpu_specs(driver: webdriver.Chrome, url: str):
    """
    returns dict:\n
    {\n
    'price' : int # rub\n
    'url' :str \n
    'brand' : str, \n
    'model' : str, \n
    'chipset' : str, \n
    'max_definition' str: , \n
    'base_freq' : int, # MHz \n
    'boost_freq' : int, # MHz \n
    'VRAM' : int, #Mb \n
    'VRAM_freq' : int, # MHz \n
    'bandwidth' : int, # GB/s \n
    'HDMI_count' : int, \n
    'DisplayPort_count' : int, \n
    'power_pin_count' : int, \n
    'guarantee' : int  # months \n
    }
    """
    driver.get(url + "properties/")
    sleep(3)
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    spec_blocks = soup.find_all(
        'li', attrs={'class': 'app-catalog-10ib5jr e14ta1090'})
    price_raw = soup.find(
        'span', {"class": "e1j9birj0 e106ikdt0 app-catalog-1f8xctp e1gjr6xo0"}).text
    price = int("".join(price_raw.split()))
    specs = dict()
    specs["url"] = url
    specs["price"] = price
    for block in spec_blocks:
        block: bs4.Tag
        # commented out parts are deemed irrelevant
        block_title = block.h4.text
        if "Основные характеристики" in block_title:
            data = parsing.parse_main(block)
        elif "Память" in block_title:
            data = parsing.parse_memory(block)
        elif "Разъемы" in block_title:
            data = parsing.parse_sockets(block)
        elif "Питание" in block_title:
            data = parsing.parse_power(block)
        # elif "Размеры" in block_title:
        #     data = parsing.parse_size(block)
        elif "Дополнительные характеристики" in block_title:
            data = parsing.parse_guarantee(block)
        else:
            print(f"skipped {block_title}")
            continue
        specs = {**specs, **data}
    return specs


def get_product_urls(driver: webdriver.Chrome, start_url: str) -> list[str]:
    """
    returns list[str] with absolute urls of products
    """
    product_urls: list[str] = []
    page = 1
    first_url = ''
    while(True):
        print(f"page {page}:")
        if (page > MAX_PAGE_COUNT) and DEBUG:  # debug
            print("exit on DEBUG")
            break
        page_url = f"{start_url}?p={page}"
        driver.get(page_url)
        print("sleeping 5")
        sleep(5)
        soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
        main_section = soup.find(
            'section', {"class": "edhylph0 app-catalog-1yo09mv e3tyxgd0"})
        tittle_elements: list[bs4.PageElement] = main_section.find_all(
            'a', attrs={'class': 'app-catalog-9gnskf e1259i3g0'})
        print(f"elements collected; on this page: {len(tittle_elements)}")
        if not tittle_elements:
            # empty page
            print("exit on empty page")
            break
        if first_url == tittle_elements[0].attrs['href']:
            # first page is displayed again
            print("exit on repeat")
            break
        elif first_url == '':
            first_url = tittle_elements[0].attrs['href']
        # print(len(tittle_elements), type(tittle_elements[0]))
        for e in tittle_elements:
            e: bs4.element.Tag
            relative_url = e.attrs['href']
            product_urls.append("https://www.citilink.ru/" + relative_url)
        page += 1

    return product_urls


def scrape():
    print("starting driver")
    options = Options()
    # if HEADLESS:
    #     # note that headless driver can, sometimes hang
    #     options.add_argument("--headless=new")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    with Chrome(options=options) as driver:
        # driver.implicitly_wait(5)
        print("acquiring urls")
        urls = get_product_urls(
            driver, "https://www.citilink.ru/catalog/videokarty/")
        print("urls acquired")
        for url in urls:
            print("-----------------------------------------------------------------")
            print(f"url: {url}")
            # probably can be done in threads
            specs = get_gpu_specs(driver, url)
            print(specs)
            db.save_gpu(specs)
            sleep(5)
        print("-----------------------------------------------------------------")
        print(f"scraped {len(urls)} gpus")
