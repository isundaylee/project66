import socket

BUFFER_SIZE = 1024

INTERRUPT_COMMANDS = [
  "click\n",
  "doubleclick\n",
  "hold\n",
  "mode polygon\n",
  "mode curve\n",
  "mode sculpt\n",
  "mode extrude\n"
]

class WifiCommandRetriever(object):
  def __init__(self, ip, port):
    super(WifiCommandRetriever, self).__init__()
    self.ip = ip
    self.port = port

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((self.ip, self.port))

    if self.socket == None:
      print('#' * 100)

    self.data = ''

  def fetch(self):
    commands = []

    self.data += self.socket.recv(BUFFER_SIZE)

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
    pass

