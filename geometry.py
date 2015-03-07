import math

def dot(a, b):
  return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def cross(a, b):
  return (
      a[1] * b[2] - a[2] * b[1],
      a[2] * b[0] - a[0] * b[2],
      a[0] * b[1] - a[1] * b[0]
    )

def norm(a):
  return math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)

def multi(k, a):
  return (k * a[0], k * a[1], k * a[2])


def minus(a, b):
  return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def plus(a, b):
  return (a[0] + b[0], a[1] + b[1], a[2] + b[2])