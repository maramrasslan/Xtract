import json
import csv
from bs4 import BeautifulSoup
from login import login_facebook

def extract_section_text(section):
    if section:
        texts = section.stripped_strings
        return list(texts)
    return []

def profile_info(driver, url):
    driver.get('https://mbasic.facebook.com')
    basic_url = url.replace("https://www.facebook.com", "https://mbasic.facebook.com")
    driver.get(basic_url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    profile_data = {}

    sections = {
        "Education": 'education',
        "Work": 'work',
        "Living": 'living',
        "Contact Info": 'contact-info',
        "Basic Info": 'basic-info',
        "Relationship": 'relationship',
        "Bio": 'bio',
        "Events": 'events'
    }

    for section_name, section_id in sections.items():
        try:
            section = soup.find('div', id=section_id)
            section_texts = extract_section_text(section)
            profile_data[section_name] = section_texts
        except:
            pass

    return profile_data
