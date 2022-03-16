#!/usr/bin/python3
import requests
 
# Making a PUT request
r = requests.put('https://httpbin.org / put', data ={'key':'value'})
response = requests.put('http://127.0.0.1:'+ str(c) +'/flussonic/api/v3/streams/'+ str(slug) +'', data = data, auth=(str(a), str(b)), headers = {'content-type': 'application/json'})
# check status code for response received
# success code - 200
print(r)
 
# print content of request
print(r.content)

url = 
slug = "gogo12"
data = '{"inputs":[{"url":"' + str(url) + '"}],"title":"' + str(slug) + '","dvr":[{"dvr_limit": 86400},{"expiration": 86400},{"root": "/home/pavel/dvr"}]}'


curl -X PUT -H "Content-Type: application/json" -u flussonic:cvdYP78a -d '{"inputs":[{"url":"rtsp://stream033:stream03@10.200.1.47:554/"}],"title":"ORT"}' "http://127.0.0.1:8080/flussonic/api/v3/streams/ort" 

curl -X PUT -H "Content-Type: application/json" -u flussonic:cvdYP78a -d '{"inputs":[{"url":"rtsp://stream033:stream03@10.200.1.47:554/"}],"title":"ORT","dvr":[{"dvr_limit": 86400,"expiration": 86400,"root": "/home/pavel/dvr"}]}' "http://127.0.0.1:8080/flussonic/api/v3/streams/ort" 