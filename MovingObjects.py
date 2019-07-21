from VisualisedObjects import *
from abc import ABC, abstractmethod
import names

class MovingObj(VisualObj, ABC):
	#magical methods
	def __init__(self, path, image_dict, state = None, t = None, speed = 1):
		self.__speed = speed
		self.__path = path if type(path) == PathList else PathList(0, 0, 0, 0)
		self.__t = None if self.__path == None else (
			self.__path.t1 if (t == None or not float_valid(t))  else float(t))
		VisualObj.__init__(self, image_dict, self.get_current_position(), state, angle=self.get_angle_in_timepoint())

	#public methods
	def get_current_position(self):
		return self.__path.get_coordinates(self.__t) if self.__path != None else None
		pass

	
	def ismovable(self):
		return False if self.__path == None or self.speed==0 else True
		pass
	

	def get_angle_in_timepoint(self, t=None, default = 0):#default will be returned in case dx = dy = 0
		t = self.__t if t == None or not float_valid(t) else float(t)
		path = self.__path.get_current_node(t)
		if path == None: return self.angle 
		M1 = path.get_coordinates(path.t1)
		M2 = path.get_coordinates(path.t2)
		return -tools.offcut_angle(M1, M2) if M1 != M2 else default


	#private methods
	def move(self, dt):
		dt = float(dt) if float_valid(dt) else 0
		dt = dt if dt>=0 else 0
		self.__t = self.__t + dt*self.speed
		prev_path = self.__path
		new_path = self.__path.get_current_node(self.__t) if self.__path != None else None
		self.__path = new_path
		self._position = self.__path.get_coordinates(self.__t)	if self.__path != None  and self.__t >= 0 else None
		if prev_path != new_path and new_path != None:
			self._angle = self.get_angle_in_timepoint(default = self._angle)
		if self.__path == None: self.end_move(dt)

	#abstract methods
	@abstractmethod
	def end_move(self, dt):
		pass
		pass
	

	#properties as private getters and setters
	def __get_speed(self):
		return self.__speed
		pass
	def __set_speed(self, value):
		value = float(value) if float_valid(value) else 1.0
		self.__speed = value if value>=0 else 1.0
	speed = property(__get_speed, __set_speed)


	def __get_path(self):
		return copy.deepcopy(self.__path)
		pass
	def __set_path(self, value):
		return
		pass
	path = property(__get_path, __set_path)


	def __get_t(self):
		return self.__t
		pass
	def __set_t(self, value):
		return
		pass
	t = property(__get_t, __set_t)