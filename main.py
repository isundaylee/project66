from coordinate_parser import CoordinateParser
from screen_controller import ScreenController

import serial

parser = CoordinateParser(5, 7)

# PORT = '/dev/tty.usbmodem1413'

# data = ''

# with serial.Serial(PORT, baudrate=9600, timeout=0.01) as s:
#   while True:
#     if s.inWaiting() > 0:
#       data = data + s.read(16)
#       loc = data.find("\n")

#       if loc != -1:
#         print data[0:loc]
#         data = data[loc + 1:]

# for i in range(20):
#   p = parser.generate_random_point()

#   print (' '.join(('point', str(p[0]), str(p[1]), str(p[2]))))

controller = ScreenController(0.65, 0.8)
controller.run()