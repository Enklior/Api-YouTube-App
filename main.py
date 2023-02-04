from flask import Flask, jsonify, render_template
import pprint
import requests
from numerize.numerize import numerize


CHANNELS = {
  'cleverprogrammer': 'UCqrILQNl5Ed9Dz6CGMyvMTQ',
  'mrbeast': 'UCX6OQ3DkcsbYNE6H8uQQuVA',
  'mkbhd': 'UCBJycsmduvYEL83R_U4JriQ',
  'pm': 'UC3DkFux8Iv-aYnTRWzwaiBA',
}

ACTIVE_CHANNEL = CHANNELS['cleverprogrammer']

pp = pprint.PrettyPrinter(indent=1)

app = Flask(__name__)

data = {
  'contents': [
    {
      'type': 'video',
      'video': {
        'isLiveNow': False,
        'publishedTimeText': None,
        'stats': {'views': 23000},
        'title': 'Build Medium App with Next.js and Firebase',
        'thumbnails': [
          {'url': 'link.com'}, 
          {'url': 'link.com'},
        ]
      }
    },
    {
      'type': 'video',
      'video': {
        'isLiveNow': False,
        'publishedTimeText': '10 days ago',
        'stats': {'views': 44443},
        'title': 'Build Modern Portfolio with NextJS, TypeScript, SSR, and CMS',
        'thumbnails': [
          {'url': 'link.com'}, 
          {'url': 'link.com'},
        ]
      }
    }
  ],
  
  'cursorNext': 'blah'
}

# pp.pprint(data['content'])

first_video = data['contents'][0]['video']

# print(first_video)
# print(first_video['title'])
# print(first_video['publishedTimeText'])
# print(first_video['thumbnails'])

@app.route('/')
def index():
  url = "https://youtube138.p.rapidapi.com/channel/videos/"
  querystring = {"id": ACTIVE_CHANNEL,"hl":"en","gl":"US"}
  
  headers = {
    "X-RapidAPI-Key": "a159a864b6msh6aa03df6a160f8fp1d00bbjsn13d7847a69bd",
    "X-RapidAPI-Host": "youtube138.p.rapidapi.com"
  }
  
  response = requests.request("GET", url, headers=headers, params=querystring)
  data = response.json()
  contents = data['contents']
  videos = [video['video'] for video in contents if video['video']['publishedTimeText']]
  print(videos)
  video = videos[0]
  return render_template('index.html', videos=videos, video=video)

@app.template_filter()
def numberize(views):
  return numerize(views, 1)

@app.template_filter()
def highest_quality_image(thumbnails):
  return thumbnails[3]['url'] if len(thumbnails) >= 4 else thumbnails[0]['url']
  
app.run(host='0.0.0.0', port=81)