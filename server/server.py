from executor import threadedSlicerExecutor
import shutil
import time
import threading
import urllib
url = "http://files.jotform.com/jufs/bsbfablab/62786174857674/351529526954964320/Twisted_Vase_Basic.stl"

local_filename, headers = urllib.urlretrieve(url)

aux = threadedSlicerExecutor(local_filename)
aux.start()

while aux.isAlive():
    print "Slic3r - Processando"
    time.sleep(5)

print "GCODE:", aux.gcode_path
print "mm:", aux.mm
print "cm3:", aux.cm3
print "Filamento:", aux.filament_length
print "Camadas:", aux.layers_count
print "Duracao:", aux.estimate_duration
