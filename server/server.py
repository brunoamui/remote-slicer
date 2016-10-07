from executor import threadedSlicerExecutor
import shutil
import time
import threading
import urllib

def processMeshUrl(url):
    local_filename, headers = urllib.urlretrieve(url)
    aux = threadedSlicerExecutor(local_filename)
    aux.start()
    while aux.isAlive():
        time.sleep(5)
    return {"volume": aux.cm3,
            "Filamento": aux.filament_length,
            "Camadas": aux.layers_count,
            "Duracao": str(aux.estimate_duration)}
