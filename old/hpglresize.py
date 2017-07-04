from chiplotle import *	
plotter = instantiate_plotters()[0]
#plotter = plottertools.instantiate_virtual_plotter()
import math

commands = []	

img_width = 4800
img_height = 4800

#8.5 x 11
paper_width = 10170
paper_height = 7840

border_width = (paper_width - img_width) / 2.0
border_height = (paper_height - img_height) / 2.0

G = "p2.hpgl"

S = shapes
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

IG = io.import_hpgl_file(G)

commands.append(IN())	 #initialize
commands.append(SP(8))	 #select pen
commands.append(FS(8)) #set force
#commands.append(LT(1)) #set line type

#GET BOUNDING BOX
xmin = 0.0
xmax = 0.0
ymin = 0.0
ymax = 0.0

xx = CoordinateArray ([(100,100)])
print (xx.x[0])

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

#total WIDTH 
tw = xmax - xmin
#total HEIGHT
th = ymax - ymin
#ratio WIDTH
rw = img_width / tw
#ratio HEIGHT
rh = img_height / th

print(tw,th)
print("resized by: ", rw, rh)
print("to: ", img_width, img_height)

#Resize
for p in IG:
	if ((p._name == 'PU' or p._name == 'PD') and len(p.xy) > 0 ):
		tmp = CoordinateArray( [ ( border_width + p.x[0] * rw, border_height + p.y[0] * rh ) ] )
		p.xy = tmp
		#print(p.xy)
		commands.append(p)

io.save_hpgl (commands, "output.hpgl")

plotter.write( commands )

# switch = 0

# #we are going to separate commands based on pen color
# sep = [[],[],[],[],[],[],[],[],[],[],[]]

# pencolors = [1]
# penidx = 0

#For each command, assign to a different PEN
# for p in IG:
# 	if (p._name == 'PU' or p._name == 'PD'):
# 		tmp = CoordinateArray( [ ( border_width + p.x[0] * rw, border_height + p.y[0] * rh ) ] )
# 		p.xy = tmp		
#  		# c.append(p)
# 		switch += 1
# 		if (switch >= 4) and (p._name != 'PD'):
# 			switch = 0
# 			if penidx < len(pencolors)-1:
# 				penidx += 1
# 			else:
# 				penidx = 0
			
# 		sep[ pencolors[penidx] ].append(p)	

# sort by pen color
# for i, x in enumerate(sep):
# 	c.append(SP(i))
# 	for com in x:
# 		c.append(com)
		

