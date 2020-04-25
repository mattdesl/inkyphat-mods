#!/usr/bin/python
from PIL import Image, ImageDraw
import random
from inky_mod import InkyPHAT
import urllib2
import json
import sched
import time
import re
import cStringIO

display = InkyPHAT("black")
scheduler = sched.scheduler(time.time, time.sleep)

ip = '192.168.1.65'
port = '3000'
url = 'http://%s:%s/' % (ip, port)


seconds_interval = 0
first_run = True

def reindex_image (other):
  rgb_im = other.convert('RGB')
  img = Image.new("P", (display.WIDTH, display.HEIGHT))
  for x in range(display.WIDTH):
    for y in range(display.HEIGHT):
      (r, g, b) = rgb_im.getpixel((x, y))
      color = display.WHITE if r > 127 else display.BLACK
      img.putpixel((x, y), color)
  return img

def render(img, bg):
  global first_run
  if first_run:
    first_run = False
    print "Resetting Screen"
    display.reset(display.BLACK)
  print "Image Size %s x %s" % img.size
  img = reindex_image(img)
  display.set_image(img)
  display.set_border(bg)
  display.fast_show(bg)

def task(_scheduler=None):
  img = None
  bg = display.BLACK
  try:
    print 'Fetching new image from %s' % url
    res = urllib2.urlopen(url)
    meta = json.load(res)
    print 'Background: %s' % meta['background']
    if meta['background'] == 'white':
      bg = display.WHITE
    base64Data = meta['data']
    image_data = re.sub('^data:image/.+;base64,', '', base64Data).decode('base64')
    img = Image.open(cStringIO.StringIO(image_data))
  except Exception as err:
    print str(err)

  if img is not None:
    maxSize = 128 * 256
    if img.size[0] * img.size[1] > maxSize:
      print "Error: Image size is too large"
    else:
      render(img, bg)

  if _scheduler is not None:
    scheduler.enter(seconds_interval, 1, task, (_scheduler,))

task()
scheduler.enter(seconds_interval, 1, task, (scheduler,))
scheduler.run()