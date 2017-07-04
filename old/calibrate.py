from chiplotle import *	
plotter = instantiate_plotters()[0]
#plotter = plottertools.instantiate_virtual_plotter()
import math

paper_width = 10170
paper_height = 7840

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

commands = []

commands.append(IN())
commands.append(SP(3))
commands.append(FS(1))

for i in range (0,20):
	la = CoordinateArray ([(i/20.0 * paper_width, 0)])
	lb = CoordinateArray ([(i/20.0 * paper_width, paper_height)])
	commands.append(PU(la))
	#commands.append(PD(lb))
	print(la, lb)

plotter.write (commands)