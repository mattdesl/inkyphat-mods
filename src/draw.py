#!/usr/bin/env python

import argparse
from PIL import Image
from inky import InkyPHAT

print("""Inky pHAT/wHAT: Logo
Displays the Inky pHAT/wHAT logo.
""")

type = "phat"
colour = "black"

inky_display = InkyPHAT(colour)
inky_display.set_border(inky_display.BLACK)

img = Image.open("assets/InkypHAT-212x104-bw.png")

inky_display.set_image(img)
inky_display.show()