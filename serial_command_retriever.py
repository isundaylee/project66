import serial

INTERRUPT_COMMANDS = [
  "click\n",
  "doubleclick\n",
  "hold\n",
  "mode polygon\n",
  "mode curve\n",
  "mode sculpt\n",
  "mode extrude\n"
]

class SerialCommandRetriever(object):
  def __init__(self, port):
    super(SerialCommandRetriever, self).__init__()
    self.port = port
    self.data = ""
    self.serial = serial.Serial(self.port, baudrate=9600, timeout=0.01)

  def fetch(self):
    commands = []

    if self.serial.inWaiting() > 0:
      self.data = self.data + self.serial.read(16)

      for c in INTERRUPT_COMMANDS:
        if c in self.data:
          commands.append(c)
          self.data = self.data.replace(c, "")

      loc = self.data.find("\n")

      if loc != -1:
        commands.append(self.data[0:loc])
        self.data = self.data[loc + 1:]

    return commands

  def send(self, msg):
    self.serial.write(msg)

