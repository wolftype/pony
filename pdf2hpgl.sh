#!/bin/bash

DIRECTORY=`dirname $1`
TARGET=`basename $1|cut -d'.' -f1 | sed -e "s|/|_|g"`

echo converting $1 to hpgl/$TARGET.hpgl
pstoedit $1 hpgl/$TARGET.hpgl -f hpgl:-penplotter
view_hpgl_file.py hpgl/$TARGET.hpgl
