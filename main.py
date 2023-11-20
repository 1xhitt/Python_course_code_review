import weakref
import requests, bs4
from selenium.webdriver import Chrome

def get_urls(driver) -> list[str]:
    pass

def main():

    with Chrome() as driver:
        driver.implicitly_wait(0.5)
        urls = get_urls(driver)
        
        pass
    pass

if __name__ == "__main__":
    main()
