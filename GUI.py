from Level import *
from controls import *
class GUIconfig:
	def __init__(self):
		pass



@Singletone
class GUI:
	def __init__(self, level = Level(), controls = None, config = GUIconfig()):
		self._level = level
		self.__controls = controls