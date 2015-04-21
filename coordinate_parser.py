import math
import random

from sympy.solvers import solve
from sympy import Symbol

class CoordinateParser(object):
  def __init__(self, height):
    super(CoordinateParser, self).__init__()
    self.height = float(height)

  def parse(self, pa, pb, pc, da, db, dc):
    h = self.height

    x = (-db ** 2 * pa[1] + dc ** 2 * pa[1] + pa[1] * pb[0] ** 2 + da ** 2 * pb[1] - dc ** 2 * pb[1] - pa[0] ** 2 * pb[1] - pa[1] ** 2 * pb[1] + pa[1] * pb[1] ** 2 - pa[1] * pc[0] ** 2 + pb[1] * pc[0] ** 2 - da ** 2 * pc[1] + db ** 2 * pc[1] + pa[0] ** 2 * pc[1] + pa[1] ** 2 * pc[1] - pb[0] ** 2 * pc[1] - pb[1] ** 2 * pc[1] - pa[1] * pc[1] ** 2 + pb[1] * pc[1] ** 2)/(2 * (pa[1] * pb[0] - pa[0] * pb[1] - pa[1] * pc[0] + pb[1] * pc[0] + pa[0] * pc[1] - pb[0] * pc[1]))

    y = (db ** 2 * pa[0] - dc ** 2 * pa[0] - da ** 2 * pb[0] + dc ** 2 * pb[0] + pa[0] ** 2 * pb[0] + pa[1] ** 2 * pb[0] - pa[0] * pb[0] ** 2 - pa[0] * pb[1] ** 2 + da ** 2 * pc[0] - db ** 2 * pc[0] - pa[0] ** 2 * pc[0] - pa[1] ** 2 * pc[0] + pb[0] ** 2 * pc[0] + pb[1] ** 2 * pc[0] + pa[0] * pc[0] ** 2 - pb[0] * pc[0] ** 2 + pa[0] * pc[1] ** 2 - pb[0] * pc[1] ** 2)/(2 * (pa[1] * pb[0] - pa[0] * pb[1] - pa[1] * pc[0] + pb[1] * pc[0] + pa[0] * pc[1] - pb[0] * pc[1]))

    delta = dc ** 2 - pc[0] ** 2 - pc[1] ** 2 + 2 * pc[0] * x - x ** 2 + 2 * pc[1] * y - y ** 2

    if delta < 0:
      return None
    else:
      z = h - math.sqrt(delta)
      return (x,y,z)

  def parse_old(self, da, db, dc):
    l = self.side
    h = self.height

    delta = - da ** 4 * l ** 2 + da ** 2 * db ** 2 * l ** 2 - db ** 4 * l ** 2 \
            + da ** 2 * dc ** 2 * l ** 2 + db ** 2 * dc ** 2 * l ** 2 - dc ** 4 * l ** 2 \
            + da ** 2 * l ** 4 + db ** 2 * l ** 4 + dc ** 2 * l ** 4 - l ** 6

    if delta < 0:
      return None
    else:
      x = (da ** 2 - dc ** 2 + l ** 2) / (2 * l)
      y = (da ** 2 - 2 * db ** 2 + dc ** 2 + l ** 2) / (math.sqrt(12) * l)
      z = (3 * h * l ** 2 - math.sqrt(3 * delta)) / (3 * l ** 2)

      return (x, y, z)

  def __distance(self, p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2])** 2)

  def generate_random_point(self):
    x = random.random() * self.side
    y = random.random() * self.side
    z = random.random() * self.height

    p = (x, y, z)

    return (
      self.__distance(p, (0, 0, self.height)),
      self.__distance(p, (self.side, 0, self.height)),
      self.__distance(p, (0.5 * self.side, math.sqrt(0.75) * self.side, self.height)),
    )


