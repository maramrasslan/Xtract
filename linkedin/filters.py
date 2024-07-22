import pandas as pd
import pythonmonkey as pm
import json
from datetime import datetime


# timestamp extractor 
# originally written in js , used pythonmonkey library to convert the code
# we cant extract the date directly , we need the post id in "data-chameleon-result-urn="urn:li:activity:postid""
# the function returns the date like that "Fri, 12 Apr 2024 18:05:07 GMT"
js_function = """(postId) => {
    const asBinary = postId.toString(2);
    const first41Chars = asBinary.slice(0, 41);
    const timestamp = parseInt(first41Chars, 2);
    const dateObject = new Date(timestamp);
    const humanDateFormat = dateObject.toUTCString();
    return humanDateFormat; 
    } """ 

date = pm.eval(js_function)(pm.bigint(7184612518198190080))
# print(date)



# Filters functions 
# Read the CSV file into a DataFrame
# df = pd.read_csv('satyanadella.csv')
df = pd.read_csv('williamhgates-with-see-more-show-more.csv')

# Access data in the DataFrame using column names or indexing
# posts = df['Content']
dates, posts = df['date'],df['content']
# print(posts)


def filter_by_keyword(keyword,posts):
    filtered_posts = list(filter(lambda k : keyword in k , posts))
    return filtered_posts

def filter_by_date(before,after,dates,posts):
    filtered_dates , filtered_posts = [] , []
    for date, post in zip(dates,posts):
        new_date = date.split()
        new_date = new_date[1] +' ' + new_date [2] + ' '+ new_date[3]
        new_date = str(datetime.strptime(new_date, "%d %b %Y").strftime("%d/%m/%Y")).split(" ")[0]
        # print(new_date)
        # before = datetime.date()
        if new_date < before and new_date > after:
            filtered_dates.append(date)
            filtered_posts.append(post)
           
        
    return filtered_dates , filtered_posts

   

# testing the filter by keyword function
# with open("filter-keyword.txt","w") as f:
#     filtered_posts = filter_by_keyword("invite",posts)
#     for post in filtered_posts:
#         f.write(post)
#         f.write("\n")



filtered_dates , filtered_posts = filter_by_date("18/06/2024","13/06/2024",dates,posts)
data = {
    "date": filtered_dates,
    "Content": filtered_posts,
}
df = pd.DataFrame(data)
df.to_csv("filter-date.csv", encoding='utf-8',index=False)

    





