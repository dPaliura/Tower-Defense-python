from WaveCreator import *

class Tower(VisualObj, VoicedObj, Cloner):
	def __init__(self, damageUHPDO, image_dict, shot_image_dict, name = names.TowerDefaultName, position = (0, 0), radius = 500, shots_delay = 1000, shot_speed = 1, cost = 15, voices = {}, shot_voices = {}):
		self.__radius = radius if float_valid(radius) else 50
		self.__cost = cost if int_valid(cost) else 15
		self.__shots_delay = shots_delay if int_valid(shots_delay) else 500
		shot_speed = shot_speed if float_valid(shot_speed) else 1
		self.__timer = 0
		self._name = name
		VoicedObj.__init__(self, voices)
		VisualObj.__init__(self, image_dict, position,names.TowerCalmSt)
		self._SHOT = Shot(None, damageUHPDO, position, shot_image_dict, shot_speed, voices = shot_voices)


	def find_target(self):
		target = None
		max_coefficient = 0
		tower_UHPDO = self._SHOT.damage
		for enemy in Tower._Level.get_enemies_list():
			if enemy.position == None: continue
			if tools.distance_cmp_radius(self.position, enemy.position, self.__radius) == 1: continue
			else:
				current_coefficient = tower_UHPDO % enemy.HP
				if current_coefficient > max_coefficient: 
					max_coefficient = current_coefficient
					target = enemy
		self._SHOT.target = target


	def _shot(self):
		Tower._Level.add_shot(self._SHOT.clone())
		self.voice(names.TowerShotVoice)


	def build(self, position):	#USING ONLY FOR CREATING SPECIAL TOWERS, otherwise use function build_tower() at Level object
		new_tower = self.clone()
		new_tower._position = position
		new_tower._SHOT._position = position
		new_tower._SHOT.position = position
		self._SHOT
		if not self._image_dict[names.TowerBuildingSt]: 
			Tower._Level.add_tower(new_tower)
			self.voice(names.TowerBuildEndVoice)
		else:
			def Task(self):
				Tower._Level.add_tower(new_tower)
				Tower.voice(names.TowerBuildEndVoice)
			Tower.voice(names.TowerBuildStartVoice)
			building = FiniteVisualObj(self._image_dict[names.TowerBuildingSt], position, other_task = Task)
			Tower._Level.add_visualObj(building)


	def try_shot(self, dt):
		if self.__timer:							#Если башня перезаряжалась
			self.__timer += dt 						#то добавляем прошедшее время
			if self.__timer >= self.__shots_delay: 	#и проверяем перезарядилась ли она теперь, если да, то:
				self.__timer = 0 					#обнуляем ее таймер перезарядки
				self.try_shot(dt)					#и делаем еще одну попытку выстрела 
													#(заметим, что при этом будет выполнено условие else этой же функции)
		else:					
			enemy_list = Tower._Level.get_enemies_list()	#Если башня перезаряжена, проверяем есть ли у нее цель
			if not enemy_list:
				self._SHOT.target = None
				return
			if (tools.distance_cmp_radius(self.position, self._SHOT.target.position, self.__radius) == 1 or not self._SHOT.target in enemy_list) if self._SHOT.target != None else True:
				self.find_target()						#Если цели нет или есть, но далеко, то пробуем найти новую.
				if self._SHOT.target == None: return		#Ну и если не нашли, то ничего не можем с этим сделать и заканчиваем на этом попытку
			else:
				self.__timer += dt 						#А если же цель есть и башня заряжена, то включаем опять тайминг перезарядки
				self.change_state(names.TowerShootingSt)			#и начинаем анимировать сам выстрел башней,
				self._shot()							#после чего производим сам выстрел


	def visualise(self, display):
		if self._SHOT.target != None:
			self.angle = -tools.offcut_angle(self.position, self._SHOT.target.position)
		VisualObj.visualise(self, display)
		if self.state == names.TowerShootingSt and self._get_counter() == 0: self.change_state(names.TowerCalmSt)


	@classmethod
	def from_resources(cls, name):
		def get_data(directory, mode = 't'):
			file = open(directory, 'r'+mode)
			data = file.read()
			file.close()
			return data

		folder_name = str(name).replace(' ', '_').replace('\t', '_')
		twr_dir = 'resources\\towers\\'+folder_name+'\\'
		img_dir = twr_dir+'sprites'
		sound_dir = twr_dir+'sounds\\'
		try:
			characteristics = [row.split(':') for row in get_data(twr_dir+'characteristics.txt').split('\n')]
			visualisation = [row.split(':') for row in get_data(twr_dir+'visualisation.txt').split('\n')]
			sounds = [row.split(':') for row in get_data(twr_dir+'sounds.txt').split('\n')]
			kwargs = {characteristics[i][0]: int(characteristics[i][1]) for i in range(0,3)}
			kwargs['shot_speed'] = float(characteristics[3][1])
			dmg_list = characteristics[4][1].split(',')
			kwargs['damageUHPDO'] = UHPDO(int(dmg_list[0]), *[float(dmg_list[i]) for i in range(1, 6)])
			kwargs['name'] = name
			for i in range(0,5):
				visualisation[i][1] = visualisation[i][1].split(',')
			kwargs['image_dict'] = {
				names.TowerCalmSt: sprites(visualisation[0][0], visualisation[0][1][0], img_dir, 1, int(visualisation[0][1][1])),
				names.TowerBuildingSt: sprites(visualisation[1][0], visualisation[1][1][0], img_dir, 1, int(visualisation[1][1][1])),
				names.TowerShootingSt: sprites(visualisation[2][0], visualisation[2][1][0], img_dir, 1, int(visualisation[2][1][1]))
			}

			kwargs['shot_image_dict'] = {
				names.ShotFlowSt: sprites(visualisation[3][0], visualisation[3][1][0], img_dir, 1, int(visualisation[3][1][1])),
				names.ShotBlastSt: sprites(visualisation[4][0], visualisation[4][1][0], img_dir, 1, int(visualisation[4][1][1]))
			}

			twr_sounds = {}
			if sounds[0][1] != 'False':
				twr_sounds[names.TowerBuildStartVoice] = pg.mixer.Sound(sound_dir+'.'.join(sounds[0]))
			if sounds[1][1] != 'False':
				twr_sounds[names.TowerBuildEndVoice] = pg.mixer.Sound(sound_dir+'.'.join(sounds[1]))
			if sounds[2][1] != 'False':
				twr_sounds[names.TowerShotVoice] = pg.mixer.Sound(sound_dir+'.'.join(sounds[2]))
			kwargs['voices'] = twr_sounds
			kwargs['shot_voices'] = {names.ShotBlastVoice: pg.mixer.Sound(sound_dir+'.'.join(sounds[3]))} if sounds[3][1]!='False' else{}
			return cls(**kwargs)

		except Exception as error:
			print(error)
			print('Can\'t load tower \''+name+'\' from resources: uncorrect name or tower\'s directory structure was broken.')
			return None
#Towers.init()