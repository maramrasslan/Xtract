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
# ---------------------------------------------------------------------

# options = Options()
# options.add_experimental_option("detach", True)
# service = Service(executable_path="chromedriver.exe")
# driver = webdriver.Chrome()
# # # Open Google.com
# driver.get("https://www.google.com")
# change_language = driver.find_element(By.PARTIAL_LINK_TEXT,"English")
# change_language.click()


# WebDriverWait(driver,5).until(
#     EC.presence_of_element_located((By.CLASS_NAME,"gLFyf"))
# )
# get_linkedin = driver.find_element(By.CLASS_NAME , "gLFyf")
# get_linkedin.clear()
# get_linkedin.send_keys("linkedin" + Keys.ENTER)

# open_linkedin = driver.find_element(By.PARTIAL_LINK_TEXT,"linkedin")
# open_linkedin.click()

# signing in
# loading credentials 
# linkedin_credentials = json.load(open("credentials.json"))
# index = random.randint(0,2)
# email = linkedin_credentials['email'][index]
# password = linkedin_credentials['password'][0]

# # finding input boxes and entering crednetials
# input_email = driver.find_element(By.XPATH,'//*[@id="session_key"]')
# input_password= driver.find_element(By.XPATH,'//*[@id="session_password"]')
# for i in email:
#     input_email.send_keys(i)
#     time.sleep(random.randint(0,4))

# for i in password:
#     input_password.send_keys(i)
#     time.sleep(random.randint(0,4))


# driver.send_keys(Keys.ENTER)
# time.sleep(50)

# visiting the profile we want
# username = "williamhgates"
# username = "satyanadella"
username = "reidhoffman"
# username = "legalheadhunter"


# -----------------------------------------------------------------------------------------
# the filters array , based on it we choose whether to output the data or not 
filters = {
    'name':True,
    'subtitle':True,
    'about':True,
    'experience':True,
    'education':True,
    'posts':True
}
#TODO implement get_filters function
#--------------------------------------------------------------------
#profile data(besides posts):
def get_profile(username, filters, postFilters):
    data = {}
    posts ={}
    # ---------------------------------------------------------------------------------
    options = Options()
    # options.add_experimental_option("detach", True)
    # options.add_argument("--headless")
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


    profile_url = f"https://www.linkedin.com/in/{username}"
    driver.get(profile_url)
    time.sleep(2)
    if (filters['name']):
        try:
            name = driver.find_element(By.CSS_SELECTOR,'h1')
            name = name.text
            data['name'] = name
            # print(name)
        except: data['name'] = ''
    
    if (filters['subtitle']):
        try:
            subtitle = driver.find_element(By.CSS_SELECTOR,'div.text-body-medium')
            subtitle = subtitle.text
            data['subtitle'] = subtitle
            # print(subtitle)
        except: data['subtitle']=''

    if(filters['about']):
        try:
            WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"div.ph5.pv3"))
    )
            about = driver.find_element(By.CSS_SELECTOR,"div.ph5.pv3")
            about_text = about.find_elements(By.CSS_SELECTOR,'span')[0].text
            data['about'] = about_text
            # print(about)
        except: data['about'] = ''


    WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"section"))
    )
    sections= driver.find_elements(By.CSS_SELECTOR,"section")

    if(filters['experience']):
        data['experience'] = ''
        try:
            experience_section=[]
            experience = False
            for section in sections:
                try: 
                    experience = section.find_element(By.CSS_SELECTOR,'div#experience')
                    if(experience):
                        experience = section
                        break
                except:
                    pass
            if (experience):
                experience_link = False
                try:
                    experience_link = experience.find_element(By.CSS_SELECTOR,'a#navigation-index-see-all-experiences').get_attribute('href')
                    # print(experience_link)
                except: pass

                if experience_link:
                    experience_link = f"https://www.linkedin.com/in/{username}/details/experience/"
                    driver.switch_to.new_window('tab')
                    driver.get(experience_link)
                    WebDriverWait(driver,20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,"div.pvs-list__container"))
                    )
                    time.sleep(3)
                    try:
                        
                        start = time.time()
                        experience_list = driver.find_element(By.CSS_SELECTOR,'div.pvs-list__container').find_elements(By.CSS_SELECTOR,'li')
                        # print(experience_list)
                        for item in experience_list:
                            try:
                                info = item.find_element(By.CSS_SELECTOR,'span.t-14').find_element(By.CSS_SELECTOR,'span').text

                                if info not in experience_section:
                                    experience_section.append(info)
                                
                                if len(experience_section) > 15 : break
                            except: pass
                            # time.sleep(2)
                            # print(experience_section)
                        end = time.time()
                        # time.sleep(5)
                            # driver.execute_script("window.scrollBy(0,350);")
                        
                            # if round(end-start)>40:
                            #     break
                           

                        driver.switch_to.new_window('tab')
                        driver.get(profile_url)
                        time.sleep(2)
                            
                    except: 
                        print("error")
                        driver.switch_to.new_window('tab')
                        driver.get(profile_url)

                else:
                    experience_list = experience.find_elements(By.CSS_SELECTOR,'li')
                    for item in experience_list:
                        try:
                            info = item.find_element(By.CSS_SELECTOR,'span.t-14').find_element(By.CSS_SELECTOR,'span').text
                       
                            if info not in experience_section:
                                experience_section.append(info)
                        except:pass

                data['experience'] = experience_section
            else: data['experience'] = ''
        except: data['experience'] = ''


    if(filters['education']):
        time.sleep(3)
        data['education'] = ''
        sections= driver.find_elements(By.CSS_SELECTOR,"section")
        # print(sections)
        try:
            education_section=[]
            education = False
            for section in sections:
                try: 
                    education = section.find_element(By.CSS_SELECTOR,'div#education')
                    if (education):
                        education = section
                        break
                except:
                    pass
            
            if (education):
              
                education_link = False
                try:
                    education_link = education.find_element(By.CSS_SELECTOR,'a#navigation-index-see-all-education').get_attribute('href')
                    # print(education_link)
                except:pass

                if  education_link:
                    education_link = f"https://www.linkedin.com/in/{username}/details/education/"
                    driver.switch_to.new_window('tab')
                    driver.get(education_link)
                    WebDriverWait(driver,20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,"div.pvs-list__container"))
                    )
                    education_list = driver.find_element(By.CSS_SELECTOR,'div.pvs-list__container').find_elements(By.CSS_SELECTOR,'li')
                    for item in education_list:
                        try:
                            info = item.find_elements(By.CSS_SELECTOR,'span')[0].text
                            if info not in education_section:
                                education_section.append(info)
                            
                            if len(education_section) > 10 : break 
                        except: pass
                    driver.switch_to.new_window('tab')
                    driver.get(profile_url)
                else:
                    # print("hi")
                    education_list = education.find_elements(By.CSS_SELECTOR,'li')
                    for item in education_list:
                        info = item.find_elements(By.CSS_SELECTOR,'span')[0].text
                        if info not in education_section:
                            education_section.append(info)

                data['education'] = education_section
            else: data['education'] = ''
        except: data['education'] = ''


    if (filters['posts']):
        post_url = f"https://www.linkedin.com/in/{username}/recent-activity/all/"

        if postFilters:
            noPosts = postFilters['loopLimit']
            keyword = postFilters['keyword']
            startDate = postFilters['startDate']
            endDate = postFilters['endDate']
            startTime = postFilters['startTime']
            endTime = postFilters['endTime']

            js_function = """(postId) => {
                const asBinary = postId.toString(2);
                const first41Chars = asBinary.slice(0, 41);
                const timestamp = parseInt(first41Chars, 2);
                const dateObject = new Date(timestamp);
                const humanDateFormat = dateObject.toUTCString();
                return humanDateFormat; 
                } """ 
            time.sleep(2)
            driver.switch_to.new_window('tab')
            driver.get(post_url)

        
            unfiltered = {}
            while True:
                start = time.time()
                WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,"[data-urn*='urn:li:activity:']"))
                )
                dates = driver.find_elements(By.CSS_SELECTOR,"[data-urn*='urn:li:activity:']")

                for date in dates:
                    WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'div.mr2'))
                )
                    try:
                        post = date.find_element(By.CSS_SELECTOR,'div.mr2')
                        try:
                            see_more_button = post.find_elements(By.CSS_SELECTOR,'[role="button"]')[0]
                            if see_more_button:
                                time.sleep(2)
                                see_more_button.click()
                                
                        except:
                            # print("no see more")
                            pass
                    except: pass

                    
                    date = date.get_attribute('data-urn').split(':')[3]
                    time.sleep(2)
                    date = pm.eval(js_function)(pm.bigint(date))

                    # if date not in unfiltered :
                    #     unfiltered[date]= post.text
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

                # print(len(posts))
               

         
            
                # if (len(unfiltered)>=10 and len(unfiltered)<=20):
                #     try:
                #         show_more_posts = driver.find_element(By.CSS_SELECTOR,'div.p5').find_element(By.CSS_SELECTOR,'button')
                #         time.sleep(5)
                #         show_more_posts.click()
                #     except:
                # # print('no more posts')
                #         pass



                if(len(posts)>=noPosts):
                    break           
                time.sleep(2)
                driver.execute_script("window.scrollBy(0,150);")


                end = time.time()

                # timeout 
                if (round(end-start) > 600):
                    break

                # time.sleep(5)
                # print("posts",posts)
                # print("-----------------------------------------------------")
                # print("unfiltered",unfiltered)
                

    driver.quit()

    if posts:
        if len(posts) > noPosts:
            posts_list = [ [k,v] for k, v in posts.items() ]
            posts_list = posts_list[:noPosts]
            posts= dict(posts_list)
# print(data)
    with open(f'./download/{username}-profile-info.csv','w',encoding='utf-8') as csv_file: 
        writer = csv.writer(csv_file)
        # writer.writerow(['name','subtitle','about','experience','education'])
        for key , value in data.items():
            writer.writerow([key,value])

    with open(f"./download/{username}-profile-info.json",'w',encoding='utf-8') as json_file:
        json_data = json.dumps(data)
        json_file.write(json_data)

    
    with open(f'./download/{username}-posts.csv','w',encoding='utf-8') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(["date","content"])
        for key, value in posts.items():
            writer.writerow([key, value])

    with open(f"./download/{username}-posts.json",'w',encoding='utf-8') as json_file:
        json_data = json.dumps(posts)
        json_file.write(json_data)


    if posts:
        posts=[]
        with open(f"./download/{username}-posts.csv", mode='r',encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file) 
            line_count = 0
            for row in csv_reader:
                posts.append(row)  


    return data , f'{username}-profile-info' , posts , f'{username}-posts'

    
# get_profile(username, filters)



# --------------------------------------------------------------------------------------------



   
   
    
        



# # -------------------------------------------------------------------------------------------
# # writing the scraped posts to a csv file
# # data = {
# #     "Name": username,
# #     "Content": post_texts,
# # }
# # df = pd.DataFrame(data)
# # df.to_csv(f"{username}-posts.csv", encoding='utf-8', index=False)

# with open(f'{username}-posts.csv','w',encoding='utf-8') as csv_file:  
#     writer = csv.writer(csv_file)
#     writer.writerow("date,content")
#     for key, value in date_post.items():
#        writer.writerow([key, value])
# driver.quit()

# # while loop so the chromedriver doesn't close immediately after launching
# # TODO: find another solution for this problem
# # while True:
# #     pass


   