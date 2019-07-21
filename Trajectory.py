from cloner import *
from validations import *

class PathList(Cloner):
	#private class atributes
	__FuncType = {type(print), type(lambda:1)}
	__NumType = {type(int()), type(float())}


	#magical methods
	def __init__(self,
		Xfunc,					#Параметризация координаты x от t
		Yfunc,					#Параметризация координаты y от t
		t1,						#Ограничение параметра t слева
		t2,						#Ограничение параметра t справа
		Next = None):		#Указатель на следующий элемент списка

		self.__Xfunc = Xfunc if type(Xfunc) in self.__FuncType else lambda t: t
		self.__Yfunc = Yfunc if type(Yfunc) in self.__FuncType else lambda t: t
		t1 = float(t1) if type(t1) in self.__NumType else 0
		t2 = float(t2) if type(t2) in self.__NumType else 0
		if t1 > t2:
			self.__t1 = t2
			self.__t2 = t1
		else:
			self.__t1 = t1
			self.__t2 = t2
		self.__Next = Next if type(Next) == type(self) else None
		

	def __repr__(self):
		return ( ', '.join(["PathList(" + repr(self.Xfunc), repr(self.Yfunc), str(self.t1), str(self.t2) + ')']) + 
		(' ==> ' + repr(self.Next) if self.Next != None else '') )


	def __add__(self, other):
		if other.get_last_node() == self: return self # Check first looping situation independent of self's last node
		new = self.independent_clone()			# Then we can copy self to except modification of self
		LastNode = new.get_last_node()		# And find it's last node to check second situation
		if LastNode == other: return self	# There we check second looping situation
		LastNode.Next = other				# Then we can modificate copy of self to return it
		dt = LastNode.t2 - other.t1
		while other != None:				# There we must make shift of time intervals
			other.t1 += dt
			other.t2 += dt
			other = other.Next
		return new							# Finally return 'summa'


	#public methods
	def get_last_node(self):
		current = self
		while 1:
			following = current.Next
			if current == following: 
				current.Next = None
				return current
			if following == None:
				return current;
			current = following


	def isordered(self):
		current = self
		while True:
			if current.Next == None: return True
			if current.t2 > current.Next.t1 : return False
			current = current.Next


	def isfullconnected(self):
		current = self
		while True:
			if current.Next == None: return True
			if current.t2 != current.Next.t1 : return False
			current = current.Next


	def get_current_node(self, t):
		if t < self.t1: return self
		elif t > self.t2: return self.Next.get_current_node(t) if self.Next != None else None
		else: return self


	def get_coordinates(self, t):
		current = self.get_current_node(t)
		return (current.Xfunc(t), current.Yfunc(t)) if current != None else None


	#public class methods
	@classmethod
	def create_by_points(cls, points, t0 = 0):
		if len(points) == 1: return cls(lambda t: points[0][0], lambda t: points[0][1], t0, t0)
		elif not len(points): return None

		result = None
		t1 = t0
		PASHA_TEHNIK = []
		for k in range(1, len(points)):
			M1 = points[k-1]
			M2 = points[k]
			if M1 == M2: 
				if k == len(points) and not len(PASHA_TEHNIK): return cls.create_by_points(cls, [M1], t0)
				else: continue
			dt = (((M1[0] - M2[0])**2 + (M1[1] - M2[1])**2)**0.5)*10
			kx = (M2[0] - M1[0])/dt
			x0 = M1[0] - kx*t1
			ky = (M2[1] - M1[1])/dt
			y0 = M1[1] - ky*t1
			PASHA_TEHNIK.append((t1, dt, kx, x0, ky, y0))
			t1 += dt
		def recursor(prmtrs_arr):
			prmtrs = prmtrs_arr[0]
			instance = cls(lambda tau: tau * prmtrs[2] + prmtrs[3], lambda tau: tau * prmtrs[4] + prmtrs[5], prmtrs[0], prmtrs[0] + prmtrs[1])

			if len(prmtrs_arr) == 1: 
				return instance

			else:
				instance.Next = recursor(prmtrs_arr[1:])
				return instance

		return recursor(PASHA_TEHNIK)


	#properties as private getters and setters
	def __get_Xfunc(self):
		return self.__Xfunc
		pass
	def __set_Xfunc(self, value):
		if type(value) != self.__FuncType: return
		try:
			value(self.t1)
		except Exception:
			return
		else: self.__Xfunc = value
	Xfunc = property(__get_Xfunc, __set_Xfunc)


	def __get_Yfunc(self):
		return self.__Yfunc
		pass
	def __set_Yfunc(self, value):
		if type(value) != self.__FuncType: return
		try:
			value(self.t1)
		except Exception:
			return
		else: self.__Yfunc = value
	Yfunc = property(__get_Yfunc, __set_Yfunc)


	def __get_Next(self):
		return self.__Next
		pass
	def __set_Next(self, value):
		if type(value) == type(self) or value == None: self.__Next = value
		pass
	Next = property(__get_Next, __set_Next)


	def __get_t1(self):
		return self.__t1
		pass
	def __set_t1(self, value):
		if not (type(value) in self.__NumType):
			try:float(value)
			except Exception:return
		value = float(value)
		if value <= self.__t2: self.__t1 = value
	t1 = property(__get_t1, __set_t1)


	def __get_t2(self):
		return self.__t2
		pass
	def __set_t2(self, value):
		if not (type(value) in self.__NumType):
			try:float(value)
			except Exception:return
		value = float(value)
		if value >= self.__t1: self.__t2 = value
	t2 = property(__get_t2, __set_t2)
	