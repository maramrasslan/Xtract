from selenium.webdriver.common.by import By
import time
import json
from login import login_facebook
import pandas as pd

# function to get user photo
def user_photos(driver, url): 
    all_photos = []
    driver.get(url)
    for i in ["photos_of" , "photos_by"]:
        driver.get(url +"/"+ i)
        time.sleep(25)
        SCROLL_PAUSE_TIME = 5
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        anchors = driver.find_elements(By.CSS_SELECTOR, "[class='x9f619 x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1n2onr6']")
        time.sleep(5) 
        for img in anchors:
            try:
                user_images = img.find_element(By.TAG_NAME, "img")
                image_link = user_images.get_attribute('src')
            except:
                pass
            all_photos.append(image_link)
        
    for photo in all_photos:
        print(f"photo link: {photo}\n")

    return all_photos
