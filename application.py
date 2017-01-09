
##### This is where everything is handled at the back-end#####

# import all necessary libraries
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir
import uuid
import base64
import io

from helpers import *

import os
from werkzeug.utils import secure_filename

# configure application
app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
        
# configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# this is the back-end for the passurl function
# meaning that you can analyze a pass in a picture with its public url
@app.route("/passurl", methods=["GET", "POST"])
def passurl():
    
    if request.method == "GET":
        return render_template ("passurl.html")
    else:
        # once we receive the url from the user
        # check if they actually put in a URL
        if not request.form.get("passurl"):
            return apology ("MISSING URL")
        
        # convert a url to a string    
        url = str(request.form.get("passurl"))
        
        # call the detect_identify function from the helper file
        # result will carry out the face of your doppleganger and the value of confidence
        result = detect_identify(url)
        
        #### if we cannot detect face, return error 1
        if (result == "error1"):
            return render_template ("fail1.html", you = url)
        # if we have trouble finding similar faces or the confidence is too low, return error 2
        if (result == "error2"):
            return render_template ("fail2.html", you = url)        
        if result["confidence"] < 0.2:
            return render_template ("fail2.html", you = url)
        
        # if all is successful, we render the result template    
        return render_template("result.html", finalresult = result, you = url)
        
# this part allows user to upload image directly from your computer, laptop
# It is sort of similar to passurl
# the main issue is MSC only processes image hosted in public url
# so I need to upload the photo to dropbox, expose it to a public url
# and pull it back for processing by MSC
@app.route("/folder", methods=["GET", "POST"])
def folder():
    if request.method == "GET":
        return render_template ("upload.html")
    else:
        # once you receive the file selected by the user
        # do some sanity check
        if 'file' not in request.files:
            return apology ("No file selected")
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return apology ("No file selected")
        name = file.filename
        
        # we call the upload function from the helpers to upload the photo to DROPBOX using the dropbox API
        path = upload(name,file)
        
        # then we use the create_url function from the helpers to create a valid link for MSC
        link = create_url (path)
        
        # then we call detect_identity from MSC to process and return the result
        result = detect_identify(link)
        
        if (result == "error1"):
            return render_template ("fail1.html", you = link)
        if (result == "error2"):
            return render_template ("fail2.html", you = link)         

        if result["confidence"] < 0.2:
            return render_template ("fail2.html", you = link)        
        
        return render_template("result.html", finalresult = result, you = link)        
        

#The function belows facilitates capturing the snapshot and processing it directly
#literally the highlight of my app
#The idea is:
# - once you receive data from Javascript
# - you create a random name (so they don't collapse with others on dropbox) by uuid function
# - you open this file and write data of photo from Javascript
# - you upload this file to Dropbox (similar to upload)
# - then you delete the file
@app.route("/selfie", methods=["GET", "POST"])
def selfie():
    if request.method == "GET":
        return render_template ("selfie.html")
    else:
        # receive data of image from Javascript 
        # I believe it is in a form a super long string
        data = request.form['mydata']
        
        if (data == None):
            return apology ("try tale the photo again")
        # if user does not select file, browser also
        # submit a empty part without filename
        name = str(uuid.uuid4()) + ".jpg" 
        fh = open(name, "wb")
        
        # write the data of the photo into the new file
        fh.write(base64.b64decode(data))
        fh.close()
        
        # open the file so that we can upload it to Dropbox and expose it to a public url
        file = open (name, "rb")
        path = upload(name,file)
        file.close()
        
        # create a link for the file
        link = create_url (path)
        # use detect_identify from helpers to get the processed result
        result = detect_identify(link)
 
        
        # then we remove the file from our directory
        os.remove(name)
        # error1 means a face cannot be detected from any photo you uploaded
        if (result == "error1"):
            return render_template ("fail1.html", you = link)
        
        # error2 means MSC cannot find a similar face
        if (result == "error2"):
            return render_template ("fail2.html", you = link)        
        # publish the result
        if result["confidence"] < 0.2:
            return render_template ("fail2.html", you = link)                
        return render_template("result.html", finalresult = result, you = link)    
        
    
@app.route("/")
def index():
    ## make sure that the two keys are imported 
    if not os.environ.get("Microsoft_key"):
        raise RuntimeError("Microsoft_key not set")
    
    if not os.environ.get("Dropbox_key"):
        raise RuntimeError("Dropbox_key not set")    
        
    return render_template ("index.html")