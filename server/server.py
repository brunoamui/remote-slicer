from executor import threadedSlicerExecutor
import shutil
import time
import threading
import urllib
import pyrebase

config = {  "apiKey": "AIzaSyCU4aVz8qFvgGmor3f0lU7K6kA161RBv18",
            "authDomain": "fab-pro.firebaseapp.com",
            "databaseURL": "https://fab-pro.firebaseio.com",
            "storageBucket": "fab-pro.appspot.com",
            "serviceAccount": "Fab-Pro-a217f1a86f46.json"}
firebase = pyrebase.initialize_app(config)
db = firebase.database()



def processMeshUrl(url, user_id):
    local_filename, headers = urllib.urlretrieve(url)

    executors = [("High", threadedSlicerExecutor(local_filename, " --layer-height 0.1 ")),
                 ("Medium", threadedSlicerExecutor(local_filename, " --layer-height 0.2 ")),
                 ("Low", threadedSlicerExecutor(local_filename, " --layer-height 0.3 "))]

    for tuple in executors:
        tuple[1].start()

    return_dict = {}

    while executors:
        for tuple in executors:
            if tuple[1].isAlive():
                time.sleep(0.1)
            else:
                dados = {"volume": tuple[1].cm3,
                         "Filamento": tuple[1].filament_length,
                         "Camadas": tuple[1].layers_count,
                         "Duracao": str(tuple[1].estimate_duration),
                         "url": url}
                return_dict[tuple[0]] = dados
                executors.remove(tuple)

    db.child("users").child(user_id)

    data_dict = {"users/"+user_id: return_dict}
    db.update(data_dict)
    return return_dict
