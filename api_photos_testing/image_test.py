import pyrebase
import requests
from io import BytesIO

config = {
    "apiKey": "AIzaSyDGuhNWHM0fqG1LUHI9FWUMRj8fIRBVTYw",
    "authDomain": "doggo-11f55.firebaseapp.com",
    "projectId": "doggo-11f55",
    "storageBucket": "doggo-11f55.appspot.com",
    "messagingSenderId": "1013988505400",
    "appId": "1:1013988505400:web:63b457e6d2536526c033cd",
    "measurementId": "G-YCSP4C5BG1",
    "serviceAccount" : "api_photos_testing/serviceAccount.json",
    "databaseURL" : "https://doggo-11f55-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)

# Access the storage bucket
storage = firebase.storage()

# Upload the image to the bucket
storage.child("images/image.jpg").put("api_photos_testing/image.jpg")

