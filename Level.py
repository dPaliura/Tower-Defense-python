from Wave import *
from SingletonDecorator import *
from TrashBasket import *


@Singleton
class Level(TrashBasket):
	__default_map = pg.Surface((2000,2000))
	__default_map.fill((50,100,200))


	def __init__(self, display, enemy_list=list(), available_towers = list(), money = 20, level_map = __default_map, player_HP = 5, towers_spacings = 100, towers_set=set(), visualObjs_set=set()):
		self.__enemies_list = enemy_list
		self.__available_towers = {}
		for twr in available_towers:
			if type(twr) is Tower:
				self.__available_towers[twr._name] = twr	#Rewrite available towers as dict to get access by key
		self.__towers_set = towers_set 											#BE CAREFUL and remember that towers must have DIFFERENT NAMES
		self.__shots_set = set()
		self.__visualObjs_set = visualObjs_set
		self.__map = level_map
		self.__display = display
		self.__money = money if int_valid(money) else 20
		self.__preparing_towers = set()
		self.__towers_spacings = towers_spacings
		self._player_HP = player_HP if int_valid (player_HP) else 5
		TrashBasket._init(self)


	def clear_basket(self):
		for wasted_enemy in self._trash_enemies: 
			self.__enemies_list.remove(wasted_enemy)
		self._trash_enemies = list()

		self.__shots_set -= self._trash_shots
		self._trash_shots = set()

		self.__visualObjs_set -= self._trash_visualObjs
		self._trash_visualObjs = set()


	def build_tower(self, tower_name, position):
		for tower in self.__towers_set | self.__preparing_towers:
			if tools.distance_cmp_radius(tower.position, position, self.__towers_spacings) == -1:
				print('Can not build tower '+tower_name+' at position '+str(position)+': too close to other tower '+tower._name+' at position '+str(tower.position))
				#rise TowersSpacingError
				return
		if not tower_name in self.__available_towers.keys():
			print('Can not build tower '+tower_name+' at position '+str(position)+': this name uncorrect or tower is not available at current level.')
			#rise TowerNameError
			return 
		new_tower = self.__available_towers[tower_name].clone()
		new_tower._SHOT = new_tower._SHOT.clone()
		new_tower._position = position
		new_tower._SHOT._position = position
		if not new_tower._image_dict[names.TowerBuildingSt]: 
			self.add_tower(new_tower)
			new_tower.voice(names.TowerBuildEndVoice)
		else:
			self.__preparing_towers |= {new_tower}
			def Task(something_no_matter_what_at_specifically_this_case):
				self.add_tower(new_tower)
				new_tower.voice(names.TowerBuildEndVoice)
				self.__preparing_towers -= {new_tower}
			new_tower.voice(names.TowerBuildStartVoice)
			building = FiniteVisualObj(new_tower._image_dict[names.TowerBuildingSt], position, other_task = Task)
			self.add_visualObj(building)


	def recieve_reward(self, killed):
		self.__money += killed.reward
		print('You recieved', killed.reward, 'money-points for killing', killed.name)


	def init_dependencies(self):
		Enemy._Level = self
		Tower._Level = self
		Shot._Level = self
		FiniteVisualObj._Level = self


	def add_shot(self, value):
		self.__shots_set |= {value}
		pass


	def add_visualObj(self, value):
		self.__visualObjs_set |= {value}
		pass


	def add_tower(self, value):
		self.__towers_set |= {value}
		pass


	def move_enemies(self, dt):
		for enemy in self.__enemies_list:
			enemy.move(dt)


	def visualise_enemies(self):
		for enemy in self.__enemies_list:
			enemy.visualise(self.__display)


	def towers_fire(self, dt):
		for tower in self.__towers_set:
			tower.try_shot(dt)


	def visualise_towers(self):
		for tower in self.__towers_set:
			tower.visualise(self.__display)


	def move_shots(self, dt):
		for shot in self.__shots_set:
			shot.move(dt)


	def visualise_shots(self):
		for shot in self.__shots_set:
			shot.visualise(self.__display)


	def visualise_visualObjs(self):
		for VO in self.__visualObjs_set:
			VO.visualise(self.__display)


	def get_enemies_list(self):
		return self.__enemies_list
		pass


	def process_enemies(self, dt, display):
		for enemy in self.__enemies_list:
			enemy.move(dt)
			enemy.visualise(display)


	def process_shots(self, dt, display):
		for shot in self.__shots_set:
			shot.move(dt)
			shot.visualise(display)


	def process_towers(self, dt, display):
		for tower in self.__towers_set:
			tower.try_shot(dt)
			tower.visualise(display)


	def process_visualObjs(self, display):
		for VO in self.__visualObjs_set:
			VO.visualise(display)


	def update(self, dt, delay = True):
		display = self.__display
		display.blit(self.__map, (0,0))
		
		self.process_enemies(dt, display)
		self.process_shots(dt, display)
		self.process_towers(dt, display)
		self.process_visualObjs(display)

		self.clear_basket()