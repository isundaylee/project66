class CommandParser(object):
  def __init__(self, delegate):
    super(CommandParser, self).__init__()
    self.delegate = delegate

  def process(self, command):
    parts = command.split()

    type = parts.pop(0)

    if type == 'point':
      self.delegate.point(float(parts[0]), float(parts[1]), float(parts[2]))
    elif type == 'mode':
      self.delegate.mode(parts[0])
