################################################################################
#
# Bare Conductive Pi Cap
# ----------------------
#
# datastream-osc.py - streams capacitive sense data from MPR121 to OSC endpoint
#
# Written for Raspberry Pi.
#
# Bare Conductive code written by Szymon Kaliski and Tom Hartley.
#
# This work is licensed under a MIT license https://opensource.org/licenses/MIT
#
# Copyright (c) 2016, Bare Conductive
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#################################################################################

from time import sleep
import signal, sys, getopt, liblo, MPR121
import argparse

try:
  sensor = MPR121.begin()
except Exception as e:
  print (e)
  sys.exit(1)

# how many electrodes we have
electrodes_range = range(12)

# this is the touch threshold - setting it low makes it more like a proximity trigger default value is 40 for touch
touch_threshold = 40

# this is the release threshold - must ALWAYS be smaller than the touch threshold default value is 20 for touch
release_threshold = 20

# set the thresholds
sensor.set_touch_threshold(touch_threshold)
sensor.set_release_threshold(release_threshold)

# handle ctrl+c gracefully
def signal_handler(signal, frame):
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def setupargs():  
  parser = argparse.ArgumentParser(description="Sends Pi Cap readings through OSC - MUST be run as root.",add_help=False)
  parser.add_argument('-h','--host', nargs='?', metavar='CMD', dest = 'host', type=str, default='127.0.0.1', 
                      help='host address, defaults to 127.0.0.1')
  parser.add_argument('-p','--port', nargs='?', metavar='CMD', dest = 'port', type=int, default=3000, 
                      help='port on which to send, defaults to 3000')
  parser.add_argument('--help', action='help', default=argparse.SUPPRESS, help=argparse._('show this help message and exit'))
                      
  
  return parser.parse_args()

args = setupargs()

# setup OSC
address = liblo.Address(args.host, args.port)

while True:
  bundle = liblo.Bundle()

  if sensor.touch_status_changed():
    sensor.update_touch_data()

  sensor.update_baseline_data()
  sensor.update_filtered_data()

  # touch values
  touch = liblo.Message("/touch")
  data_array = []
  for i in electrodes_range:
    # get_touch_data returns boolean values: True or False
    # we need to turn them into ints first: 1 or 0
    # and then into string: "1" or "0" so we can display them
    touch.add(int(sensor.get_touch_data(i)))
  bundle.add(touch)

  # touch thresholds
  tths = liblo.Message("/tths")
  for i in electrodes_range:
    tths.add(touch_threshold)
  bundle.add(tths)

  # release threshold
  rths = liblo.Message("/rths")
  for i in electrodes_range:
    rths.add(release_threshold)
  bundle.add(rths)

  # filtered values
  fdat = liblo.Message("/fdat")
  for i in electrodes_range:
    fdat.add(sensor.get_filtered_data(i))
  bundle.add(fdat)

  # baseline values
  bval = liblo.Message("/bval")
  for i in electrodes_range:
    bval.add(sensor.get_baseline_data(i))
  bundle.add(bval)

  # value pairs
  diff = liblo.Message("/diff")
  for i in electrodes_range:
    diff.add(sensor.get_baseline_data(i) - sensor.get_filtered_data(i))
  bundle.add(diff)

  # send our bundle to given address
  liblo.send(address, bundle)

  # a little delay so that we don't just sit chewing CPU cycles
  sleep(0.01)
