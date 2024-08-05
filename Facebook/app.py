from flask import Flask, request, jsonify, send_file
from information import profile_info
from posts import scrape_posts
from userPhotos import user_photos
from searchKeyword import searchText
import json
import csv
import os
from login import login_facebook
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime
import time
import pytz
from middleware import token_required
from util import decode_auth_token
from search import search_by_name
from dotenv import dotenv_values



app = Flask(__name__) 
Cors = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)

env_vars = dotenv_values(".env")
app.config["MONGO_URI"] = env_vars.get("DATABASE_URL")
# Initialize PyMongo
mongo = PyMongo(app)

# Create the SearchHistory schema
search_history_schema = {
    "service": str,
    "query": str,
    "date": datetime.datetime,
    "userId": ObjectId
}
# Create the Search schema
search_schema = {
    "duration": float,
    "query": str,
    "date": datetime.datetime,
    "userId": ObjectId
}



def save_to_csv_keyword(results, file_name):
    with open(f"{file_name}_keywords.csv", 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Text', 'Link'])
        for keyword_data in results.get('keywords', []):
            writer.writerow([keyword_data['text'], keyword_data['link']])
        writer.writerow([])  # Empty row for separation

def save_to_csv(results, file_name):
    with open(f"{file_name}.csv", 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        for section, data in results.items():
            writer.writerow([section])
            if section == 'information':
                writer.writerow(['Section', 'Information'])
                for info_section, info_data in data.items():
                    writer.writerow([info_section, ', '.join(info_data)])
            elif section == 'posts':
                writer.writerow(['Date', 'Post'])
                for post_data in data:
                    writer.writerow([post_data['date'], post_data['post']])
            elif section == 'photos':
                writer.writerow(['Photo URL'])
                for photo in data:
                    writer.writerow([photo])
            writer.writerow([])  # Empty row for separation

@app.route("/",methods=['GET'])
def hi():
    return jsonify({"hi":"from facebook"})

@app.route('/search/profile', methods=['POST'])
# @token_required
def search_profile():
    try:
        
        token = request.headers.get('Authorization').split()[1]
        if token !="null":
            user_id = decode_auth_token(token)
        else: user_id=None
    except: user_id=None
    
    try:
        data = request.json
        # print(data)
        search_type = data['searchMethod']
        # print(search_type)
        url = data['profileLink']
        # print(url)
        username = url.split("/")[-1]
        # print(username)
        include_information = data['includeInformation']
        include_photos = data['includePhotos']
        include_posts = data['includePosts']
        # info_types = data['info_types']
        start_date = data['startDate']
        print(F"start_date: {start_date}")
        end_date = data['endDate']
        num_posts = data['numPosts']
        file_format = 'csv'
        file_name = "results"
        keyword = data['keyword']


        if user_id:
            utc3 = pytz.timezone('Etc/GMT+3')
            now_utc3 = datetime.datetime.now(utc3)
            # Format the datetime
            formatted_date = now_utc3.strftime('%Y-%m-%d %H:%M')

            search_history = {
                "service": "Facebook",
                "query": username or data['keyword'],
                "date": formatted_date,
                "userId": ObjectId(user_id)
            }


        results = {}
        start = time.time()
        driver = login_facebook()
        if search_type == 'profile':

            if include_information:
                profile_data = profile_info(driver, url)
                results['information'] = profile_data

            if include_posts:
                posts, dates = scrape_posts(driver, url, num_posts, start_date, end_date)
                results['posts'] = [{'date': date, 'post': post} for date, post in zip(dates, posts)]  # Organize as date: post pairs

            if include_photos:
                photos = user_photos(driver, url)
                results['photos'] = photos

            if file_format == 'csv':
                save_to_csv(results, file_name)
            else:
                with open(f"{file_name}.json", 'w', encoding='utf-8') as jsonfile:
                    json.dump(results, jsonfile, indent=4, ensure_ascii=False)
        elif search_type == 'keyword':
            texts, links = searchText(driver, keyword)
            if file_format == 'csv':
                results['keywords'] = [{'text': text, 'link': link} for text, link in zip(texts, links)]
                save_to_csv_keyword(results, file_name)
            
            else:
                with open(f"{file_name}.json", 'w', encoding='utf-8') as jsonfile:
                    json.dump(results, jsonfile, indent=4, ensure_ascii=False)

        end = time.time()
        duration = round(end-start)
        if user_id:
            search = {
                "duration": duration,
                "query": username or data['keyword'],
                "createdAt": formatted_date,
                "userId": ObjectId(user_id)
            }


            mongo.db['searchhistories'].insert_one(search_history)
            mongo.db['search'].insert_one(search)

    except:pass
    return jsonify(results=results,fileName = file_name)

@app.route('/download/<file_name>')
def download_file(file_name):
    csv_file_path = f"./{file_name}.csv"
    csv_keywords_file_path = f"./{file_name}_keywords.csv"
    json_file_path = f"./{file_name}.json"
    
    if os.path.exists(csv_file_path):
        return send_file(csv_file_path,download_name=file_name, as_attachment=True)
    elif os.path.exists(csv_keywords_file_path):
        return send_file(csv_keywords_file_path,download_name=file_name, as_attachment=True)
    elif os.path.exists(json_file_path):
        return send_file(json_file_path, download_name=file_name, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404


@app.route('/findFBProfile',methods=['POST'])
# @token_required
def search():
    driver = login_facebook()
    name = request.json['profileName']

    try:
        token = request.headers.get('Authorization').split()[1]
        if token !="null":
            user_id = decode_auth_token(token)
            print(user_id)
        else: user_id=None
    except: user_id=None
      
    
    start_time = time.time()
    profiles = search_by_name(driver, name)
    end_time = time.time()
    duration = end_time - start_time


    if user_id:
        utc3 = pytz.timezone('Etc/GMT+3')
        now_utc3 = datetime.datetime.now(utc3)
        # Format the datetime
        formatted_date = now_utc3.strftime('%Y-%m-%d %H:%M')
        search_history = {
            "service": "Facebook",
            "query": name,
            "date": formatted_date,
            "userId": ObjectId(user_id)
        }   
        search = {
                "duration": duration,
                "query": name,
                "createdAt": formatted_date,
                "userId": ObjectId(user_id)
        }
        mongo.db['searchhistories'].insert_one(search_history)
        mongo.db['search'].insert_one(search)
    return jsonify (profiles = profiles)


if __name__ == '__main__':
    app.run(port=4000,debug=True)
