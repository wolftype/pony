from __future__ import print_function
from PIL import Image

im = Image.open("cone.png")

print(im.format, im.size, im.mode)
