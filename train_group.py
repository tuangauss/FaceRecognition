# thiis where we train the group
# in essence even though MSC hosts a bunch of names and their associated faces
# every time we add_data to our libary
# we have to train our dataset again
# so that new data is recognized and taken into consideration by the MSC
# the code below is suggested and inspired by the Microsoft Cognitve Service
# it is open for public use at "https://www.microsoft.com/cognitive-services/en-us/face-api"

import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '616963a716e441aaae75a834e78b021c',
}

body = ''
params = urllib.parse.urlencode({
    'personGroupId' : 'database'
})

try:
    conn = http.client.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/face/v1.0/persongroups/database/train?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))