#!/bin/bash

#note output gl2ps with shaded output on (as .eps file)

DIRECTORY=`dirname $1`
TARGET=`basename $1|cut -d'.' -f1 | sed -e "s|/|_|g"`

echo converting $1 to hpgl/$TARGET.hpgl
pstoedit $1 hpgl/$TARGET.hpgl -f "hpgl:-penplotter -filltype 'FT4'"
view_hpgl_file.py hpgl/$TARGET.hpgl
