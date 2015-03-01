from coordinate_parser import CoordinateParser

import serial
import math

SS_POLYGON_MODE = 0
SS_CURVE_MODE = 1

SAMPLE_SIZE = 5
NEARBY_THRESHOLD = 0.05

PORT = '/dev/tty.usbmodem1413'

INTERRUPT_COMMANDS = [
  "click\n",
  "doubleclick\n",
  "hold\n",
  "mode polygon\n",
  "mode curve\n",
]

class CommandParser(object):

  def __init__(self, side, height):
    super(CommandParser, self).__init__()

    self.side = side
    self.height = height
    self.mode = SS_POLYGON_MODE
    self.last_point = (0, 0, 0)
    self.current_points = []
    self.polygons = []
    self.curves = []
    self.samples = []
    self.curve_tracing = False
    self.nearby_point = None

    self.das = []
    self.dbs = []
    self.dcs = []

    self.serial = serial.Serial(PORT, baudrate=9600, timeout=0.01)
    self.data = ''

    self.coordinate_parser = CoordinateParser(side, height)

  def __parse_point(self, rp):
    rp = (float(rp[0]), float(rp[1]), float(rp[2]))
    p = (rp[0] / 1000.0, rp[1] / 1000.0, rp[2] / 1000.0)
    print self.coordinate_parser.parse(float(p[0]), float(p[1]), float(p[2]))
    return self.coordinate_parser.parse(float(p[0]), float(p[1]), float(p[2]))

  def fetch_and_process(self):
    if self.serial.inWaiting() > 0:
      self.data = self.data + self.serial.read(16)

      for c in INTERRUPT_COMMANDS:
        if c in self.data:
          print(c)
          self.process(c)
          self.data = self.data.replace(c, "")

      loc = self.data.find("\n")

      if loc != -1:
        print self.data[0:loc]
        self.process(self.data[0:loc])
        self.data = self.data[loc + 1:]

  def __extract_sample(self, samples):
    if len(samples) == 1:
      return samples[0]
    elif len(samples) <= 3:
      return 1.0 * sum(samples) / len(samples)
    else:
      return (1.0 * sum(samples) - max(samples) - min(samples)) / (len(samples) - 2)

  def __previous_vertices(self):
    res = []

    for poly in self.polygons:
      for p in poly:
        res.append(p)

    return res

  def __fetch_nearby_point(self, point):
    mind = 1000000000
    minp = None

    for p in self.__previous_vertices():
      d = math.sqrt((point[0] - p[0]) ** 2 + (point[1] - p[1]) ** 2 + (point[2] - p[2]) ** 2)

      if d < mind:
        mind = d
        minp = p

    if mind <= NEARBY_THRESHOLD:
      return minp
    else:
      return None

  def __insert_and_fetch_sample(self, p):
    self.das.append(float(p[0]))
    self.dbs.append(float(p[1]))
    self.dcs.append(float(p[2]))

    if len(self.das) > SAMPLE_SIZE:
      self.das.pop(0);
      self.dbs.pop(0);
      self.dcs.pop(0);

    da = self.__extract_sample(self.das)
    db = self.__extract_sample(self.dbs)
    dc = self.__extract_sample(self.dcs)

    return self.__parse_point((da, db, dc))

  def process(self, command):
    parts = command.split()

    type = parts.pop(0)

    if type == 'point':
      point = self.__parse_point(parts)

      if point == None:
        print('[ERROR] Invalid point. ')
        print parts
      else:
        self.last_point = self.__insert_and_fetch_sample(parts)

        np = self.__fetch_nearby_point(self.last_point)

        if np:
          self.nearby_point = np
          self.serial.write("n")
          print('#' * 80)
        else:
          self.nearby_point = None
          self.serial.write('x')

        if self.mode == SS_CURVE_MODE:
          self.current_points.append(point)
    elif type == 'doubleclick':
      if self.mode == SS_POLYGON_MODE:
        if self.nearby_point:
          self.last_point = self.nearby_point
          self.current_points.append(self.last_point)
    elif type == 'click':
      if self.mode == SS_POLYGON_MODE:
        self.current_points.append(self.last_point)
      else:
        if self.curve_tracing:
          if len(self.current_points) >= 2:
            self.curves.append(self.current_points)
        self.curve_tracing = (not self.curve_tracing)
    elif type == 'hold':
      if self.mode == SS_POLYGON_MODE:
        if len(self.current_points) >= 3:
          self.polygons.append(self.current_points)
        self.current_points = []
    elif type == 'mode':
      self.current_points = []
      self.curve_tracing = False
      if parts[0] == 'polygon':
        self.mode = SS_POLYGON_MODE
      elif parts[0] == 'curve':
        self.mode = SS_CURVE_MODE
      else:
        print('[ERROR] Invalid mode. ')
