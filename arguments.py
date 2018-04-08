from sys import argv

args = {}

def setup_argument(index, name=None, default=None):
  if name == None:
    name = index
  if index >= len(argv)-1:
    if default == None:
      raise Exception("No default value for argument: " + index)
    else:
      args[name] = default
  else:
    if type(default) == bool:
      args[name] = bool(argv[index + 1])
    elif type(default) == int:
      args[name] = int(argv[index + 1])
    else:
      args[name] = argv[index + 1]
