#!/usr/bin/python
from PIL import Image, ImageDraw
import random
from inky_mod import InkyPHAT

display = InkyPHAT("black")

def get_filled_image (color):
  img = Image.new("P", (display.WIDTH, display.HEIGHT))
  for x in range(display.WIDTH):
    for y in range(display.HEIGHT):
      img.putpixel((x, y), color)
  return img

def reindex_image (other):
  rgb_im = other.convert('RGB')
  img = Image.new("P", (display.WIDTH, display.HEIGHT))
  for x in range(display.WIDTH):
    for y in range(display.HEIGHT):
      (r, g, b) = rgb_im.getpixel((x, y))
      color = display.WHITE if r > 127 else display.BLACK
      img.putpixel((x, y), color)
  return img

colors = [ display.BLACK, display.WHITE ]

def run (colors, type = None):
  [ bg, fg ] = colors
  img = get_filled_image(bg)
  [ width, height ] = img.size

  draw = ImageDraw.Draw(img)

  def ray ():
    start = (
      random.random() * width,
      random.random() * height
    )

    end = (
      random.random() * width,
      random.random() * height
    )

    draw.line(start + end, width=4, fill=fg)

  for x in range(10):
    ray()

  # if type is not None:
  display.set_border(bg)
  display.set_image(img)
  display.fast_show(bg)
  # display.fast_show(bg)
  # if bg == display.BLACK:
  #   display.show('black-bg')
  # else:
  #   display.show('white-bg')
  # if bg == display.BLACK:
  #   display.show('clear-black')
  #   display.show('black-to-image')
  # else:
  #   display.show('clear-white')
  #   display.show('white-to-image')


# if random.random() < 0.5:
# colors.reverse()

colorList = [
  [ display.BLACK, display.WHITE ],
  [ display.WHITE, display.BLACK ],
  [ display.BLACK, display.WHITE ],
  [ display.WHITE, display.BLACK ],
  [ display.WHITE, display.BLACK ],
  [ display.BLACK, display.WHITE ]
]

# img = get_filled_image(display.BLACK)
# display.set_border(display.BLACK)
# display.set_image(img)
# display.show()

# img = get_filled_image(display.WHITE)
# display.set_border(display.WHITE)
# display.set_image(img)
# display.show()

display.reset(colorList[0][0])

for colors in colorList:
  print "Running!"
  run(colors)
  # if random.random() < 0.5:
  # colors.reverse()


# run(colors)
# colors.reverse()
# run(colors)
# run(colors, 'clear-black')
# run(colors, 'black-to-white')

# display.show('black-to-white')
# display.show()