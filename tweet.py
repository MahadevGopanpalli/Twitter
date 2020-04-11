
import tweepy 
import requests
import json
from requests_oauthlib import OAuth1
import sys
import time
import os

consumer_key ="BBVMXjeHsirPwWOsok4HSblqu"
consumer_secret ="vxbThUs9f7A44kp8vD3gX1G2abt9oh80t6OpM0yo4fdXlRgYc3"
access_token ="2836086368-bARBjONNDGqilVYDNpcGfY9rJRn0oa5DmRdvgW4"
access_token_secret ="hAb2CkpkWzneYramANV7YIMShA52bW8rUzf8iIkWuQFEA"
  

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth) 
  
#api.update_status(status="Hello Everyone !")

tweet ="THis post is done by Python"
image_path ="m.png"
video="m.mp4"
#status = api.update_with_media(image_path, tweet)  

auth = OAuth1(consumer_key,
  client_secret=consumer_secret,
  resource_owner_key=access_token,
  resource_owner_secret=access_token_secret)

total_bytes = os.path.getsize(video)
request_data = {
      'command': 'INIT',
      'media_type': 'video/mp4',
      'total_bytes': total_bytes,
      'media_category': 'tweet_video'
    }


req = requests.post('https://upload.twitter.com/1.1/media/upload.json', data=request_data, auth=auth)
media_id = req.json()['media_id']

print('Media ID: %s' % str(media_id))

s = 0
file = open(video, 'rb')
bytes_sent=0
while bytes_sent < total_bytes:
    chunk=file.read(4096)
    request_data = {
            'command': 'APPEND',
            'media_id': media_id,
            'segment_index': s
        }
        

    files = {
            'media':chunk
        }
    req = requests.post('https://upload.twitter.com/1.1/media/upload.json', data=request_data, files=files, auth=auth)

    s=s+1        
    print(req.status_code)
    print (req.text)
    bytes_sent = file.tell()

    print ('%s of %s bytes uploaded' % (str(bytes_sent), str(total_bytes)))
print ("Done...")

request_data = {
      'command': 'FINALIZE',
      'media_id': media_id
    }

req = requests.post('https://upload.twitter.com/1.1/media/upload.json', data=request_data, auth=auth)
print(req.json())

processing_info = req.json().get('processing_info', None)
    

if processing_info is None:
    print ("Not Processed")
    sys.exit(0)

state = processing_info['state']

print('Media processing status is %s ' % state)

if state == u'succeeded':
    print ("Successfully Uploaded")
    sys.exit(0)

if state == u'failed':
    sys.exit(0)

check = processing_info['check_after_secs']
    
print('Checking after %s seconds' % str(check))
time.sleep(check)

print('-------STATUS-------')

request_params = {
      'command': 'STATUS',
      'media_id': media_id
    }

req = requests.get('https://upload.twitter.com/1.1/media/upload.json', params=request_params, auth=auth)
    
p = req.json().get('processing_info', None)

print(p)

request_data = {
      'status': 'I just uploaded a video with Python.',
      'media_ids': media_id
    }

req = requests.post('https://api.twitter.com/1.1/statuses/update.json', data=request_data, auth=auth)
print(req.json())
