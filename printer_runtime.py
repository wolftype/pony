from chiplotle import *

import math
import sys
import subprocess
import os

SP = hpgl.SP
LT = hpgl.LT
FS = hpgl.FS
SM = hpgl.SM
PU = hpgl.PU
PA = hpgl.PA
PD = hpgl.PD
OT = hpgl.OT
OW = hpgl.OW
PG = hpgl.PG
SC = hpgl.SC
IP = hpgl.IP
RO = hpgl.RO
IN = hpgl.IN
CV = hpgl.CV
CI = hpgl.CI
LB = hpgl.LB

class Printer:
    def __init__(self):
        self.commands = []
        self.bVirtual = True

    def instantiate ():
        if self.bVirtual:
	    self.plotter = plottertools.instantiate_virtual_plotter()
        else:
	    self.plotter = instantiate_plotters()[0]

    def write ():
        if self.bVirtual == true:
            subprocess.check_output(['view_hpgl_file.py', output_filename])
        else:
            plotter.write(commands)

class Style:
    def __init__(self):
        self.should_draw_original = True
        self.should_draw_circles = False
        self.should_draw_crosses = False
        self.should_draw_text = False

class State:
    def __init__(self):
        self.circle_coords_radius = 20
        self.pen_number = 1
        self.text = ""
        self.line_type = 1

class File:
    def __init__(self, name):
        self.input = name or ""
        self.output = "output.hpgl"

class Calibration:
    def _init__(self):
        self.reg_x = 0.0
        self.reg_y = 0.0
        self.img_x_scale = 1.0
        self.img_y_scale = 1.0
        self.reg_x_percentage = 0.0
        self.reg_y_percentage = 0.0
        self.reg_is_centered = True
        self.paper_y_dim = 10170 		#11"
        self.paper_x_dim = 7840 		#8.5"
        self.paper_x_dim_B = 16450		#17"
        self.paper_height_inches = 11
        self.paper_width_inches = 8.5
        self.paper_width_inches_B = 17
        self.preserve_source_aspect = True

    def scale (x,y, bAbsolute):
        if bAbsolute:
            self.img_x_scale = x/self.paper_width_inches
            self.img_y_scale = y/self.paper_height_inches
        else:
            self.img_x_scale = x
            self.img_y_scale = y

     def register (x,y,bAbsolute):
        if bAbsolute:
            self.reg_x_percentage = float(args[iter+1])/self.paper_width_inches
    	    self.reg_y_percentage = float(args[iter+2])/self.paper_height_inches
        else:
            self.reg_x_percentage = x
            self.reg_y_percentage = y

    def calc ():
        xmin = 1000000.0
        xmax = 0.0
        ymin = 1000000.0
        ymax = 0.0

class Print:
    def _init_(self, args):
        self.file = File()
        self.printer = Printer()
        self.calibration = Calibration ()
        self.style = Style()
        self.state = State ()

        for iter, i in enumerate(args):
            if i == "-i": #filename input 
                self.file.input_filename = args[iter+1]
            if i == "-o": #filename to save as
                self.file.output_filename = args[iter+1]
            if i == "-p": #actually send to printer
                self.printer.bVirtual = False
            if i == "-sr": #scale relatively (0,1.0)
                self.calibration.scale (float(args[iter+1]), float(args[iter+2], False)
            if i == "-sa": #scale absolutely (in inches)
                self.calibration.scale (float(args[iter+1]), float(args[iter+2], True)
            if i == "-rr": #register relatively from 0,1
                self.calibration.register (float(args[iter+1]), float(args[iter+2], False)
            if i == "-ra": #register absolutely (in inches)
                self.calibration.register (float(args[iter+1]), float(args[iter+2], True)
            if i == "-c": #make all coordinates circles of radius
                self.style.should_draw_circles = True
                self.style.circle_coords_radius = float(args[iter+1])
            if i == "-x": #make all coordinates Xs
                self.style.should_draw_crosses = True
                self.style.cross_coords_length = float(args[iter+1])
            if i == "-no": #don't draw lines
                self.style.should_draw_original = False
            if i == "-sp": #select pen
                self.state.pen_number = int(sys.argv[iter+1])
            if i == "-t": #text
                self.style.should_plot_text = True
                self.state.text = args[iter+1]


