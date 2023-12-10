import bs4
import re
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import db

# docker-compose loses stdout
import sys
sys.stdout = sys.stderr

OVERLY_VERBOSE = False    # print details
DEBUG = False             # scrape only one page

NUMBER_PATTERN = re.compile("[0-9]+")
FREQ_PATTERN = re.compile("[0-9]+(?!МГц)")
MEM_PATTERN = re.compile("[0-9]+(?!ГБ)")
HDMI_PATTERN = re.compile("(?<=HDMI\sх\s)[0-9]+")
DISPLAYPORT_PATTERN = re.compile("(?<=Display\sPort\sх\s)[0-9]+")


def parse_specs(gpu_card: bs4.Tag):
    """
    returns dict:\n
    {
        'id' : int,
        'url' : str,
        'price' : int,
        'brand' : str, 
        'name' : str, 
        'chipset' : str, 
        'base_freq' : int,
        'boost_freq' : int,
        'VRAM' : int,
        'VRAM_freq' : int, 
        'HDMI_count' : int, 
        'DisplayPort_count' : int, 
        'power_input' : int,
        'pin_count' : int, 
    }
    """
    specs = dict()
    # get loose values
    title = gpu_card.find('a', {'class': 'app-catalog-9gnskf e1259i3g0'})
    full_name = title.text[11:]
    specs['brand'] = full_name[:full_name.find(' ')]
    specs['name'] = full_name[full_name.find(' ') + 1:]
    specs['url'] = "https://www.citilink.ru" + title.attrs['href']
    price_raw = gpu_card.find(
        'span', {"class": 'e1j9birj0 e106ikdt0 app-catalog-j8h82j e1gjr6xo0'}).text
    specs["price"] = int("".join(list(NUMBER_PATTERN.findall(price_raw))))
    # get specs
    spec_items = gpu_card.find_all(
        'li', {'class': 'app-catalog-17ju59h e4qu3682'})
    if OVERLY_VERBOSE:
        print(f"parsing {specs['full_name']}")
    for item in spec_items:
        name = item.span.text
        # print(name)
        if "Видеочипсет" in name:
            line: str = item.text
            first_coma = line.find(',')
            specs['chipset'] = line[12:first_coma]
            numbers = FREQ_PATTERN.findall(line[first_coma:])
            if len(numbers) == 1:
                specs['base_freq'] = int(numbers[0])
                specs['boost_freq'] = int(numbers[0])
            else:
                specs['base_freq'] = int(numbers[0])
                specs['boost_freq'] = int(numbers[1])
            pass
        elif "Память" in name:
            nums = NUMBER_PATTERN.findall(item.text)
            specs['VRAM'] = int(nums[0])
            specs['VRAM_freq'] = int(nums[2])
        elif "Разъемы" in name:
            hdmi = HDMI_PATTERN.findall(item.text)
            if hdmi:
                specs["HDMI_count"] = int(hdmi[0])
            else:
                specs["HDMI_count"] = 0
            displayport = DISPLAYPORT_PATTERN.findall(item.text)
            if displayport:
                specs["DisplayPort_count"] = int(displayport[0])
            else:
                specs["DisplayPort_count"] = 0

        elif "Питание" in name:
            numbers = NUMBER_PATTERN.findall(item.text)
            if len(numbers) == 0:
                specs["power_input"] = 0
                specs["pin_count"] = 0
            if len(numbers) == 1:
                specs["power_input"] = int(numbers[0])
                specs["pin_count"] = 0
            elif len(numbers) == 2:
                specs["pin_count"] = int(numbers[0])
                specs["power_input"] = int(numbers[1])
            elif '+' in item.text:
                specs["pin_count"] = int(numbers[0]) + int(numbers[1])
                specs["power_input"] = int(numbers[2])
            else:
                print(" -!  PROBLEM: " + item.text)
                print(f"found {len(numbers)}, {numbers}")
        else:
            if OVERLY_VERBOSE:
                print(f"  - skipped \"{name}\"")
    return specs


def get_gpus(driver: webdriver.Chrome, page_url: str) -> list[dict]:
    """
    returns list[dicts] with gpus from parse_specs\n
    """
    gpus = []
    driver.get(page_url)
    st = random.randint(5, 15)
    print(f"sleeping {st}s")
    sleep(st)
    soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
    main_section = soup.find(
        'section', {"class": "edhylph0 app-catalog-1yo09mv e3tyxgd0"})
    gpu_item_blocks = main_section.find_all(
        'div', {"class": "e12wdlvo0 app-catalog-1bogmvw e1loosed0"})
    print("start parsing")
    for block in gpu_item_blocks:
        try:
            gpus.append(parse_specs(block))
        except Exception:
            print(" !!! - failed to parse a block")
            print(block.text)
    print("end parsing")
    return gpus


def scrape():
    db.remake_db(True)
    print("starting driver")
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--headless=new")
    options.add_argument('--start-maximized')

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    with Chrome(options=options) as driver:
        print("stating scraping")
        url = "https://www.citilink.ru/catalog/videokarty/?p="
        page = 1
        scraped = 1
        first_gpu_url = ''
        count = 0
        while scraped:
            try:
                gpus = get_gpus(driver, url+str(page))
            except Exception:
                print(f" !!! failed to scrape page {page}")
                continue
            scraped = len(gpus)
            page += 1
            print("scrape finished, saving")
            if not gpus:
                print(' - exit on empty scrape')
                break
            if first_gpu_url == '':
                first_gpu_url = gpus[0]["url"]
            elif first_gpu_url == gpus[0]["url"]:
                print(" !!! returned to p=1. Exiting")
                scraped = 0
                gpus = []
            for gpu in gpus:
                # print(gpu)
                gpu['id'] = count
                db.save_gpu(gpu)
                count += 1
            print(
                f"---------------  scraped {scraped} from page {page}  ---------------")
            if DEBUG:
                print(" - !!! exit on DEBUG")
                break
        print(f"saved {count} gpus")
    db.collect_brands()
    db.collect_chipsets()
