from coordinate_parser import CoordinateParser
from screen_controller import ScreenController

parser = CoordinateParser(0.5, 0.5)
print parser.parse(0.4, 0.4, 0.4)

controller = ScreenController(0.5, 0.5)
controller.run()