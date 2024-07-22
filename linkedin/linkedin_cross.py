from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json


def find_profile(name):
    options = Options()
    # options.add_experimental_option("detach", True)
    # options.add_argument("--headless=new")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(options=options)
    # # Open Google.com
    driver.get("https://www.google.com")
    change_language = driver.find_element(By.PARTIAL_LINK_TEXT,"English")
    change_language.click()

    # time.sleep(3)


    WebDriverWait(driver,5).until(
        EC.presence_of_element_located((By.CLASS_NAME,"gLFyf"))
    )
    get_linkedin = driver.find_element(By.CLASS_NAME , "gLFyf")
    get_linkedin.clear()
    get_linkedin.send_keys("linkedin" + Keys.ENTER)

    
    open_linkedin = driver.find_element(By.PARTIAL_LINK_TEXT,"linkedin")
    open_linkedin.click()

   
    linkedin_credentials = json.load(open("credentials.json"))
    index = random.randint(0,1)
    email = linkedin_credentials['email'][index]
    password = linkedin_credentials['password'][0]

    # sign_in = driver.find_element(By.PARTIAL_LINK_TEXT,"signin")
    # sign_in.click()
    # finding input boxes and entering crednetials
    driver.switch_to.new_window('tab')
    driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    input_email = driver.find_element(By.CSS_SELECTOR,'input#username')
    input_password= driver.find_element(By.CSS_SELECTOR,'input#password')
    for i in email:
        input_email.send_keys(i)
        time.sleep(random.randint(0,1))

    for i in password:
        input_password.send_keys(i)
        time.sleep(random.randint(0,1))


    input_password.send_keys(Keys.ENTER)

    # time.sleep(30)

    # time.sleep(50)


    url = f"https://www.linkedin.com/search/results/all/?keywords={name}"
    driver.get(url)

    max_results = 20
    profiles = []



    try:
        WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"div#search-reusables__filters-bar"))
        )

        bar = driver.find_element(By.CSS_SELECTOR,"div#search-reusables__filters-bar")

        buttons = bar.find_elements(By.CSS_SELECTOR,"button")
        right_button = False
        for button in buttons:
            try: 
                if "People" in button.text:
                    right_button = button
                    right_button.click()
                    break        
            except:
                pass

        time.sleep(1)
        while True:
            WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"div.mb2"))
            )
            list = driver.find_element(By.CSS_SELECTOR,"div.mb2")

            profile_list = list.find_elements(By.CSS_SELECTOR,"li")

            for profile in profile_list:
                try:
                    profile_pic=profile.find_element(By.CSS_SELECTOR,'img').get_attribute('src')
                except: profile_pic=None
                try:
                    profile_name= profile.find_element(By.CSS_SELECTOR,'span[dir="ltr"]').find_element(By.CSS_SELECTOR,'span').text
                except: profile_name=""
                try:
                    profile_url= profile.find_element(By.CSS_SELECTOR,'a').get_attribute('href')
                except: profile_url=''


                if not(any(profile['ProfileLink'] == profile_url for profile in profiles)):
                    profiles.append({
                        'ProfileImg':profile_pic,
                        'ProfileName':profile_name,
                        'ProfileLink':profile_url
                    })

            print(profiles)
            if (len(profiles) >= max_results):
                break
            
           
            try:
                driver.execute_script("window.scrollBy(0,300);")
                WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'button[aria-label="Next"]'))
                )
                next = driver.find_element(By.CSS_SELECTOR,'button[aria-label="Next"]')
                next.click()
            except: print("error")

            time.sleep(2)
    except:pass

    return profiles
