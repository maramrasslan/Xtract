from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from config import Config
import time
import json
import pandas as pd

def search_by_name(driver, nameToSearch):
    #search by name 
    search_box = driver.find_element(By.XPATH, "//input[@type='search']")
    search_box.clear()
    search_box.send_keys(nameToSearch)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)
    print(search_box)
    search_box.clear()


    #see all 
    see_all = driver.find_element(By.CSS_SELECTOR, "[aria-label='See all']")
    if see_all:
        see_all.click()

    #scroll down with users name and password

    SCROLL_PAUSE_TIME = 2
    page_height = 0
    Max = 5  # define the maximum number of iterations
    counter = 0
    while True:

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == page_height:
            break
        page_height = new_height
        counter += 1  # increment the counter
        if counter >= Max:  # check if the counter has reached the maximum
            break

    #user profile and image and description
    all_photos = []
    all_links = []
    profiles = []
    max = 10
    searchResults = driver.find_elements(By.CSS_SELECTOR, "[class='x1yztbdb']")
    for img in searchResults:
        try:
            users_profilePhoto = img.find_element(By.TAG_NAME, "image")
            profilePhoto_link = users_profilePhoto.get_attribute('xlink:href')
        except:
            profilePhoto_link = None
        all_photos.append(profilePhoto_link)
        

    for link in searchResults:
        try:
            users_profileLink = link.find_element(By.CSS_SELECTOR, "[aria-hidden='true']")
            profile_link = users_profileLink.get_attribute('href')
        except:
            profile_link = None
        all_links.append(profile_link)
       
    for photo, link in zip(all_photos, all_links):
        profiles.append({
            'ProfilePhoto':photo,
            'ProfileLink':link
        })
    return profiles

