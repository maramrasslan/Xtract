from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from login import login_facebook
import time
import pandas as pd

def scroll(driver):
    SCROLL_PAUSE_TIME = 2
    page_height = 0
    counter = 0
    max = 20
    while counter<max:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == page_height:
            break
        page_height = new_height
        counter = counter + 1


def searchText(driver, textToSearch):
    all_text = []
    all_link = []
    search_box = driver.find_element(By.XPATH, "//input[@type='search']")
    search_box.clear()
    search_box.send_keys(textToSearch)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)
    print(search_box)
    search_box.clear()

    driver.get(f"https://www.facebook.com/search/posts/?q={textToSearch}")
    scroll(driver)

    posts = driver.find_elements(By.CSS_SELECTOR, "[class='x1n2onr6 x1ja2u2z']")
    for post in posts:
        try:
            txt = post.find_element(By.CSS_SELECTOR, "[class='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a']")
            txt_t = txt.text
            print(txt_t)
        except:
            txt_t = None
        all_text.append(txt_t)
    for link in posts:
        try:
            lnk = link.find_element(By.TAG_NAME, "a")
            lnk_l = lnk.get_attribute('href')
            print(lnk_l)
        except:
            lnk_l = None

        all_link.append(lnk_l)
    
    return all_text, all_link
