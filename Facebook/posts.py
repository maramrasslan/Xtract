from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from login import login_facebook
from datetime import datetime
import csv
import json


def is_within_date_range(date_text, start_date, end_date):
    formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d')
    formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    try:
        if len(date_text.split()) == 4:  # Example: '6 July at 08:45'
            current_year = datetime.now().year
            date_text = date_text.replace('at', f'{current_year} at')
        date_text = datetime.strptime(date_text, '%d %B %Y at %H:%M').date()
        
        # post_date = datetime.strptime(date_text, '%d %B %Y')
        if formatted_start_date.date() <= date_text <= formatted_end_date.date():
            return True
        else:
            return False
    except Exception as e:
        print(f"Error parsing date: {e}")
        return False

def scrape_posts(driver, url, num_posts=100, start_date=None, end_date=None):
    driver.get('https://mbasic.facebook.com')
    basic_url = url.replace("https://www.facebook.com", "https://mbasic.facebook.com")
    driver.get(basic_url + '?v=timeline')

    all_posts = []
    all_dates = []


    print(start_date)
    print(end_date)

    def scrape_current_page():
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        posts = soup.find_all('p')
        dates = soup.find_all('abbr')
        
        for post, date in zip(posts, dates):
            post_text = post.get_text()
            date_text = date.get_text()
            if start_date and end_date:
                if is_within_date_range(date_text, start_date, end_date):
                    all_posts.append(post_text)
                    all_dates.append(date_text)
                else:
                    if len(date_text.split()) == 4:  # Example: '6 July at 08:45'
                        current_year = datetime.now().year
                        date_text = date_text.replace('at', f'{current_year} at')
                    post_date = datetime.strptime(date_text, '%d %B %Y at %H:%M').date()
                    formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                    
                    if post_date < formatted_end_date:
                        print("yes doesn't fit")
                        return False
            else:
                all_posts.append(post_text)
                all_dates.append(date_text)
        return True

    def click_see_more(button_id):
        try:
            see_more_stories = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, button_id)))
            links = see_more_stories.find_elements(By.TAG_NAME, 'a')
            for link in links:
                if link.text == 'See more stories':
                    link.click()
                    return True
        except:
            pass
        return False

    # Initial scrape
    if not scrape_current_page():
        return all_posts, all_dates

    # State machine implementation
    state = 'initial'

    while len(all_posts) < num_posts:
        if state == 'initial':
            if click_see_more('timelineBody'):
                state = 'structured'
            else:
                print("No more 'See more stories' links found in initial state")
                break
        elif state == 'structured':
            if click_see_more('structured_composer_async_container'):
                state = 'structured'
            else:
                print("No more 'See more stories' links found in structured state")
                break
        
        if not scrape_current_page():
            break

    return all_posts, all_dates
