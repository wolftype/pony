from pony import *

p = Print ()

filename = "-i hpgl/p2.hpgl"

num = 50

for i in range (1, num):
    #[0,1)
    scl = float(i)/float(num)
    #reset
    args = "-r -l "
    #select pen
    args += "-sp 8 "
    #draw border
    args += "-b "
    #scale
    args += "-sr " + str(scl) + " " + str(scl)+ " "
    #line type
    if (i % 5 ):
        args += "-lt 6 " + str(scl * 5) + " "
        args += "-fs " + str(i % 5) + " "
        if (i % 2 == False):
            args += "-t " + str(scl) + " -st .2 .2 "
    else:
        args += "-lt 2 " + str(100) + " "
        args += "-fs " + str(8) + " "
        args += "-t " + str(scl) + " -st .4 .2 "
    #set force

    #send to printer
    args += "-p"
    p.parse(args.split());

p.printer.instantiate()
p.send()
