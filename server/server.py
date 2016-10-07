from executor import threadedSlicerExecutor
import shutil
import time
import threading
import urllib

def processMeshUrl(url):
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

    return return_dict
