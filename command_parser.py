from coordinate_parser import CoordinateParser
from serial_command_retriever import SerialCommandRetriever
from wifi_command_retriever import WifiCommandRetriever
from geometry import dot, cross, norm, multi, minus, plus

import serial
import math

SS_POLYGON_MODE = 0
SS_CURVE_MODE = 1
SS_SCULPT_MODE = 2
SS_EXTRUDE_MODE = 3

SAMPLE_SIZE = 5
NEARBY_THRESHOLD = 0.05
EC_CANDIDATE_THRESHOLD = 0.05

PORT = '/dev/tty.usbmodem1413'
HPORT = '/dev/cu.usbserial-A602KCO2'
WIFI_IP = '18.189.110.81'
WIFI_PORT = 23

EPSILON = 1e-9
INFINITY = 1e10

class CommandParser(object):

  def __init__(self, side, height):
    super(CommandParser, self).__init__()

    self.side = side
    self.height = height
    self.mode = SS_POLYGON_MODE
    self.last_point = (0, 0, 0)
    self.current_points = []
    self.current_sizes = []
    self.polygons = []
    self.curves = []
    self.lastClick = 0
    self.solids = []
    self.extrusions = []
    self.samples = []
    self.curve_tracing = False
    self.sculpting = False
    self.nearby_point = None
    self.extruding = False
    self.extruding_polygon = None
    self.extruding_origin = None
    self.extruding_candidate = None
    # self.command_retriever = SerialCommandRetriever(PORT)
    self.command_retriever = WifiCommandRetriever(WIFI_IP, WIFI_PORT)
    self.handle = SerialCommandRetriever(HPORT)
    self.brush_radius=0.05

    self.das = []
    self.dbs = []
    self.dcs = []

    self.coordinate_parser = CoordinateParser(side, height)

  def __parse_point(self, rp):
    rp = (float(rp[0]), float(rp[1]), float(rp[2]))
    p = (rp[0] / 1000.0, rp[1] / 1000.0, rp[2] / 1000.0)
    return self.coordinate_parser.parse(float(p[0]), float(p[1]), float(p[2]))

  def fetch_and_process(self):
    print(len(self.polygons))
    commands = self.command_retriever.fetch()
    hcommands = self.handle.fetch()

    for c in commands:
      print('[LOG] ' + c)

    for c in hcommands:
      print('[HLOG] ' + c)

    self.handle.clear()

    for c in hcommands:
      self.hprocess(c)
    for c in commands:
      self.process(c)

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

  def __calculate_point_triangle_distance(self, point, triangle):
    def orientation(point, a, b, normal):
      sig_norm = cross(minus(b, a), normal)
      return dot(sig_norm, minus(point, a))

    a, b, c = triangle
    normal = cross(minus(c, a), minus(b, a))
    unormal = multi(1.0 / norm(normal), normal)
    d = abs(dot(minus(point, a), unormal))

    o1 = orientation(point, a, b, normal)
    o2 = orientation(point, b, c, normal)
    o3 = orientation(point, c, a, normal)

    return (o1 >= -EPSILON and o2 >= -EPSILON and o3 >= -EPSILON), d

  def __calculate_point_polygon_distance(self, point, polygon):
    i1 = 0
    within, dist = False, INFINITY

    for i2 in range(1, len(polygon) - 1):
      i3 = i2 + 1
      triangle = [polygon[i1], polygon[i2], polygon[i3]]
      w, d = self.__calculate_point_triangle_distance(point, triangle)

      if w:
        within = True
        if d < dist:
          dist = d

    return within, dist

  def __fetch_extruding_candidate(self, point):
    minp = None
    mind = INFINITY

    for p in self.polygons:
      within, d = self.__calculate_point_polygon_distance(point, p)

      if within:
        if d < mind:
          mind = d
          minp = p

    if mind <= EC_CANDIDATE_THRESHOLD:
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

  def hprocess(self, command):
    parts = command.split()
    state=int(parts[0])
    angle=int(parts[1])
    clicked=int(parts[2])
    nclick=int(parts[3])
    if clicked>self.lastClick:
      self.lastClick=clicked
    if state==0:
      self.brush_radius=0.01+0.05*(angle/50.0)
      
  def calculate_extrusion_extra_polygons(self, e):
    polys = []
    poly, vec = e
    new_poly = list(map(lambda v: plus(v, vec), poly))

    polys.append(new_poly)

    for i in range(len(poly)):
      polys.append([poly[i - 1], poly[i], new_poly[i], new_poly[i - 1]])

    return polys

  def process(self, command):
    parts = command.split()

    type = parts.pop(0)

    if type == 'point':
      point = self.__parse_point(parts)

      if point == None:
        print('[ERROR] Invalid point. ')
        print('        parts')
      else:
        self.last_point = self.__insert_and_fetch_sample(parts)

        if self.mode == SS_POLYGON_MODE:
          np = self.__fetch_nearby_point(self.last_point)
          if np:
            self.nearby_point = np
            self.command_retriever.send('n')
          else:
            self.nearby_point = None
            self.command_retriever.send('x')

        if self.mode == SS_EXTRUDE_MODE:
          ec = self.__fetch_extruding_candidate(self.last_point)
          if ec:
            self.extruding_candidate = ec
            self.command_retriever.send('n')
          else:
            self.extruding_candidate = None
            self.command_retriever.send('x')

        if self.mode == SS_CURVE_MODE:
          self.current_points.append(point)
        elif self.mode ==SS_SCULPT_MODE:
          self.current_points.append(point)
          self.current_sizes.append(self.brush_radius)
    elif type == 'doubleclick':
      if self.mode == SS_POLYGON_MODE:
        if self.nearby_point:
          self.last_point = self.nearby_point
          self.current_points.append(self.last_point)
    elif type == 'click':
      if self.mode == SS_POLYGON_MODE:
        self.current_points.append(self.last_point)
      elif self.mode==SS_CURVE_MODE:
        if self.curve_tracing:
          if len(self.current_points) >= 2:
            self.curves.append(self.current_points)
        self.curve_tracing = (not self.curve_tracing)
      elif self.mode==SS_SCULPT_MODE:
        if self.sculpting:
          if len(self.current_points) >= 2:
            self.solids.append((self.current_points,self.current_sizes))
        self.sculpting = (not self.sculpting )
        self.current_points=[]
        self.current_sizes=[]
      elif self.mode == SS_EXTRUDE_MODE:
        if self.extruding:
          self.extrusions.append((self.extruding_polygon, minus(self.last_point, self.extruding_origin)))

          eps = self.calculate_extrusion_extra_polygons(self.extrusions[-1])
          for p in eps:
            self.polygons.append(p)

          self.extruding = False
        else:
          if self.extruding_candidate:
            self.extruding_origin = self.last_point
            self.extruding_polygon = self.extruding_candidate
            self.extruding = True
    elif type == 'hold':
      if self.mode == SS_POLYGON_MODE:
        if len(self.current_points) >= 3:
          self.polygons.append(self.current_points[:])
        self.current_points = []
    elif type == 'mode':
      self.current_points = []
      self.current_sizes = []
      self.curve_tracing = False
      self.sculpting = False
      if parts[0] == 'polygon':
        self.mode = SS_POLYGON_MODE
      elif parts[0] == 'curve':
        self.mode = SS_CURVE_MODE
      elif parts[0] == 'sculpt':
        self.mode = SS_SCULPT_MODE
      elif parts[0] == 'extrude':
        self.mode = SS_EXTRUDE_MODE
        self.extruding = False
      else:
        print('[ERROR] Invalid mode. ')
