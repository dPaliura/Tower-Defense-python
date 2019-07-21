from DamageMechanic import *
from VoicedObjects import *

class EnemyModel():
	def __init__(self, HealthUHPDO, image_dict, reward=5, name=names.EnemyDefaultName, speed=1, voices={}):
		self._HP = HealthUHPDO if type(HealthUHPDO) == UHPDO else UHPDO(10)
		self._reward = reward if int_valid(reward) else 5
		vals = self.__dict__.values()
		if not image_dict in vals: self._image_dict = image_dict
		self._name = str(name)
		self._speed = speed
		if not voices in vals: self._voices = voices


	def __get_HP(self):
		return self._HP
		pass
	def __set_HP(self, value):
		if type(value) == UHPDO and value.HitPoints > 0: self._HP = value
		pass
	HP = property(__get_HP, __set_HP)


	def __get_name(self):
		return self._name
		pass
	def __set_name(self, value):
		pass
		pass
	name = property(__get_name, __set_name)


	def __get_reward(self):
		return self._reward
		pass
	def __set_reward(self, value):
		pass
		pass
	reward = property(__get_reward, __set_reward)

	

class Enemy(MovingObj, EnemyModel, VoicedObj, Cloner):
	def __init__(self, HealthUHPDO, path, image_dict, reward=5, name=names.EnemyDefaultName, speed=1, state = None, t = None, voices={}):
		MovingObj.__init__(self, path, image_dict, state, t, speed)
		if not names.EnemyDyingSt in self._image_dict.keys(): self._image_dict[names.EnemyDyingSt] = []
		EnemyModel.__init__(self, HealthUHPDO, image_dict, reward, name, speed, voices)
		VoicedObj.__init__(self, voices)


	def remove(self):
		self._HP = None
		Enemy._Level.add_enemy_to_trash(self)


	def die(self):
		self.remove()
		self.voice(names.EnemyDyingVoice)
		Enemy._Level.add_visualObj(FiniteVisualObj(self._image_dict[names.EnemyDyingSt], self.position, self.angle))
		Enemy._Level.recieve_reward(self)
		#not ended method


	def end_move(self, dt):
		self._Level._player_HP -= 1
		self.voice(names.EnemyPassedVoice)
		self.remove()

	def hit(self, shot):
		if self._HP != None: self._HP -= shot
		if not self._HP.isalive(): self.die()
		else: self.voice(names.EnemyHitVoice)
		#not ended method

	@classmethod
	def from_resources(cls, name):
		def get_data(directory, mode = 't'):
			file = open(directory, 'r'+mode)
			data = file.read()
			file.close()
			return data

		folder_name = str(name).replace(' ', '_').replace('\t', '_')
		enemy_dir = 'resources\\enemies\\'+folder_name+'\\'
		img_dir = enemy_dir+'sprites'
		sound_dir = enemy_dir+'sounds\\'

		try:
			characteristics = [row.split(':') for row in get_data(enemy_dir+'characteristics.txt').split('\n')]
			visualisation = [row.split(':') for row in get_data(enemy_dir+'visualisation.txt').split('\n')]
			sounds = [row.split(':') for row in get_data(enemy_dir+'sounds.txt').split('\n')]

			kwargs = {	characteristics[0][0]: int(characteristics[0][1]),
						characteristics[1][0]: float(characteristics[1][1])}
			HP_list = characteristics[2][1].split(',')
			kwargs['HealthUHPDO'] = UHPDO(int(HP_list[0]), *[float(HP_list[i]) for i in range(1, 6)])
			kwargs['name'] = name
			for i in range(0,2):
				visualisation[i][1] = visualisation[i][1].split(',')
			kwargs['image_dict'] = {
				names.EnemyRunSt: sprites(visualisation[0][0], visualisation[0][1][0], img_dir, 1, int(visualisation[0][1][1])),
				names.EnemyDyingSt: sprites(visualisation[1][0], visualisation[1][1][0], img_dir, 1, int(visualisation[1][1][1]))
			}

			enemy_sounds = {}
			if sounds[0][1] != 'False':
				enemy_sounds[names.EnemyHitVoice] = pg.mixer.Sound(sound_dir+'.'.join(sounds[0]))
			if sounds[1][1] != 'False':
				enemy_sounds[names.EnemyDyingVoice] = pg.mixer.Sound(sound_dir+'.'.join(sounds[1]))
			if sounds[2][1] != 'False':
				enemy_sounds[names.EnemyPassedVoice] = pg.mixer.Sound(sound_dir+'.'.join(sounds[2]))
			kwargs['voices'] = enemy_sounds

			kwargs['path'] = None
			kwargs['state'] = names.EnemyRunSt
			kwargs['t'] = 0
			return cls(**kwargs)

		except Exception as error:
			print(error)
			print('Can\'t load tower \''+name+'\' from resources: uncorrect name or tower\'s directory structure was broken.')
			return None
		#name, HealthUHPDO, reward, speed, image_dict, voices
	
#Enemy.init()