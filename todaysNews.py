from flask import Flask, redirect, render_template, url_for, request
from configparser import ConfigParser
import requests
import json

country = ""
result = ""
source = []
title = []
description = []
url = []
urlImg = []
article_length = 0
resultant_array = []
result_status = ""
myResult = []

myConfig = ConfigParser()
myConfig.read('../config/creds.cfg')
API_KEY = myConfig.get("newsapi", "api_key")

API_URL = ("https://newsapi.org/v2/top-headlines?country={}&apiKey={}")


app = Flask(__name__)

def query_api(country):
    try:
        data = requests.get(API_URL.format(country, API_KEY)).json()
    except Exception as exec:
        print(exec)
        data = None
    return data

def process_result(result):
    #Loading the result data as json
    try:
        myCont = json.loads(json.dumps(result))
        result_status = myCont.get("status")
        #checking whether the api result status is 'ok'
        if result_status == "ok":
            article_length = len(myCont["articles"])
            for i in range(article_length):
                if ((myCont.get("articles")[i].get("source").get("name") != '') and (myCont.get("articles")[i].get("source").get("name") != None)):
                    source.append(myCont.get("articles")[i].get("source").get("name"))
                else:
                    source.append('Not available')

                if ((myCont.get("articles")[i].get("title") != '') and (myCont.get("articles")[i].get("title") != None)):
                    title.append(myCont.get("articles")[i].get("title"))
                else:
                    title.append('Not available')

                if ((myCont.get("articles")[i].get("description") != '') and (myCont.get("articles")[i].get("description") != None)):             
                    description.append(myCont.get("articles")[i].get("description"))
                else:
                    description.append('Not available')

                if ((myCont.get("articles")[i].get("url") != '') and (myCont.get("articles")[i].get("url") != None)):
                    url.append(myCont.get("articles")[i].get("url"))
                else:
                    url.append('Not available')

                if ((myCont.get("articles")[i].get("urlToImage") != '') and (myCont.get("articles")[i].get("urlToImage") != None)):                
                    urlImg.append(myCont.get("articles")[i].get("urlToImage"))
                else:
                    urlImg.append('Not available')
            resultant_array.extend([source,title,description,url,urlImg])
    except Exception as exec:
        print(exec)
    return {'myStat': result_status, 'myArtCount':article_length, 'myRes':resultant_array} 

#Defining home page
@app.route("/")
def home():
    return render_template("getNews.html")

@app.route("/getNews", methods=["POST","GET"])
def getNews():
    if request.method == "POST":
        country = request.form["country"]
        if country != '(select)':
            data = query_api(country)
            try:
                myResult = process_result(data)
            except:
                status = "Error not found"
            return render_template("result.html", status = myResult["myStat"], articleLength = myResult["myArtCount"], res = myResult["myRes"])
    else:
        return render_template("getNews.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)