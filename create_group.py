# thiis the file used to create a group 
# in essence our library to store celebrities name and their associated faces (that we choose)
# the code below is suggested and inspired by the Microsoft Cognitve Service
# it is open for public use at "https://www.microsoft.com/cognitive-services/en-us/face-api"


# this works in the IDE
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64
# convert the Microsoft key to a string
key = str(os.environ.get("Microsoft_key"))
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': key,
}


params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('api.projectoxford.ai')
    conn.request("PUT", "/face/v1.0/persongroups/database?%s" % params, "{'name' : 'data'}" , headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))