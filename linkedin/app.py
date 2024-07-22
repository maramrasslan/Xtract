from flask import Flask , jsonify , request
from flask import send_file
from flask_cors import CORS
from middleware import token_required
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime
import time
import pytz
from linkedin_profile import get_profile 
from linkedin_keyword import get_content
from linkedin_cross import find_profile
from util import decode_auth_token
from dotenv import dotenv_values



app = Flask('__name__')
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

Cors = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)

@app.route('/')
# @token_required
def hi():
    return jsonify({'hi':'bye'})

@app.route('/searchLinkedin',methods=['POST'])
# @token_required
def search_linkedin():
    try:
        token = request.headers.get('Authorization').split()[1]
        # print(token)
        # print(decode_auth_token(token))
        if token !="null":
            user_id = decode_auth_token(token)
            print(user_id)
        else: user_id=None
    except: user_id=None
    
    # print(request.json)
    # print(id)
    data = {}
    if request.method == 'POST':
        data['searchMethod'] = request.json['searchMethod']
        data['username'] = request.json['username']
        data['keyword'] = request.json['keyword']
        data['loopLimit'] = request.json['loopLimit']
        data['startDate'] = request.json['startDate']
        data['endDate'] = request.json['endDate']
        data['startTime'] = request.json['startTime']
        data['endTime'] = request.json['endTime']
        data['filters'] = request.json['filters']


        if user_id:
            utc3 = pytz.timezone('Etc/GMT+3')
            now_utc3 = datetime.datetime.now(utc3)
            # Format the datetime
            formatted_date = now_utc3.strftime('%Y-%m-%d %H:%M')
          
            # print(search_history)
      
        
        if 'profile' in data['searchMethod']:
            if (data['filters']['posts']):
                postFilters = {
                'keyword':  data['keyword'],
                'loopLimit': data['loopLimit'],
                'startDate' : data['startDate'],
                'endDate' : data['endDate'],
                'startTime': data['startTime'],
                'endTime' : data['endTime']
            }
            else : postFilters ={}
            start_time = time.time()
            profile , profile_file , posts , posts_file = get_profile(data['username'],data['filters'],postFilters)
            end_time = time.time()
            duration = end_time - start_time

            if user_id:
                search_history = {
                "service": "Linkedin",
                "query": data["username"],
                "date": formatted_date,
                "userId": ObjectId(user_id)
            }
                search = {
                "duration": duration,
                "query": data["username"],
                "createdAt": formatted_date,
                "userId": ObjectId(user_id)
            }
                mongo.db['searchhistories'].insert_one(search_history)
                mongo.db['search'].insert_one(search)

            return jsonify(profile=profile , profilefileName=profile_file,postsfileName=posts_file,posts=posts)
                     
        elif 'keyword' in data['searchMethod']:
            postFilters = {
                'loopLimit': data['loopLimit'],
                'startDate' : data['startDate'],
                'endDate' : data['endDate'],
                'startTime': data['startTime'],
                'endTime' : data['endTime']
            }
            start_time = time.time()
            posts , posts_file = get_content(data['keyword'],postFilters)
            end_time = time.time()
            duration = end_time - start_time

            if user_id:
                search_history = {
                "service": "Linkedin",
                "query": data['keyword'],
                "date": formatted_date,
                "userId": ObjectId(user_id)
            }
                search = {
                "duration": duration,
                "query": data['keyword'],
                "createdAt": formatted_date,
                "userId": ObjectId(user_id)
            }
                mongo.db['searchhistories'].insert_one(search_history)
                mongo.db['search'].insert_one(search)
            return jsonify(postsfileName=posts_file,posts=posts)
            

                
@app.route('/download/<file_name>',methods=['GET'])
def download(file_name):
    format = request.args.get('fileFormat')
    if format =='csv':
        file_path = f"./download/{file_name}.csv"    
        return send_file(file_path,download_name=file_name,as_attachment=True)
    elif format =='json':    
        file_path = f"./download/{file_name}.json"
        return send_file(file_path,download_name=file_name,as_attachment=True)
    
    return jsonify('Not found 404')


@app.route('/findProfile',methods=['POST'])
# @token_required
def search():
    name = request.json['profileName']
    try:
        
        token = request.headers.get('Authorization').split()[1]
        if token !="null":
            user_id = decode_auth_token(token)
        else:user_id=None
    except: user_id=None
      

    start_time = time.time()
    profiles = find_profile(name)
    end_time = time.time()
    duration = end_time - start_time
    if user_id:
        utc3 = pytz.timezone('Etc/GMT+3')
        now_utc3 = datetime.datetime.now(utc3)
        # Format the datetime
        formatted_date = now_utc3.strftime('%Y-%m-%d %H:%M')
        search_history = {
            "service": "Linkedin",
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
    # print(profiles)
    return jsonify (profiles = profiles)


# 
if __name__ == '__main__':
    app.run(port=5000,debug=True)