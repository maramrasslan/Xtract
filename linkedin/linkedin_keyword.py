from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import pythonmonkey as pm
import csv
import json
import random


def get_content(keyword,filters):
    url = f"https://www.linkedin.com/search/results/all/?keywords={keyword}"

    options = Options()
    # options.add_experimental_option("detach", True)
    # options.add_argument('--headless')
 
  
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(options=options)
    # # Open Google.com
    driver.get("https://www.google.com")
    change_language = driver.find_element(By.PARTIAL_LINK_TEXT,"English")
    change_language.click()


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



    driver.get(url)

    try:
        WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"div#search-reusables__filters-bar"))
        )

        bar = driver.find_element(By.CSS_SELECTOR,"div#search-reusables__filters-bar")

        buttons = bar.find_elements(By.CSS_SELECTOR,"button")
        right_button = False
        for button in buttons:
            try: 
                if "Posts" in button.text:
                    right_button = button
                    right_button.click()
                    break        
            except:
                pass

        time.sleep(1)

        posts={}
        unfiltered={}
        noPosts = filters['loopLimit']
        if filters:
            
            startDate = filters['startDate']
            endDate = filters['endDate']
            startTime = filters['startTime']
            endTime = filters['endTime']

        js_function = """(postId) => {
            const asBinary = postId.toString(2);
            const first41Chars = asBinary.slice(0, 41);
            const timestamp = parseInt(first41Chars, 2);
            const dateObject = new Date(timestamp);
            const humanDateFormat = dateObject.toUTCString();
            return humanDateFormat; 
            } """

        while True:
            start = time.time()
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"[data-urn*='urn:li:activity:']"))
            )
            dates = driver.find_elements(By.CSS_SELECTOR,"[data-urn*='urn:li:activity:']")

            for date in dates:
                if(len(posts)>=noPosts):
                    break      
                WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'div.mr2'))
            )
                post = date.find_element(By.CSS_SELECTOR,'div.mr2')
                try:
                    see_more_button = post.find_elements(By.CSS_SELECTOR,'[role="button"]')[0]
                    if see_more_button:
                        time.sleep(1)
                        see_more_button.click()
                        
                except:
                    # print("no see more")
                    pass

                
                date = date.get_attribute('data-urn').split(':')[3]
                time.sleep(1)
                date = pm.eval(js_function)(pm.bigint(date))

                if date not in unfiltered :
                    unfiltered[date]= post.text
                if keyword:
                    if keyword.lower() in post.text or keyword.upper() in post.text or keyword.capitalize() in post.text: 
                        post_text=post.text
                    else: post_text=''
                else:
                    post_text=post.text

                if startDate and endDate:
                    new_date = date.split()
                    new_date = new_date[1] +' ' + new_date [2] + ' '+ new_date[3]
                    new_date = str(datetime.strptime(new_date, "%d %b %Y").strftime("%Y-%m-%d")).split(" ")[0]
                    if new_date > startDate and new_date < endDate: pass
                    else: date=''
                
                post_text = post.text
                if post_text and date and date not in posts:
                    posts[date] = post_text
        
            print(len(posts))
            if(len(posts)>=noPosts):
                break      

            time.sleep(1)
            driver.execute_script("window.scrollBy(0,150);")


            end = time.time()

            # timeout 
            # if (round(end-start) > 600):
            #     break

            # time.sleep(5)
            # print("posts",posts)
            print("-----------------------------------------------------")
            # print("unfiltered",unfiltered)
            
    except:pass

    driver.quit()

    if len(posts) > noPosts:
        posts_list = [ [k,v] for k, v in posts.items() ]
        posts_list = posts_list[:noPosts]
        posts= dict(posts_list)

    with open(f'./download/{keyword}.csv','w',encoding='utf-8') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(["date","content"])
        for key, value in posts.items():
            writer.writerow([key, value])

    with open(f"./download/{keyword}.json",'w',encoding='utf-8') as json_file:
        json_data = json.dumps(posts)
        json_file.write(json_data)


    if posts:
        posts=[]
        with open(f"./download/{keyword}.csv", mode='r',encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file) 
            for row in csv_reader:
                posts.append(row)  


    return posts , f'{keyword}'


    
    
