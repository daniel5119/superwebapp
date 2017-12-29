#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import datetime

# HTML to send to browser
html = """<!DOCTYPE html>
<html>
<head> <title>Moon State</title> </head>
<h2>Moon State Display</h2>
<h3>Distelli App Pipeline Test</h3>
<p>This App simply displays the state of the moon currently, based on a USNO API.</p>
<p><strong>Moon State:</strong><br>
The moon is a {0} moon on {1}.</p>
</html>
"""

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = html.format(phase(), str(datetime.date.today()))
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

def phase():
  datestr = datetime.date.today().strftime('%m/%d/%Y')
  url = "http://api.usno.navy.mil/rstt/oneday?date=" + datestr + "&coords=54.59,-5.93&tz=0"
  r = requests.get(url).json()
  if 'curphase' in r:
      mnph = r['curphase']
  else:
      mnph = r['closestphase']['phase']
  return mnph

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('', 80)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()
