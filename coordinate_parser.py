import math

from sympy.solvers import solve
from sympy import Symbol

class CoordinateParser(object):
  def __init__(self, side, height):
    super(CoordinateParser, self).__init__()
    self.side = side
    self.height = height

  def parse(self, da, db, dc):
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    z = Symbol('z', real=True)

    eq1 = (self.height - z) ** 2 + x ** 2 + y ** 2 - da ** 2
    eq2 = (self.height - z) ** 2 + (0.5 * self.side - x) ** 2 + (math.sqrt(0.75) * self.side - y) ** 2 - db ** 2
    eq3 = (self.height - z) ** 2 + (self.side - x) ** 2 + y ** 2 - dc ** 2

    raw_sols = solve([eq1, eq2, eq3])
    sols = filter(lambda s:
      (s[z] > 0 and s[z] < self.height),
      raw_sols
    )

    if len(sols) > 0:
      return (sols[0][x], sols[0][y], sols[0][z])
    else:
      return None