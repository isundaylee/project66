import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import vispy.gloo as gloo
import vispy.app as app

import math

from command_parser import CommandParser

VERT_SHADER = """ // simple vertex shader
attribute vec3 a_position;
void main (void) {
    gl_Position = vec4(a_position, 1.0);
}
"""

FRAG_SHADER = """ // simple fragment shader
uniform vec4 u_color;
void main()
{
    gl_FragColor = u_color;
}
"""

class ScreenController(object):

  def __init__(self, side, height):
    super(ScreenController, self).__init__()
    self.command_parser = CommandParser(self)
    self.side = side
    self.height = height

  def run(self):
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
    glut.glutCreateWindow('Hello, triangles! ')
    glut.glutReshapeWindow(800, 600)
    glut.glutReshapeFunc(self.__reshape)
    glut.glutDisplayFunc(self.__display)
    glut.glutKeyboardFunc(self.__keyboard)

    gl.glClearColor(1, 1, 1, 1)
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glEnable(gl.GL_CULL_FACE)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_LIGHTING)

    self.quadric = glu.gluNewQuadric()
    glu.gluQuadricNormals(self.quadric, glu.GLU_SMOOTH)
    glu.gluQuadricTexture(self.quadric, gl.GL_TRUE)

    lightPosition = [self.side / 2, self.height / 2, self.side / 3, 0.05]
    lightColor = [10.0 / 255, 124.0 / 255, 1, 1]

    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, lightPosition)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, lightColor)
    gl.glLightf(gl.GL_LIGHT0, gl.GL_CONSTANT_ATTENUATION, 0.01)
    gl.glLightf(gl.GL_LIGHT0, gl.GL_LINEAR_ATTENUATION, 0.05)
    gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT)
    gl.glEnable(gl.GL_COLOR_MATERIAL)
    gl.glEnable(gl.GL_LIGHT0)


    gl.glMatrixMode(gl.GL_PROJECTION)
    glu.gluPerspective(20, 1, 1, 40)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    glu.gluLookAt(
      self.side / 2, self.height / 2, 3,
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

  def __draw_cylinder(self, p1, p2, radius=0.005):
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

  def __draw_sphere(self, p1, radius=0.01):
    p1 = self.tr(p1[0], p1[1], p1[2])

    gl.glPushMatrix()

    gl.glTranslatef(p1[0], p1[1], p1[2])

    glu.gluSphere(self.quadric, radius, 32, 32)

    gl.glPopMatrix()

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

    gl.glColor3f(1.0, 0.0, 0.0)

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

    glut.glutSwapBuffers()

  def __reshape(self, width, height):
    gl.glViewport(0, 0, width, height)

  def __keyboard(self, key, x, y):
    if key == '\033':
      exit()
