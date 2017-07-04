from chiplotle import *	

plotter = instantiate_plotters()[0]

import math
S = shapes
SP = hpgl.SP
LT = hpgl.LT
SM = hpgl.SM
PU = hpgl.PU
PA = hpgl.PA
PD = hpgl.PD
c = []
# c.append(SM('o'))
# c.append(hpgl.PA([(0,0)]))
# c.append(hpgl.PD())
# c.append(hpgl.PA([(1000,1000)]))
# c.append(hpgl.PU())
# c.append(hpgl.PA([(500,1000)]))
# c.append(hpgl.LB("hello"))

c.append(hpgl.SP(0))

ng = shapes.group([])
com = []
coords = [ (0,100), (100,100), (100,-100), (0,-100), (0,100)  ]
weights = [.2,1,0, 1,0]
# 
for weight in range(0,5,1):

	# print(f)
	a = mathtools.bezier_interpolation(coords,50,weights)
	t = hpgltools.convert_coordinates_to_hpgl_absolute_path(a)
	# transforms.offset(a,(weight*400,0))
	for x in t:
		# print(x)
		c.append(x)
		# c.append(SP(1))
	# c.append(t)
c[0] = SP(1)

for x in c:
	print(x)
# 
for x in range(0,5,1):
	a = shapes.cross(x*10, 20)
	transforms.rotate(a, x)
	transforms.offset(a, (x*100,0))
	ng.append(a)

for x in range(0,5,1):
	a = shapes.fan(x*10, 0,math.pi*2, 20)
	transforms.offset(a, (x*200,0))
	ng.append(a)

for x in range(0,5,1):
	a = shapes.line( (0,0), (300,100))
	transforms.offset(a, (0,x*10))
	ng.append(a)

for x in range(0,5,1):
	a = S.arc_ellipse( x * 100, 100, 0,math.pi*2)
	ng.append(a)
	t = shapes.annotation(a)
	print(t.width, t.height)
# io.save_hpgl(c, "hpgl_save_test.plt")
io.view(c)	
# plotter.write(ng)