# 10170,7840;
# http://cmc.music.columbia.edu/chiplotle/manual/chapters/api/hpgl.html

from chiplotle import *	
plotter = instantiate_plotters()[0]
#plotter = plottertools.instantiate_virtual_plotter()
import math

paper_width = 10170
paper_height = 7840

image_width = 3000;
image_height = 3800;

border_width = ((paper_width - image_width) / 2.0) - 600
border_height = ((paper_height - image_height) / 2.0) - 300

num_lines = 20.0

height_unit = image_height / num_lines;

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

commands = []

commands.append(IN())
commands.append(SP(2))

for j in range (0,8):
	commands.append(FS(5))
	commands.append(LT(j % 6))

	for i in range (0,int(num_lines)):
		la = CoordinateArray ([(border_width, border_height + i/num_lines * image_height + j/8.0 * height_unit)])
		lb = CoordinateArray ([(border_width + image_width, border_height + i/num_lines * image_height + j/8.0 * height_unit)])
		commands.append(PU(la))	
		commands.append(CI(20))
		commands.append(PU(lb))	
		commands.append(CI(10))

commands.append(SP(0))
plotter.write(commands)
