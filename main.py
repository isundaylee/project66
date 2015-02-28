from coordinate_parser import CoordinateParser
from screen_controller import ScreenController

parser = CoordinateParser(5, 7)

# for i in range(20):
#   p = parser.generate_random_point()

#   print (' '.join(('point', str(p[0]), str(p[1]), str(p[2]))))

controller = ScreenController(5, 7)
controller.run()