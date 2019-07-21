import tools
from loadingModule import *
from Trajectory import *


class VisualObjFrame:
	def __init__(self, image_list, position, angle=0):
		self._state = 'dont touch me'
		self._image_dict = {self._state: image_list}
		self._position = position
		self._angle = angle
		self._counter = 0



	def __del__(self):
		#print(str(self) + ' deleted')
		pass

	#public methods
	def visualise(self, display):
		if self._state == None: return print('Nothing to visualise')
		else:
			if self._position == None: return
			imgList = self._image_dict[self._state]
			counter = self._counter
			img_list_length = len(imgList)
			if img_list_length: 
				ready_surf = pg.transform.rotate(imgList[counter], self._angle)
				pos = (int(self._position[0]-ready_surf.get_width()/2), int(self._position[1]-ready_surf.get_height()/2))
				display.blit(ready_surf, pos)
			if counter+1 == img_list_length or not img_list_length:
				self.end_visualisation()
			else: self._counter += 1
			 

	#protected methods
	def _get_counter(self):
		return self._counter
		pass

	def end_visualisation(self):
		self._counter = 0



	#properties as private getters and setters
	def __get_angle(self):
		return self._angle
		pass
	def __set_angle(self, value):
		if float_valid(value):
			value = float(value)%360
			self._angle = value	
	angle = property(__get_angle, __set_angle)


	def __get_position(self):
		return self._position
		pass
	def __set_position(self, value):
		return
		pass
	position = property(__get_position, __set_position)




class VisualObj(VisualObjFrame):
	#magical methods
	def __init__(self, image_dict, position, state = None, angle=0):
		self._image_dict = image_dict
		self._position = position
		self._angle = angle
		self._state = state if state in image_dict.keys() else None
		self._counter = 0
	

	def change_state(self, new, reset_counter = True):#BE CAREFUL WHILE USING reset_counter = False. It can rise IndexError
		try:
			self._image_dict[new]
		except KeyError:
			print('Cannot change state to' + str(new) + 'in ' + str(self))
			return
		self._state = new
		if reset_counter != False: self._counter = 0
	

	def __get_state(self):
		return self._state
		pass
	def __set_state(self, value):
		return
		pass
	state = property(__get_state, __set_state)




class FiniteVisualObj(VisualObjFrame):
	def __init__(self, image_list, position, angle=0, other_task = False):
		self.other_task = other_task
		VisualObjFrame.__init__(self, image_list, position, angle)


	def end_visualisation(self, *args, **kwargs):
		if self.other_task != False: (self.other_task)(self, *args, **kwargs)
		FiniteVisualObj._Level.add_visualObj_to_trash(self)