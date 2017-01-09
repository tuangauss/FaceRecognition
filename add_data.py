#################### Add_data manual ###############
##### This file is used to build up the library for our recognition app#####
##### The idea is that Microsoft cognitive services does not have a library of public figures ready to use
##### so we have to manually update our database by adding the name + faces of the figures
#### This addition of data only works on the IDE

import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import os
from cs50 import SQL
from helpers import *

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# insert the name of the public figure
name = "Ariana Grande"
# convert the key in the environment to a string
key = str(os.environ.get("Microsoft_key"))
# insert two public URL of the image of the figures
# Microsoft Cognitive service is very particular about getting the url right
# so we have to manually add the urls which end with .jpeg, .jpg, .png
url1 = "http://hellogiggles.com/wp-content/uploads/2015/04/15/Ariana-Grande-2-500x375c.jpg"
url2 = "http://a5.files.biography.com/image/upload/c_fit,cs_srgb,dpr_1.0,q_80,w_620/MTI2NDQwNDA2NTg5MTUwNDgy.jpg"

# headers is among the particulars that we have to send to Microsoft as part of our requests
# headers1 is part of the request to add new name to our database
headers1 = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': key,
}


# params1 specify which database we want to add the person too
params1 = urllib.parse.urlencode({
    'personGroupId' : 'database'})
    
# at first we create a person in the dictionary
body1 = { 'name': name}
body1_1 = json.dumps(body1)

# we send our request to Microsoft to create an entry in our database
create = http.client.HTTPSConnection('api.projectoxford.ai')
create.request("POST", "/face/v1.0/persongroups/database/persons?%s" % params1, body1_1, headers1)
response = create.getresponse()
data1 = response.read()
print(data1)
create.close()

# convert data1 from byte to json
convert1 = data1.decode('UTF-8')
readdata1 = json.loads(convert1)
personId = readdata1["personId"]

#### now we have successfully add a person in the dictionary, we will add photos into the dictionary
params2 = urllib.parse.urlencode({
    'personGroupId' : 'database',
    'personId' : str(personId)
})

body2a = {'url' : url1}
body2a_1 = json.dumps(body2a)

body2b = {'url' : url2}
body2b_1 = json.dumps(body2b)

# we send our request to Microsoft to analyze the two pictures and make the connection between the name and the similar features in these two photos
# add1 adds the first photo
add1 = http.client.HTTPSConnection('api.projectoxford.ai')
add1.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons/{personId}/persistedFaces?%s" % params2, body2a_1, headers1)
response = add1.getresponse()
data2 = response.read()
print(data2)
add1.close()

# add2 adds the second photo
add2 = http.client.HTTPSConnection('api.projectoxford.ai')
add2.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons/{personId}/persistedFaces?%s" % params2, body2b_1, headers1)
response = add2.getresponse()
data3 = response.read()
print(data3)
add2.close()

#### Now we want to add the person in our database to keep track of which celebrity we have in our library:
#### we need to store
# the personID: how MSC recognize a "person"'s identity
# name: so that we can refer back later
# url: so that we have a link to a photo of that celebrity for display in the result html
insert = db.execute("INSERT INTO database (name, personId, url) VALUES (:name, :personId, :url)",
        name = name,
        personId = str(personId),
        url = url1)
# if there is any issue with adding the person, we print out the issue
if not insert:
    print ('We could not add a new person')

    
