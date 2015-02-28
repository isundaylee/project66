import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import vispy.gloo as gloo
import vispy.app as app

import math

from command_parser import CommandParser
from coordinate_parser import CoordinateParser

GREEN = (0, 0.8, 0)
YELLOW = (1, 243.0 / 255, 71.0 / 255)
BLUE = (10.0 / 255, 124.0 / 255, 1)
RED = (1, 0, 0)

class ScreenController(object):

  sample_commands_parsed = False

  def __init__(self, side, height):
    super(ScreenController, self).__init__()
    self.command_parser = CommandParser(side, height)
    self.coordinate_parser = CoordinateParser(side, height)
    self.side = float(side)
    self.height = float(height)

  def run(self):
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
    glut.glutCreateWindow('Hello, triangles! ')
    glut.glutReshapeWindow(1280, 800)
    glut.glutReshapeFunc(self.__reshape)
    glut.glutDisplayFunc(self.__display)
    glut.glutIdleFunc(self.__idle)
    glut.glutKeyboardFunc(self.__keyboard)

    gl.glClearColor(0, 0, 0, 1)
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glEnable(gl.GL_CULL_FACE)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    # gl.glEnable(gl.GL_LIGHTING)

    self.quadric = glu.gluNewQuadric()
    glu.gluQuadricNormals(self.quadric, glu.GLU_SMOOTH)
    glu.gluQuadricTexture(self.quadric, gl.GL_TRUE)

    lightPosition = [self.side / 2, self.height / 2, self.side / 3, 0.5]
    lightColor = [BLUE[0], BLUE[1], BLUE[2], 1]

    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, lightPosition)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, lightColor)
    gl.glLightf(gl.GL_LIGHT0, gl.GL_CONSTANT_ATTENUATION, 0.01)
    gl.glLightf(gl.GL_LIGHT0, gl.GL_LINEAR_ATTENUATION, 0.05)
    gl.glColorMaterial(gl.GL_FRONT, gl.GL_DIFFUSE)
    gl.glEnable(gl.GL_COLOR_MATERIAL)
    gl.glEnable(gl.GL_LIGHT0)

    gl.glMatrixMode(gl.GL_PROJECTION)
    glu.gluPerspective(30, 1, 1, 40)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    glu.gluLookAt(
      self.side / 2, self.height / 2, 15,
      self.side / 2, self.height / 2, 0,
      0, 1, 0
    )
    gl.glPushMatrix()

    glut.glutMainLoop()

  # Translate from reallife coordinates to OpenGL coordinates
  def tr(self, x, y, z):
    return (x, z, -y)

  # Translate to reallife coordinates from OpenGL coordinates
  def fr(self, x, y, z):
    return (x, z, -y)

  def __draw_cylinder(self, p1, p2, radius=0.02):
    p1, p2 = self.tr(p1[0], p1[1], p1[2]), self.tr(p2[0], p2[1], p2[2])

    dx = float(p2[0] - p1[0])
    dy = float(p2[1] - p1[1])
    dz = float(p2[2] - p1[2])

    r = math.sqrt(dy ** 2 + dz ** 2)
    length = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    if r == 0:
      x_angle = 0
    else:
      x_angle = math.atan2(-dy / r, dz / r)
    y_angle = math.atan2(dx / length, r / length)

    gl.glPushMatrix()

    gl.glTranslatef(p1[0], p1[1], p1[2])
    gl.glRotatef(math.degrees(x_angle), 1, 0, 0)
    gl.glRotatef(math.degrees(y_angle), 0, 1, 0)

    glu.gluCylinder(self.quadric, radius, radius, length, 32, 32)

    gl.glPopMatrix()

  def __draw_sphere(self, p1, radius=0.05):
    p1 = self.tr(p1[0], p1[1], p1[2])

    gl.glPushMatrix()

    gl.glTranslatef(p1[0], p1[1], p1[2])

    glu.gluSphere(self.quadric, radius, 32, 32)

    gl.glPopMatrix()

  def __draw_polygon(self, points):
    gl.glBegin(gl.GL_LINE_LOOP)

    for rp in points:
      p = self.tr(rp[0], rp[1], rp[2])
      gl.glVertex3f(p[0], p[1], p[2])

    gl.glEnd()

  def __draw_line(self, points):
    gl.glBegin(gl.GL_LINE_STRIP)

    for rp in points:
      p = self.tr(rp[0], rp[1], rp[2])
      gl.glVertex3f(p[0], p[1], p[2])

    gl.glEnd()

  def __display(self):
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    # Drawing the axes
    gl.glBegin(gl.GL_LINES)

    # gl.glVertex3f(0.0, 0.0, 0.0)
    # gl.glVertex3f(10.0, 0.0, 0.0)

    # gl.glVertex3f(0.0, 0.0, 0.0)
    # gl.glVertex3f(0.0, 10.0, 0.0)

    # gl.glVertex3f(0.0, 0.0, 0.0)
    # gl.glVertex3f(0.0, 0.0, 10.0)

    gl.glEnd()

    # Drawing the framework

    gl.glColor4f(GREEN[0], GREEN[1], GREEN[2], 0.8)

    # Bottom triangle
    self.__draw_cylinder((0, 0, 0), (0.5 * self.side, math.sqrt(0.75) * self.side, 0))
    self.__draw_cylinder((self.side, 0, 0), (0.5 * self.side, math.sqrt(0.75) * self.side, 0))
    self.__draw_cylinder((0, 0, 0), (self.side, 0, 0))

    # Top triangle
    self.__draw_cylinder((0, 0, self.height), (0.5 * self.side, math.sqrt(0.75) * self.side, self.height))
    self.__draw_cylinder((self.side, 0, self.height), (0.5 * self.side, math.sqrt(0.75) * self.side, self.height))
    self.__draw_cylinder((0, 0, self.height), (self.side, 0, self.height))

    # Sides
    self.__draw_cylinder((0, 0, 0), (0, 0, self.height))
    self.__draw_cylinder((self.side, 0, 0), (self.side, 0, self.height))
    self.__draw_cylinder((0.5 * self.side, math.sqrt(0.75) * self.side, 0), (0.5 * self.side, math.sqrt(0.75) * self.side, self.height))

    # Decorative spheres

    self.__draw_sphere((0, 0, 0))
    self.__draw_sphere((self.side, 0, 0))
    self.__draw_sphere((0.5 * self.side, math.sqrt(0.75) * self.side, 0))
    self.__draw_sphere((0, 0, self.height))
    self.__draw_sphere((self.side, 0, self.height))
    self.__draw_sphere((0.5 * self.side, math.sqrt(0.75) * self.side, self.height))

    # Plot the current point

    gl.glColor3f(RED[0], RED[1], RED[2])
    self.__draw_sphere(self.command_parser.last_point, radius=0.03)

    # Plot the pending selected points

    gl.glColor4f(YELLOW[0], YELLOW[1], YELLOW[2], 0.7)
    self.__draw_line(self.command_parser.current_points)

    if len(self.command_parser.current_points) > 0:
      self.__draw_sphere(self.command_parser.current_points[-1])
      self.__draw_line([self.command_parser.current_points[-1], self.command_parser.last_point])

    # Predictive line

    # Plot the polygons

    gl.glColor4f(BLUE[0], BLUE[1], BLUE[2], 0.7)
    for poly in self.command_parser.polygons:
      self.__draw_polygon(poly)

    glut.glutSwapBuffers()

  def __parse_sample_commands(self):
    if not self.sample_commands_parsed:
      self.sample_commands_parsed = True
      f = open('sample_commands', 'r')
      lines = f.readlines()
      for l in lines:
        self.command_parser.process(l)
        glut.glutPostRedisplay()
      f.close()

  def __idle(self):
    self.__parse_sample_commands()

  def __reshape(self, width, height):
    gl.glViewport(0, 0, width, height)

  def __keyboard(self, key, x, y):
    if key == '\033':
      exit()
