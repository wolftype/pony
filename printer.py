from printer_runtime import *

#GLOBAL VARS
input_filename = ""
output_filename = ""
virtual = True
plotter = 0


#ACTUAL WIDTH OF PAPER (add _coord)
paper_y_dim = 10170 		#11"
paper_x_dim = 7840 		#8.5"
paper_x_dim_B = 16450		#17"

##PAPER WIDTH AND HEIGHT IN INCHES
paper_height_inches = 11 
paper_width_inches = 8.5 
paper_width_inches_B = 17

##OUTPUT IMAGE SCALE FACTOR
img_x_scale = 1.0
img_y_scale = 1.0
preserve_source_aspect = True

#BOUNDING BOX OF INPUT IMAGE
xmin = 1000000.0
xmax = 0.0
ymin = 1000000.0
ymax = 0.0

#REGISTRATION
reg_x = 0
reg_y = 0
reg_x_percentage = 0
reg_y_percentage = 0
reg_is_centered = True

#POST EFFECTS
#whether to pick random colors for each PD command
should_randomize_colors = False
#whether to draw original line drawing
should_draw_original = True
#whether to replace PD commands with CI commands
should_draw_circles = False
circle_coords_radius = 20.0;
#whether to replace PD commands with Xs
should_draw_crosses = False
cross_coords_length = 20.0;
#whether to plot text
should_plot_text = False
text = ""

##PENS:
#1: hb pencil |  2: 2b pencil | 3: red pencil | 4: 4b pencil
#5: blue pencil | 8: blue pen
pen_number = 8

#ARGUMENTS (loop over once looking for -l flag)
for iter, i in enumerate(sys.argv):
	print iter, i
	if i == "-l": #long format (11x17)
		paper_x_dim = paper_x_dim_B
		paper_width_inches = paper_width_inches_B
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

# loop over again, now that we know paper size
for iter, i in enumerate(sys.argv):
	if i == "-i": #filename to send
		input_filename = sys.argv[iter+1]
	if i == "-p": #actually send to printer
		virtual = False
	if i == "-o": #filename to save as
		output_filename = sys.argv[iter+1]
	if i == "-sr": #scale relatively (0,1.0)
		img_x_scale = float(sys.argv[iter+1])
		img_y_scale = float(sys.argv[iter+2])
	if i == "-sa": #scale absolutely (in inches)
		img_x_scale = (float(sys.argv[iter+1])/paper_width_inches)
		img_y_scale = (float(sys.argv[iter+2])/paper_height_inches)
	if i == "-rr": #register relatively from 0,1
		reg_x_percentage = float(sys.argv[iter+1])
		reg_y_percentage = float(sys.argv[iter+2])
		reg_is_centered = False
	if i == "-ra": #register absolutely (in inches)
		reg_x_percentage = float(sys.argv[iter+1])/paper_width_inches
		reg_y_percentage = float(sys.argv[iter+2])/paper_height_inches
		reg_is_centered = False
	if i == "-c": #make all coordinates circles of radius
		should_draw_circles = True
		circle_coords_radius = float(sys.argv[iter+1])
	if i == "-x": #make all coordinates Xs
		should_draw_crosses = True
		cross_coords_length = float(sys.argv[iter+1])
	if i == "-no": #don't draw lines
		should_draw_original = False
        if i == "-sp": #select pen
                pen_number = int(sys.argv[iter+1])
        if i == "-t": #text
                should_plot_text = True
                text = sys.argv[iter+1]

#OUTPUT IMAGE WIDTH AND HEIGHT
img_x_dim = paper_x_dim * img_x_scale
img_y_dim = paper_y_dim * img_y_scale

#BOTTOM LEFT CORNER
if reg_is_centered == True:
	reg_x = (paper_x_dim - img_x_dim) / 2.0
	reg_y = (paper_y_dim - img_y_dim) / 2.0
else:
	reg_x = paper_x_dim * reg_x_percentage
	reg_y = paper_y_dim * reg_y_percentage

pos_commands = []
if input_filename != "":
    IG = io.import_hpgl_file(input_filename)
    #for each COMMAND in the input file
    for p in IG:
    	#if the name is Up or Down and its not empty
    	if ((p._name == 'PU' or p._name == 'PD') and len(p.xy) > 0 ):
     		if p.x[0] > xmax:
     			xmax = p.x[0]
     		if p.x[0] < xmin:
     			xmin = p.x[0]
     		if p.y[0] > ymax:
     			ymax = p.y[0]
     		if p.y[0] < ymin:
     			ymin = p.y[0]


    #WIDTH of input image
    tw = float(xmax - xmin)
    #HEIGHT of input image
    th = float(ymax - ymin)
    #input aspect ratio
    aspect = tw/th
    #adjustment ratio WIDTH
    rw = img_x_dim / tw
    #adjustment ratio HEIGHT
    if preserve_source_aspect == True:
        rh = rw
    else:
        rh = img_y_dim / th

    #Resize
    for p in IG:
    	if ((p._name == 'PU' or p._name == 'PD') and len(p.xy) > 0 ):
    		tmp = CoordinateArray( [ ( reg_x + p.x[0] * rw, reg_y + p.y[0] * rh ) ] )
    		p.xy = tmp
    		pos_commands.append(p)

#Post Effects
#tentatively make all coordinates circles
cir_commands = []
for c in pos_commands:
	if (c._name == 'PD'):
		c = CI(30)
	cir_commands.append(c)


#OUTPUT FILENAME
if output_filename == "":
	name, ext = os.path.splitext(input_filename)
	output_filename = name + "_output.hpgl"

print "paper size: ", paper_x_dim, paper_y_dim
#print "input file: ", input_filename, tw, th, "aspect ratio input: ", tw/th
print "output file: ", output_filename, img_x_dim, img_y_dim, "aspect ratio output: ", img_x_dim/img_y_dim

#ASSEMBLE COMMANDS
commands = []
commands.append(IN())	 #initialize
commands.append(FS(8))  #set force
#commands.append(LT(4))  #set line type

if (should_draw_original):
	commands.append(SP(pen_number))	 #select pen
	for p in pos_commands:
		commands.append(p)

if (should_draw_circles):
	commands.append(SP(pen_number))	 #select pen
	for c in cir_commands:
		commands.append(c)

if (should_plot_text):
	commands.append(SP(pen_number))	 #select pen
        commands.append(PA([(reg_x , reg_y)])) #registration
        commands.append(hpgl.SI(img_x_scale, img_y_scale))
        commands.append(hpgl.LB(text))
        commands.append(IN())

io.save_hpgl (commands, output_filename)

if virtual:
	plotter = plottertools.instantiate_virtual_plotter()
	subprocess.check_output(['view_hpgl_file.py', output_filename])
else:
	plotter = instantiate_plotters()[0]


plotter.write(commands)


