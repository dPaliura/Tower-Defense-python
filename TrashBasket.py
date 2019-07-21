class TrashBasket:
	def _init(self):
		self._trash_enemies = list()
		self._trash_shots = set()
		self._trash_visualObjs = set()


	def pop_trash_enemy(self):
		return self._trash_enemies.pop()
		pass


	def pop_all_trash_enemies(self):
		all_enemies = self._trash_enemies
		self._trash_enemies = list()
		return all_enemies


	def add_enemy_to_trash(self, value):
		self._trash_enemies.append(value)
		pass


	def pop_trash_shot(self):
		return self._trash_shots.pop()
		pass


	def pop_all_trash_shots(self):
		all_shots = self._trash_shots
		self._trash_shots = set()
		return all_enemies


	def add_shot_to_trash(self, value):
		self._trash_shots |= {value}
		pass


	def pop_trash_visualObj(self):
		return self._trash_visualObjs.pop()
		pass


	def pop_all_trash_visualObjs(self):
		all_visuals = self._trash_visualObjs
		self._trash_visualObjs = set()
		return all_visuals


	def add_visualObj_to_trash(self, value):
		self._trash_visualObjs |= {value}
		pass

	def basket_is_empty(self):
		return False if self._trash_enemies or self._trash_shots or self._trash_visualObjs else True
		pass