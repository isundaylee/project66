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

    gl.glClearColor(0, 0, 0, 1)
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glEnable(gl.GL_CULL_FACE)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_LIGHTING)

    lightPosition = [10, 4, 10, 1]
    lightColor = [0.8, 1.0, 0.8, 1.0]

    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, lightPosition)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, lightColor)
    gl.glLightf(gl.GL_LIGHT0, gl.GL_CONSTANT_ATTENUATION, 0.1)
    gl.glLightf(gl.GL_LIGHT0, gl.GL_LINEAR_ATTENUATION, 0.05)
    gl.glEnable(gl.GL_LIGHT0)

    gl.glMatrixMode(gl.GL_PROJECTION)
    glu.gluPerspective(40, 1, 1, 40)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    glu.gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)
    gl.glPushMatrix()

    glut.glutMainLoop()

  def __display(self):
    # Drawing the framework

    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glPushMatrix()
    color = [1.0, 0, 0, 1]
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, color)
    glut.glutSolidSphere(2, 20, 20)
    gl.glPopMatrix()

    glut.glutSwapBuffers()

  def __reshape(self, width, height):
    gl.glViewport(0, 0, width, height)

  def __keyboard(self, key, x, y):
    if key == '\033':
      exit()
