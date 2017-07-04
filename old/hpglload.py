from chiplotle import *	
plotter = instantiate_plotters()[0]
# plotter = plottertools.instantiate_virtual_plotter()
import math

sl = -17000
sb =  -11184
mywidth =34000
myheight = 22368

dx = 15000.0
dy = 9000.0

width = dx * 2.0
height = dy * 2.0

# A = "hpgl/c18_hpgl"
# B = "hpgl/circle_08_hpgl"
# C = "hpgl/COMBO_00_hpgl_a1"
# D = "hpgl/plottest_04_hpgl"
# E = "hpgl/cshapes_00_hpgl"
# G = "hpgl/optics_comp_01_hpgl" #
# G = "hpgl/warp2_hpgl" #
# G = "hpgl/cit_01_hpgl" #
G = "hpgl/circles_06_hpgl" #
# G = "hpgl/optics_042_hpgl" #
# G = "hpgl/twists5_hpgl"
# "hpgl/twist3_04_hpgl"
# G = "hpgl/twines_02_hpgl"
# G = "hpgl/tikz_twine_01_hpgl"

S = shapes
SP = hpgl.SP
LT = hpgl.LT
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

c = []	
# 
# IA = io.import_hpgl_file(A)
# IB = io.import_hpgl_file(B)
# IC = io.import_hpgl_file(C)
# ID = io.import_hpgl_file(D)
# IE = io.import_hpgl_file(E)
# IF = io.import_hpgl_file(F)
IG = io.import_hpgl_file(G)
# 
# c.append(OT)
# c.append(OW)
# c.append
# 


# c.append(SC([(-17214,17214),(-11482,11482)]))
# 
c.append(IN())
# c.append( SP(1) )
# c.append( RO(90) )
# c.append( CV(1,100) )
# c.append( PU([(-17000,11000)]))
# c.append( PD([(-15000,11000)]))
# for p in IE:
# 	c.append(p)

xmin = 0.0
xmax = 0.0
ymin = 0.0
ymax = 0.0

for p in IG:
	if (p._name == 'PU' or p._name == 'PD'):
		if p.x[0] > xmax: 
			xmax = p.x[0]
		if p.x[0] < xmin:
			xmin = p.x[0]
		if p.y[0] > ymax:
			ymax = p.y[0]
		if p.y[0] < ymin:
			ymin = p.y[0]
# 
tw = xmax - xmin
th = ymax - ymin
rw = mywidth / tw
rh = myheight / th
print(tw,th,rw,rh)	

switch = 0

sep = [[],[],[],[],[],[],[],[],[],[],[]]

black = 1
red = 2
green = 3
blue = 4
yellow = 7
orange = 8

penstart = 2
penend = 4
pencolors = [1,2,3,4]
penidx = 0
# pen = pencolors[1]	

for p in IG:
	if (p._name == 'PU' or p._name == 'PD'):
		tmp = CoordinateArray( [ ( sl + p.x[0] * rw, sb + p.y[0] * rh ) ] )
		p.xy = tmp		
 		# c.append(p)
		switch += 1
		if (switch >= 4) and (p._name != 'PD'):
			switch = 0
			if penidx < len(pencolors)-1:
				penidx += 1
			else:
				penidx = 0
			
		sep[ pencolors[penidx] ].append(p)	
			# c.append(SP(pen))

# sort by pen color
for i, x in enumerate(sep):
	c.append(SP(i))
	for com in x:
		c.append(com)
		


# for i, x in enumerate(c):
# 	if x._name =="SP":
# 		pen = x.pen
# 		tn = i+1
# 		nc = c[tn]
# 		while nc._name != "SP":
# 			sep[pen].append(nc)
# 			
# 		if x.pen == 1:
# 			
# 			# collect all until new pen select
# 			print(x.format)


		# print(p.format)


# 
# plotter.clear()
# io.view(c)	
plotter.write( c )
 # c )
