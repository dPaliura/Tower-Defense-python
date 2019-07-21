import copy

class Cloner:
	def clone(self):
		return copy.copy(self)

	def independent_clone(self):
		return copy.deepcopy(self)