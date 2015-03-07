import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import vispy.gloo as gloo
import vispy.app as app
import ctypes

import math
import random
from geometry import minus, plus

from command_parser import *
from coordinate_parser import CoordinateParser

COLZ=((0, 0.8, 0), (1, 243.0 / 255, 71.0 / 255), (10.0 / 255, 124.0 / 255, 1), (1, 0, 0), (1,1,1) )

GREEN = (0, 0.8, 0)
YELLOW = (1, 243.0 / 255, 71.0 / 255)
BLUE = (10.0 / 255, 124.0 / 255, 1)
RED = (1, 0, 0)
WHITE = (1,1,1)

WIDTH = 1280
HEIGHT = 800

BASE_WIDTH = 0.2

class ScreenController(object):

  sample_commands_parsed = False

  def __init__(self, side, height):
    super(ScreenController, self).__init__()
    self.command_parser = CommandParser(side, height)
    self.coordinate_parser = CoordinateParser(side, height)
    self.side = float(side)
    self.height = float(height)
    self.phi = 0
    self.theta = 0
    self.zoom = 1
    self.point2 = (side/2,side/2,height/2)

  def run(self):
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DEPTH|glut.GLUT_DOUBLE | glut.GLUT_RGBA)
    glut.glutCreateWindow('Hello, triangles! ')
    glut.glutReshapeWindow(WIDTH, HEIGHT)
    glut.glutReshapeFunc(self.__reshape)
    glut.glutDisplayFunc(self.__display)
    glut.glutIdleFunc(self.__idle)
    glut.glutKeyboardFunc(self.__keyboard)

    gl.glLineWidth(0.001);
    gl.glClearColor(0, 0, 0, 1)
    # gl.glShadeModel(gl.GL_SMOOTH)
    gl.glLineWidth(BASE_WIDTH * 1000)
    gl.glDisable(gl.GL_CULL_FACE)

    gl.glEnable(gl.GL_DEPTH_TEST);
    gl.glDepthMask(gl.GL_TRUE);
    gl.glDepthFunc(gl.GL_LEQUAL);
    gl.glDepthRange(0.0, 1.0);


    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    # gl.glEnable(gl.GL_LIGHTING)

    self.quadric = glu.gluNewQuadric()
    glu.gluQuadricNormals(self.quadric, glu.GLU_SMOOTH)
    glu.gluQuadricTexture(self.quadric, gl.GL_TRUE)

    lightP= self.tr(self.side/2, self.side/2, self.side/2)
    lightPosition = [lightP[0],lightP[1],lightP[2],0.0]
    lightColor = [WHITE[0], WHITE[1], WHITE[2], 1]

    """gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, lightPosition)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, lightColor)
    gl.glLightf(gl.GL_LIGHT0, gl.GL_CONSTANT_ATTENUATION, 0.01)
    gl.glLightf(gl.GL_LIGHT0, gl.GL_LINEAR_ATTENUATION, 0.05)"""

    lightP= self.tr(-self.side/2, -self.side/2, self.side/2)
    lightPosition2 = [lightP[0],lightP[1],lightP[2],0.0]

    gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, gl.GLfloat_4(0.0, 1.0, 0.0, 1.0))
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, lightColor)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, gl.GLfloat_4(1.0, 1.0, 1.0, 1.0))
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, lightPosition)

    gl.glLightfv(gl.GL_LIGHT1, gl.GL_AMBIENT, gl.GLfloat_4(0.0, 1.0, 0.0, 1.0))
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_DIFFUSE, lightColor)
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_SPECULAR, gl.GLfloat_4(1.0, 1.0, 1.0, 1.0))
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_POSITION, lightPosition2)

    gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, gl.GLfloat_4(0.2, 0.2, 0.2, 1.0))
    gl.glEnable(gl.GL_LIGHTING)
    gl.glEnable(gl.GL_LIGHT0)
    gl.glEnable(gl.GL_LIGHT1)
    gl.glColorMaterial(gl.GL_FRONT, gl.GL_DIFFUSE)


    gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT, gl.GLfloat_4(0.2, 0.2, 0.2, 1.0))
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, gl.GLfloat_4(0.8, 0.8, 0.8, 1.0))
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, gl.GLfloat_4(1.0, 0.0, 1.0, 1.0))
    gl.glMaterialfv(gl.GL_FRONT, gl.GL_SHININESS, gl.GLfloat(50.0))
    gl.glEnable(gl.GL_COLOR_MATERIAL)
    gl.glEnable(gl.GL_LIGHT0)

    gl.glMatrixMode(gl.GL_PROJECTION)
    glu.gluPerspective(30, 1, 0.0001, 40)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    p1 =  self.turn(self.theta,self.phi,self.zoom)
    point3 = self.upvector(p1,self.point2)
    glu.gluLookAt(
      p1[0],p1[2],-p1[1],#v1[0],v1[1],v1[2],#
      self.point2[0],self.point2[2],-self.point2[1],#v2[0],v2[1],v2[2],#
      # 2, 0.5 * self.height, -math.sqrt(0.75 / 4) * self.side,
      # 0, 0.5 * self.height, -math.sqrt(0.75 / 4) * self.side,
      point3[0],point3[2],-point3[1]#v3[0],v3[1],v3[2]
    )
    gl.glPushMatrix()

    glut.glutMainLoop()

  # Translate from reallife coordinates to OpenGL coordinates
  def tr(self, x, y, z):
    return (x, z, -y)

  # Translate to reallife coordinates from OpenGL coordinates
  def fr(self, x, y, z):
    return (x, z, -y)

  def __draw_cylinder(self, p1, p2, radius=BASE_WIDTH*0.02, radius2=BASE_WIDTH*0.02):
    p1, p2 = self.tr(p1[0], p1[1], p1[2]), self.tr(p2[0], p2[1], p2[2])

    dx = float(p2[0] - p1[0])
    dy = float(p2[1] - p1[1])
    dz = float(p2[2] - p1[2])

    r = math.sqrt(dy ** 2 + dz ** 2)
    length = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    if length==0:
      return

    if r == 0:
      x_angle = 0
    else:
      x_angle = math.atan2(-dy / r, dz / r)
    y_angle = math.atan2(dx / length, r / length)

    gl.glPushMatrix()

    gl.glTranslatef(p1[0], p1[1], p1[2])
    gl.glRotatef(math.degrees(x_angle), 1, 0, 0)
    gl.glRotatef(math.degrees(y_angle), 0, 1, 0)

    glu.gluCylinder(self.quadric, radius, radius2, length, 32, 32)

    gl.glPopMatrix()

  def __draw_sphere(self, p1, radius=BASE_WIDTH*0.05):
    p1 = self.tr(p1[0], p1[1], p1[2])

    gl.glPushMatrix()

    gl.glTranslatef(p1[0], p1[1], p1[2])

    glu.gluSphere(self.quadric, radius, 32, 32)

    gl.glPopMatrix()

  def __draw_solid(self, solid, sizes):
    for i in range(len(solid)-1):
      sp=solid[i]
      ep=solid[i+1]
      print i,sp,ep
      self.__draw_sphere(sp,radius=(1)*sizes[i])
      self.__draw_cylinder(sp,ep,radius=sizes[i],radius2=sizes[i+1] )

  def __draw_polygon(self, op):
    r, g, b, a = gl.glGetFloatv(gl.GL_CURRENT_COLOR)

    points = op[:]
    points.append(points[0])

    gl.glBegin(gl.GL_TRIANGLE_FAN)

    for rp in points:
      p = self.tr(rp[0], rp[1], rp[2])
      gl.glVertex3f(p[0], p[1], p[2])

    gl.glEnd()

    gl.glColor4f(0.3 * r, 0.3 * g, 0.3 * b, a)

    gl.glBegin(gl.GL_LINE_LOOP)
    for rp in points:
      p = self.tr(rp[0], rp[1], rp[2])
      gl.glVertex3f(p[0], p[1], p[2])
    gl.glEnd()

    gl.glColor4f(r, g, b, a)

  def __draw_line(self, points):
    gl.glBegin(gl.GL_LINE_STRIP)

    for rp in points:
      p = self.tr(rp[0], rp[1], rp[2])
      gl.glVertex3f(p[0], p[1], p[2])

    gl.glEnd()

  def __draw_text(self, x, y, text):
      blending = False
      if gl.glIsEnabled(gl.GL_BLEND):
          blending = True

      gl.glColor3f(1, 1, 1)
      gl.glWindowPos2f(x,y)

      for ch in text:
          glut.glutBitmapCharacter(glut.GLUT_BITMAP_9_BY_15, ctypes.c_int(ord(ch)))

      if not blending:
          gl.glDisable(gl.GL_BLEND)

  def __draw_extrusion(self, extrusion):
    polys = self.command_parser.calculate_extrusion_extra_polygons(extrusion)

    for p in polys:
      self.__draw_polygon(p)

  def __display(self):
    gl.glClearColor(0.0, 0.0, 0.0, 0.0);
    gl.glClearDepth(1.0);
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT);

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

    CUR=COLZ[self.command_parser.color]

    if self.command_parser.mode == SS_POLYGON_MODE:
      gl.glColor3f(RED[0], RED[1], RED[2])
      self.__draw_sphere(self.command_parser.last_point, radius=0.03)
    elif self.command_parser.mode == SS_SCULPT_MODE:
      gl.glColor3f(CUR[0], CUR[1], CUR[2])
      self.__draw_sphere(self.command_parser.last_point, radius=self.command_parser.brush_radius)

    # Plot the pending selected points

    if self.command_parser.mode != SS_SCULPT_MODE:
      gl.glColor4f(YELLOW[0], YELLOW[1], YELLOW[2], 0.7)
      self.__draw_line(self.command_parser.current_points)
    else:
      if self.command_parser.sculpting:
        gl.glColor4f(YELLOW[0], YELLOW[1], YELLOW[2], 0.7)
        self.__draw_solid(self.command_parser.current_points,self.command_parser.current_sizes)


    if len(self.command_parser.current_points) > 0:
      self.__draw_sphere(self.command_parser.current_points[-1])
      self.__draw_line([self.command_parser.current_points[-1], self.command_parser.last_point])

    # Plot the polygons

    gl.glColor4f(BLUE[0], BLUE[1], BLUE[2], 0.7)
    for poly in self.command_parser.polygons:
      self.__draw_polygon(poly)

    # Plot the curves
    gl.glColor4f(BLUE[0], BLUE[1], BLUE[2], 0.7)
    for curve in self.command_parser.curves:
      self.__draw_line(curve)

    gl.glColor4f(CUR[0], CUR[1], CUR[2], 1)
    for solid in self.command_parser.solids:
      self.__draw_solid(solid[0],solid[1])

    # Draw status texts
    if self.command_parser.mode == SS_POLYGON_MODE:
      self.__draw_text(20, HEIGHT - 25, "POLYGON MODE")
    elif self.command_parser.mode==SS_CURVE_MODE:
      self.__draw_text(20, HEIGHT - 25, "CURVE MODE")
    elif self.command_parser.mode==SS_SCULPT_MODE:
      self.__draw_text(20, HEIGHT - 25, "SCULPT MODE")
    elif self.command_parser.mode == SS_EXTRUDE_MODE:
      self.__draw_text(20, HEIGHT - 25, "EXTRUDE MODE")

    if self.command_parser.mode == SS_POLYGON_MODE and self.command_parser.nearby_point:
      self.__draw_text(20, HEIGHT - 50, "NEARBY POINT DETECTED")

    if self.command_parser.mode == SS_EXTRUDE_MODE and self.command_parser.extruding_candidate:
      self.__draw_text(20, HEIGHT - 50, "EXTRUDING CANDIDATE DETECTED")

    # Draw the extrusion preview
    gl.glColor4f(YELLOW[0], YELLOW[1], YELLOW[2], 0.7)

    if self.command_parser.mode == SS_EXTRUDE_MODE and self.command_parser.extruding:
      preview = (self.command_parser.extruding_polygon, minus(self.command_parser.last_point, self.command_parser.extruding_origin))
      self.__draw_extrusion(preview)

    # # Draw the actual extrusions
    # gl.glColor4f(BLUE[0], BLUE[1], BLUE[2], 0.7)

    # for e in self.command_parser.extrusions:
    #   self.__draw_extrusion(e)

    if self.command_parser.last_point:
      self.__draw_text(WIDTH - 140, HEIGHT - 25, str(self.command_parser.last_point[0]))
      self.__draw_text(WIDTH - 140, HEIGHT - 50, str(self.command_parser.last_point[1]))
      self.__draw_text(WIDTH - 140, HEIGHT - 75, str(self.command_parser.last_point[2]))

    # Plot the current point

    if self.command_parser.mode == SS_POLYGON_MODE or self.command_parser.mode == SS_EXTRUDE_MODE:
      gl.glColor3f(RED[0], RED[1], RED[2])
      self.__draw_sphere(self.command_parser.last_point, radius=0.01)
    elif self.command_parser.mode == SS_SCULPT_MODE:
      gl.glColor3f(GREEN[0], GREEN[1], GREEN[2])
      self.__draw_sphere(self.command_parser.last_point, radius=0.03)

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
    # self.__parse_sample_commands()
    # self.command_parser.process("point %lf %lf %lf" % self.coordinate_parser.generate_random_point())
    # if random.random() < 0.05:
      # self.command_parser.process("click")
    # if random.random() < 0.01:
      # self.command_parser.process("hold")

    self.command_parser.fetch_and_process()
    glut.glutPostRedisplay()

  def __reshape(self, width, height):
    gl.glViewport(0, 0, width, height)
  def turn(self,theta,phi,zoom):
    return (self.side/2+zoom*9*self.side*math.sin(theta)/2,self.side/2-zoom*9*self.side*math.cos(theta)/2,
      self.height/2+zoom*9*self.height*math.sin(phi)/2)
  def upvector(self,p1,p2):
    if p2[2] == p1[2]:
        return (0,0,1)
    else:
        return (p1[0]-p2[0],p1[1]-p2[1],abs(((p1[0]-p2[0]) ** 2 + (p1[1]-p2[1]) ** 2)/(p2[2]-p1[2])))
  def outputfile(self):
    f = open('myPaint.obj', 'w')
    vertices = []
    faces = []
    for poly in self.command_parser.polygons:
      first = len(vertices)
      current = len(vertices)
      for i in poly:
        vertices = vertices+['v '+ str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) +'\n']
        if first+1 < current:
          faces = faces + ['f '+ str(first+1) + ' ' + str(current) + ' ' + str(current+1) + '\n']
        current += 1
    for i in vertices:
      f.write(i)
    f.write('g objsurface' + '\n')
    for i in faces:
      f.write(i)
    f.write('g')

  def __keyboard(self, key, x, y):
    if key == chr(27):
      exit()
    if key == chr(119): #up
        self.phi =self.phi + 0.05
    if key == chr(115): #down
        self.phi = self.phi -0.05
    if key == chr(97):  #left
        self.theta = self.theta -0.05
    if key == chr(100): #right
        self.theta = self.theta +0.05
    if key == chr(113): #zoom in(q)
        self.zoom = self.zoom *0.95
    if key == chr(101): #zoom out(e)
        self.zoom = self.zoom *1.05
    if key == chr(111): #output as .obj
        self.outputfile()
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    p1 =  self.turn(self.theta,self.phi,self.zoom)
    point3 = self.upvector(p1,self.point2)
    glu.gluLookAt(
      p1[0],p1[2],-p1[1],#v1[0],v1[1],v1[2],#
      self.point2[0],self.point2[2],-self.point2[1],#v2[0],v2[1],v2[2],#
      # 2, 0.5 * self.height, -math.sqrt(0.75 / 4) * self.side,
      # 0, 0.5 * self.height, -math.sqrt(0.75 / 4) * self.side,
      point3[0],point3[2],-point3[1]#v3[0],v3[1],v3[2]
    )
    if key == chr(114):
      self.command_parser.polygons = []
      self.command_parser.curves = []
      self.command_parser.current_points = []
      self.command_parser.current_sizes = []
      self.command_parser.solids = []
      self.command_parser.extrusions = []
      self.command_parser.samples = []
      self.theta = 0
      self.zoom = 1
      self.phi = 0
    glut.glutPostRedisplay()

#
