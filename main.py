from coordinate_parser import CoordinateParser
from screen_controller import ScreenController


width = 0.6414
depth = 0.4477
height = 1.219
sensors = (((0, 0), 391), ((0, depth), 391), ((width, depth), 391), ((width, 0),391))

controller = ScreenController(sensors, width, depth, height)
controller.run()
