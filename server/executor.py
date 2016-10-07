import pexpect
import threading
import time
import sys
sys.path.append("../Printrun/printrun")
import gcoder

files_to_slice = ['../stl/BeardedYell_Low_137k_Solid.stl', '../stl/BeardedYell_Mid_372k_Solid.stl', '../stl/BeardedYell_High_965k_Solid.stl']
threads = []


class threadedSlicerExecutor(threading.Thread):
    def __init__(self, file, opt_add=""):
        threading.Thread.__init__(self)
        self.slic3r_cmd = '../Slic3r/bin/slic3r '
        self.slic3r_opt = '--support-material --nozzle-diameter 0.4 --filament-diameter 1.75 --output_filename_format [input_filename_base]_[layer_height].gcode' + opt_add + " "
        self.files_to_slice = file
        self.result = ""
        self.timeout = 1000
        self.child = pexpect.spawn(self.slic3r_cmd + self.slic3r_opt + self.files_to_slice)
        self.gcode_path = ""
        self.mm = ""
        self.cm3 = ""
        self.xdims = ()
        self.ydims = ()
        self.zdims = ()
        self.filament_length = 0
        self.layers_count = 0
        self.estimate_duration = 0
        return

    def run(self):
        try:
            self.child.expect("Processing triangulated mesh", timeout=10)
            self.child.expect("Exporting G-code to ([^ ]+)[\r\n]", timeout=self.timeout)
            self.gcode_path = self.child.match.groups()[0][:-1]
            self.child.expect("Filament required: (.*)mm \((.*)cm3\)[\r\n]", timeout=30)
            self.mm, self.cm3 = self.child.match.groups()
            self.child.expect(pexpect.EOF, timeout=30)
            self.result = self.child.before

            gcode = gcoder.GCode(open(self.gcode_path, "rU"))
            self.xdims = (gcode.xmin, gcode.xmax, gcode.width)
            self.ydims = (gcode.ymin, gcode.ymax, gcode.depth)
            self.zdims = (gcode.zmin, gcode.zmax, gcode.height)
            self.filament_length = gcode.filament_length
            self.layers_count = gcode.layers_count
            self.estimate_duration = gcode.estimate_duration()[1]

        except(pexpect.exceptions.TIMEOUT):
            self.result = "TIMEOUT"
