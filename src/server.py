#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from io import BytesIO
import time

haspHAT = False
display = None
last_image = None

try:
  from PIL import Image
  from inky import InkyPHAT
  haspHAT = True

  display = InkyPHAT("black")
except:
  pass

print "has inkypHAT %s" % haspHAT

PORT_NUMBER = 42371

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

def invert_image (paletteImage):
  img = Image.new("P", (display.WIDTH, display.HEIGHT))
  for x in range(display.WIDTH):
    for y in range(display.HEIGHT):
      p = paletteImage.getpixel((x, y))
      color = display.BLACK if p == display.WHITE else display.WHITE
      img.putpixel((x, y), color)
  return img

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
  def __init__(self, request, client_address, server):
    BaseHTTPRequestHandler.__init__(self, request, client_address, server)

  def send_error(self, error = "Error handling request"):
    self.send_response(400)
    self.send_header('Content-type','text/plain')
    self.end_headers()
    self.wfile.write(error)

  def do_POST(self):
    global last_image
    if self.path.endswith("/image"):
      content_length = int(self.headers['content-length'])
      if content_length > 16000:
        return self.send_error("Content is too large, over 16kb")
      post_data = self.rfile.read(content_length)

      bytes = BytesIO(post_data)
      img = Image.open(bytes)
      if img:
        width, height = img.size
        if width == 104 and height == 212:
          img = img.rotate(90)
          width, height = img.size
        if width != 212 or height != 104:
          return self.send_error("Image must be 212 by 104 pixels")
      if display is not None and img is not None:
        img = reindex_image(img)
        last_image = img
        display.set_image(img)
        display.show()
    elif self.path.endswith("/invert"):
      if display is not None and last_image is not None:
        img = invert_image(last_image)
        last_image = img
        display.set_image(img)
        display.show()
    elif self.path.endswith("/white"):
      if display is not None:
        last_image = None
        img = get_filled_image(display.WHITE)
        display.set_border(display.WHITE)
        display.set_image(img)
        display.show()
    elif self.path.endswith("/black"):
      if display is not None:
        last_image = None
        img = get_filled_image(display.BLACK)
        display.set_border(display.BLACK)
        display.set_image(img)
        display.show()
    elif self.path.endswith("/clean"):
      if display is not None:
        cycles = 3
        colours = (display.RED, display.BLACK, display.WHITE)
        colour_names = ("white", "black", "white")
        img = Image.new("P", (display.WIDTH, display.HEIGHT))
        for i in range(cycles):
          print("Cleaning cycle %i\n" % (i + 1))
          for j, c in enumerate(colours):
            print("- updating with %s" % colour_names[j])
            display.set_border(c)
            for x in range(display.WIDTH):
              for y in range(display.HEIGHT):
                img.putpixel((x, y), c)
            display.set_image(img)
            display.show()
            time.sleep(1)

    self.send_response(200)
    self.send_header('Content-type','text/plain')
    self.end_headers()
    # Send the html message
    self.wfile.write("OK")
    return

try:
  #Create a web server and define the handler to manage the
  #incoming request
  server = HTTPServer(('', PORT_NUMBER), myHandler)
  print 'Started httpserver on port ' , PORT_NUMBER

  #Wait forever for incoming htto requests
  server.serve_forever()
except KeyboardInterrupt:
  print '^C received, shutting down the web server'
  server.socket.close()