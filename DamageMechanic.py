from VoicedObjects import *
import math


#UHPDO stands for Unified Hit-points and Damage Object
class UHPDO():
	def __init__(self, hit_points, first=1, second=0, third=0, fourth=0, fifth=0):
		self.__HitPoints = int(hit_points) if int_valid(hit_points) else 100
		self.__first = first if float_valid(first) else 1
		self.__second = second if float_valid(second) else 0
		self.__third = third if float_valid(third) else 0
		self.__fourth = fourth if float_valid(fourth) else 0
		self.__fifth = fifth if float_valid(fifth) else 0


	def  __add__(self, other):
		return UHPDO(self.HitPoints + other.HitPoints, self.first+ other.first, self.second + other.second, self.third + other.third, self.fourth + other.fourth, self.fifth + other.fifth)
		pass


	def __sub__(self, other):
		newHP = self.HitPoints - other.HitPoints*(self%other)
		return UHPDO(int(newHP), self.first, self.second, self.third, self.fourth, self.fifth)


	def __iadd__(self, other):
		return self + other
		pass


	def __isub__(self, other):
		return self - other
		pass


	def __int__(self):
		return self.__HitPoints
		pass


	def __mod__(self, other):
		return self.first*other.first+self.second*other.second+self.third*other.third+self.fourth*other.fourth+self.fifth*other.fifth


	def __repr__(self):
		return 'UHPDO(' + str(self.HitPoints)+', '+str(self.first)+', '+str(self.second)+', '+str(self.third)+', '+str(self.fourth)+', '+str(self.fifth)+')'
		pass


	def isalive(self):
		return True if self.HitPoints >= 0 else False


	def __get_HitPoints(self):
		return self.__HitPoints
		pass
	def __set_HitPoints(self, value):
		if int_valid(value): self.__HitPoints = value
		return
	HitPoints = property(__get_HitPoints, __set_HitPoints)


	def __get_first(self):
		return self.__first
		pass
	def __set_first(self, value):
		if float_valid(value): self.__first = value
		return
	first = property(__get_first, __set_first)


	def __get_second(self):
		return self.__second
		pass
	def __set_second(self, value):
		if float_valid(value): self.__second = value
		return
	second = property(__get_second, __set_second)


	def __get_third(self):
		return self.__third
		pass
	def __set_third(self, value):
		if float_valid(value): self.__third = value
		return
	third = property(__get_third, __set_third)


	def __get_fourth(self):
		return self.__fourth
		pass
	def __set_fourth(self, value):
		if float_valid(value): self.__fourth = value
		return
	fourth = property(__get_fourth, __set_fourth)


	def __get_fifth(self):
		return self.__fifth
		pass
	def __set_fifth(self, value):
		if float_valid(value): self.__fifth = value
		return
	fifth = property(__get_fifth, __set_fifth)



class Shot(MovingObj, Cloner, VoicedObj):
	def __init__(self, target, damage, position, image_dict, speed = 10, voices = {}):
		self.__target = target
		self.damage = damage
		MovingObj.__init__(self, None, image_dict, names.ShotFlowSt, 0, speed)
		VoicedObj.__init__(self, voices)
		self._position = position
		self.__path = PathList.create_by_points([self.position, target.position]) if target != None else None
		self.__t = 0


	def blast(self, position):
		self.voice(names.ShotBlastVoice)
		Shot._Level.add_visualObj(FiniteVisualObj(self._image_dict[names.ShotBlastSt], position, self.angle))


	def remove(self):
		Shot._Level.add_shot_to_trash(self)
		pass

	def move(self, dt):
		if self.target == None: 
			self.remove()
			return None
		if self.target.HP == None: 
			self.remove()
			return None
		if self._position == None: 
			self.end_move(dt)
		else: 
			self.__t = self.__t + dt*self.speed
			path_res = self.__path.get_current_node(self.__t) if self.__path != None else None
			self._position = path_res.get_coordinates(self.__t)	if path_res != None else None
			M1 = self.position
			M2 = self.target.position
			if not (M1 == M2 or M2 == None or M1 == None): self.angle = tools.offcut_angle(M1, M2)

			self.__path = PathList.create_by_points([M1, M2], self.t) if path_res != None else None


	def end_move(self, dt):
		self.target.hit(self.damage)
		self.blast(self.target.position)
		self.remove()


	def __get_target(self):
		return self.__target

	def __set_target(self, value):
		if isinstance(value, MovingObj):
			self.__target = value
			self.__path = PathList.create_by_points([self.position, self.target.position])
	
	target = property(__get_target, __set_target)



