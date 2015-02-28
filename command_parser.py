from coordinate_parser import CoordinateParser

SS_POLYGON_MODE = 0
SS_CURVE_MODE = 1

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
    self.curve_tracing = False

    self.coordinate_parser = CoordinateParser(side, height)

  def __parse_point(self, p):
    return self.coordinate_parser.parse(float(p[0]), float(p[1]), float(p[2]))

  def process(self, command):
    parts = command.split()

    type = parts.pop(0)

    if type == 'point':
      point = self.__parse_point(parts)

      if point == None:
        print('[ERROR] Invalid point. ')
        print parts
      else:
        self.last_point = point

        if self.mode == SS_CURVE_MODE:
          self.current_points.append(point)
    elif type == 'click':
      if self.mode == SS_POLYGON_MODE:
        self.current_points.append(self.last_point)
      else:
        if self.curve_tracing:
          self.curves.append(self.current_points)
        self.curve_tracing = (not self.curve_tracing)
    elif type == 'hold':
      if self.mode == SS_POLYGON_MODE:
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
