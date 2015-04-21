from coordinate_parser import CoordinateParser
from screen_controller import ScreenController


sensors = ((0, 0, 0), (0, .4477, 0), (.6414, .4477, 0), (.6414, 0, 0))

controller = ScreenController(sensors, 0.65, 0.8)
controller.run()
