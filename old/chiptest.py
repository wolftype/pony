# 10170,7840;
# http://cmc.music.columbia.edu/chiplotle/manual/chapters/api/hpgl.html

from chiplotle import *

plotter = instantiate_plotters( )[0]
plotter.select_pen(1)

height = 2000
width = 1000
offset = 200

for j in range (0,8):
	plotter.write(hpgl.FS(j))
	for i in range (0,10):
		plotter.pen_up([(5090,3720 + i/10.0 * height + j/8.0 * offset)])	
		plotter.pen_down([(5090 + width,3720 + i/10.0 * height+j/8.0 * offset)])

plotter.select_pen(0)
