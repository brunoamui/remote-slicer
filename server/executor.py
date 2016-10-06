import pexpect
import threading
import time

files_to_slice = ['../stl/BeardedYell_Low_137k_Solid.stl', '../stl/BeardedYell_Mid_372k_Solid.stl', '../stl/BeardedYell_High_965k_Solid.stl']
threads = []


class threadedSlicerExecutor(threading.Thread):
    def __init__(self, file):
        threading.Thread.__init__(self)
        self.slic3r_cmd = '../Slic3r/bin/slic3r '
        self.slic3r_opt = '--support-material '
        self.files_to_slice = file
        self.result = ""
        self.timeout = 1000
        return

    def run(self):
        try:
            child = pexpect.spawn(self.slic3r_cmd + self.slic3r_opt + self.files_to_slice)
            child.expect(pexpect.EOF, timeout=self.timeout)
            self.result = child.before
        except(pexpect.exceptions.TIMEOUT):
            self.result = "TIMEOUT"


for file in files_to_slice:
    aux = threadedSlicerExecutor(file)
    aux.start()
    threads.append(aux)

while threads:
    for thr in threads:
        if thr.isAlive():
            print thr.files_to_slice, "Processando"
        else:
            print thr.result
            threads.remove(thr)
    time.sleep(2)
