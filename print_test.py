from pony import *

p = Print ()

filename = "-i hpgl/p2.hpgl"

num = 100
for i in range (1, num):
    scl = float(i)/float(num)
    args = "-b -sr " + str(scl) + " " + str(scl) + " -lt 3 " + str(scl) + " -fs " + str(int(scl*8)) + " -p"
    p.parse(args.split());

p.printer.instantiate()
p.send()
