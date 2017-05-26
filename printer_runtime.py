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
        self.bVirtual = True

    def instantiate ():
        if self.bVirtual:
	    self.plotter = plottertools.instantiate_virtual_plotter()
        else:
	    self.plotter = instantiate_plotters()[0]

class Style:
    def __init__(self):
        self.should_draw_original = True
        self.should_draw_circles = False
        self.should_draw_crosses = False
        self.should_draw_text = False
        self.should_randomize_colors = False

class State:
    def __init__(self):
        self.circle_coords_radius = 20.0
        self.cross_coords_length = 20.0
        self.pen_number = 1
        self.text = ""
        self.line_type = 1

class File:
    def __init__(self, name):
        self.input = name or ""
        tname, ext = os.path.splitext(name)
        self.output = tname+"_output.hpgl"
        self.width_coord = 0.0
        self.height_coord = 0.0
        self.aspect = 1.0
        self.load (name)

    def load (name):
        if name != "":
            self.input = name
            self.input_commands = io.import_hpgl_file(self.input)
            xmin = 1000000.0
            xmax = 0.0
            ymin = 1000000.0
            ymax = 0.0

            #for each COMMAND in the input file
            for p in self.input_commands:
                #if the command name is Up or Down and its not empty, get max size
                if ((p._name == 'PU' or p._name == 'PD') and len(p.xy) > 0 ):
                    if p.x[0] > xmax:
                        xmax = p.x[0]
                    if p.x[0] < xmin:
                        xmin = p.x[0]
                    if p.y[0] > ymax:
                        ymax = p.y[0]
                    if p.y[0] < ymin:
                        ymin = p.y[0]

            self.width_coord = float(xmax-xmin);
            self.height_coord = float(ymax-ymin);
            self.aspect = self.width_coord/self.height_coord

class Calibration:
    def _init__(self):
        self.reg_x = 0.0
        self.reg_y = 0.0
        self.img_x_scale = 1.0
        self.img_y_scale = 1.0
        self.img_x_coord = 7840
        self.img_y_coord = 10170
        self.reg_x_percentage = 0.0
        self.reg_y_percentage = 0.0
        self.reg_is_centered = True
        self.paper_y_coord = 10170 		#11"
        self.paper_x_coord = 7840 		#8.5"
        self.paper_x_coord_B = 16450		#17"
        self.paper_height_inches = 11
        self.paper_width_inches = 8.5
        self.paper_width_inches_B = 17
        self.preserve_source_aspect = True

    def long ():
        self.paper_x_coord = self.paper_x_coord_B
        self.paper_width_inches = self.paper_width_inches_B

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
        #OUTPUT IMAGE WIDTH AND HEIGHT
        self.img_x_coord = self.paper_x_coord * self.img_x_scale
        self.img_y_coord = self.paper_y_coord * self.img_y_scale

        #BOTTOM LEFT CORNER
        if reg_is_centered == True:
            reg_x = (paper_x_coord - img_x_coord) / 2.0
            reg_y = (paper_y_coord - img_y_coord) / 2.0
        else:
            reg_x = paper_x_coord * reg_x_percentage
            reg_y = paper_y_coord * reg_y_percentage


class Print:
    def _init_(self, args):
        self.file = File()
        self.printer = Printer()
        self.calibration = Calibration ()
        self.style = Style()
        self.state = State ()
        self.pos_commands = []
        self.cir_commands = []
        self.commands = [IN(),FS(8)]

        for iter, i in enumerate(args):
            print iter, i
            if i == "-l": #long format (11x17)
                self.calibration.long ()
            if i == "-help": #print out below
                print ("""
                    -i  input_filename
                    -o  output_filename
                    -p  actually send to printer
                    -sr scaling relative
                    -sa scale absolute
                    -rr register relative
                    -ra register absolute
                    -c  draw circles around coordinates
                    -x  draw crosses around coordinates (not implemented)
                    -no do not draw original line drawing
                    -sp select pen
                        1: hb pencil   |  2: 2b pencil | 3: red pencil | 4: 4b pencil
                        5: blue pencil |  6: black pen | 7: red pen    | 8: blue pen
                """)
                sys.exit("----")

            for iter, i in enumerate(args):
                if i == "-i": #filename input
                    self.file.input = args[iter+1]
                if i == "-o": #filename to save as
                    self.file.output = args[iter+1]
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


            self.calibration.calc()
            self.resize()
            self.prepare()

    def resize():
        rw = 1.0
        rh = 1.0
        rw = self.calibration.img_x_coord / self.file.width_coord
        if self.calibration.preserve_source_aspect == True:
            rh = rw
        else:
            rh = self.calibration.img_y_coord / self.file.height_coord

        for p in self.file.input_commands:
    	if ((p._name == 'PU' or p._name == 'PD') and len(p.xy) > 0 ):
            tmpx = self.calibration.reg_x + p.x[0] * rw
            tmpy = self.calibration.reg_y + p.y[0] * rh 
            p.xy = CoordinateArray( [ (tmpx, tmpy) ] )
            self.pos_commands.append(p)

    def prepare():

        if (self.style.should_draw_original):
            self.commands.append(SP(self.style.pen_number))
            for p in self.pos_commands:
                self.commands.append(p)

        if (self.style.should_draw_circles):
            self.commands.append(SP(self.style.pen_number))
            for c in self.pos_commands:
	    if (c._name == 'PD'):
		c = CI(30)
	        self.commands.append(c)

        if (should_plot_text):
            self.commands.append(SP(self.style.pen_number))
            self.commands.append(PA([(self.calibration.reg_x , self.calibration.reg_y)]))
            self.commands.append(hpgl.SI(self.calibration.img_x_scale, self.calibration.img_y_scale))
            self.commands.append(hpgl.LB(self.state.text))

    def send():
        io.save_hpgl (self.commands, self.file.output)

        if self.plotter.bVirtual:
	    subprocess.check_output(['view_hpgl_file.py', self.file.output])
        else:
            plotter.write(commands)

