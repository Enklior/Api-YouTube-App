from flask import Flask, jsonify, render_template
from numerize.numerize import numerize
import requests
import pprint

pp = pprint.PrettyPrinter(indent=2)

app = Flask(__name__)

@app.route('/')
def index():
  url = "https://youtube138.p.rapidapi.com/channel/videos/"
  querystring = {"id":"UCqrILQNl5Ed9Dz6CGMyvMTQ", 
                 "filter":"uploads_latest", 
                 "hl":"en", "gl":"US"}
  headers = {
  	"X-RapidAPI-Key": "d72c98894cmsh28b3af34c5863e1p19f360jsne4b9c3aa39ec",
  	"X-RapidAPI-Host": "youtube138.p.rapidapi.com"
  }
  
  response = requests.get(url, headers=headers, params=querystring)
  data = response.json()
  contents = data['contents']
  
  # print(type(response.text))
  # print(type(data))
  # pp.pprint(contents)
  videos = [video['video'] for video in contents if video['video']['publishedTimeText']]
  
  print(videos[0])
  
  return render_template('index.html', 
                        videos=videos)

@app.template_filter()
def numberize(views):
  return numerize(views, 1)

@app.template_filter()
def highest_quality_image(images):
  return images[3]['url'] if len(images) >= 4 else images[0]['url']
  
app.run(host='0.0.0.0', port=81)