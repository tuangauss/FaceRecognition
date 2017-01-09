#################### Helpers manual ###############
##### This is the crux of my app#####
##### All of the main functions are defined here#####

# import necessary libraries
import csv
import urllib.request

from flask import redirect, render_template, request, session, url_for
from functools import wraps
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import json
from cs50 import SQL

import requests
import uuid

# convert the two keys into string for requests
key = str(os.environ.get("Microsoft_key"))
dropboxkey = "Bearer " + str(os.environ.get("Dropbox_key"))

# define apology (to use in case of errors)
# credit to CS50 Problem Set 7
# I did not code the apology function on my own, and have no intention of claim ownership over the code. All rights go to the rightful owner
def apology(top="", bottom=""):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=escape(top), bottom=escape(bottom))

# this is probably the most important function of the webapp as it allows Microsoft cognitive service (MSC) to analyze the photos

def detect_identify (url):
    # activate our SQL database
    db = SQL("sqlite:///database.db")
    
    # create headers as stipulate by Microsoft Face API
    # headers is part of the request
    headers = {
    # Request headers
    # I also include my personal subscription key, please don't tamper with it
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': key,}
    
    # this params1 is used for detecting face
    params1 = urllib.parse.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age', })
    
    # this params2 is used for identifying face
    # this is stipulated by the MSC Face API
    params2 = urllib.parse.urlencode({})
    
    # parse in the url of the image into the body of the request
    body =  {'url': url}
    body1 = json.dumps(body)
    
    
        # send request to detect face in the photos
    detect = http.client.HTTPSConnection('api.projectoxford.ai')
    detect.request("POST", "/face/v1.0/detect?%s" % params1, body1, headers)
        # get responses as JSOn value
    response1 = detect.getresponse()
    data1 = response1.read()
    print(data1)
        # since it turns out that Microsoft returns the result as a byte type, we need to covert it to string 
    convert1 = data1.decode('UTF-8')
    readdata1 = json.loads(convert1)
        
        # Explanation:
        # - At this stage, what happens on MSC Face API is that
        # - they receive a url of the image
        # - they will run some complicated facial recognition based on neural networks to detect the face in the photo
        # - and accompanying features such as (age, beard, glasses, ratio between nose and eye distant, etc)
        # - that face is assigned a face-id
        # we need to refer to this face-id if we want to refer to it later on
    
    # Now if a face cannot be detected (think, uploading a photo of a river)
    # then error 1 will be returns
    if not readdata1:
        finalresult = "error1"
        return finalresult
    faceid = readdata1[0]["faceId"]
    age = readdata1[0]["faceAttributes"]["age"]
    detect.close()
        
    try:    
        # now, we try to send request to identify face
        # explanation:
        # - now that MSC has identifies a face in our submitted photo
        # - we will send a request for MSC to run through our database (library) of faces
        # - and pick out which faces resemble the most
        # - for simplicity sake, I limit at 1 candidate return, and super low threshold
        # - but if absolutely noone looks like you, MSC will return an empty Json
        
        # this is our request
        newbody = { "personGroupId":"database", "faceIds":[ faceid], "maxNumOfCandidatesReturned":1, "confidenceThreshold": 0.1}
        newbody1 = json.dumps(newbody)
        identify = http.client.HTTPSConnection('api.projectoxford.ai')
        identify.request("POST", "/face/v1.0/identify?%s" % params2, newbody1, headers)
        # we get the response from MSC
        response = identify.getresponse()
        # read the response
        data2 = response.read()
        # we have to decode it and convert it to a json file
        convert2 = data2.decode('UTF-8')
        readdata2 = json.loads(convert2)
        
        identify.close()
        # since MSC will return candidates with his personID (not the celebrity name)
        # we will retrieve this data
        # and the confident level
        name = readdata2[0]["candidates"][0]["personId"]
        confidence = readdata2[0]["candidates"][0]["confidence"]
        #### Now we search from the database for name associated with that personId
        rows = db.execute("SELECT * FROM database WHERE personId = :personId", personId = name)
        
        # we store the name into exactname
        exactname = rows[0]["name"]
        # we also take out a photo of that celebrity for display
        image = str(rows[0]["url"])
        # convert our confidence level to percent scale
        confidencelevel = str(confidence*100)
        # create a statement
        statement = "You look like " + exactname + " with " + confidencelevel + " % confidence"
        
        # return the result as a dictionary, this is useful for html to pickup and display it on the web
        finalresult = {"age":age ,"statement" : statement, "image" : image,  "confidence": confidence}
        return finalresult
    except Exception as e:
        # again, I simplify the logic
        # anything wrong along the way, is lumped into one big issue called "error2"
        # I recognize this is not the best design, but at least errors are recognized and picked out
        finalresult = "error2"
        return finalresult

# now, sometime, the file we submit is either from our laptop or an snapshot from the webcam
# so it does not have a public URL
# the critical condition for MSC to process and return resut
# so the idea here is too upload the file to DROPBOX using dropbox API
# and then get the public link
# this is also good storage of image file
def upload (name, file):
    # this is part of the request sent to Dropbox
    url = "https://content.dropboxapi.com/2/files/upload"
    # get the name
    filename = str(name)
    
    # headers file

    headers = {
        "Authorization": dropboxkey,
        "Content-Type": "application/octet-stream",
        "Dropbox-API-Arg": "{\"path\":\"/API/" + filename+ "\"}"
    }
    # we read the file
    data = file.read()
    
    # then we send the upload request to Dropbox
    # dropbox will upload the photo (of course to my dropbox)
    # and create an internal link
    upload = requests.post(url, headers=headers, data=data)
    #convert response to json so that we can read the path within our dropbox
    data = json.loads(upload.text)
    
    # now we get an internal dropbox link
    # this is a good start, but still not usable by MSC
    # create_url will expose the image file publicly and retrieve a public link
    return data["path_display"]
    
def create_url (path):
    # we send the request to DROPBOX
    url2 = "https://api.dropboxapi.com/2/sharing/create_shared_link"

    headers2 = {
        "Authorization": dropboxkey,
        "Content-Type": "application/json"
    }
    data2 = {"path": path}
    # we send the request to publicly expose the image file to dropbox
    create_url = requests.post(url2, headers=headers2, data=json.dumps(data2))
    
    #read the url and try to modify them into a permanent url that microsoft cognitive service can read
    data2 = json.loads(create_url.text)
    temp1 = data2["url"]
    
    # we change the name of the file into something the MSC can read
    # in essence: "https:/www.dropbox.com/image.jpg"
    # will become: "https:dl.dropboxuserconent.com/image.jpg"
    # which is usale by MSC
    cut = temp1.split("www.dropbox")
    perm = cut[0] + "dl.dropboxusercontent"+ cut[1]
    
    # we return the modified link
    return perm