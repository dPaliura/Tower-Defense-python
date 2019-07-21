from Enemies import *

class WaveCreationPathError(Exception):
	pass

class WaveCreationEnemyModelTypeError(TypeError):
	pass


class WaveCreator():
	def __init__(self, path, period=500):
		if type(path) is PathList: self._path = path
		else:
			raise WaveCreationPathError
		self._period = period

	def create(self, enemy, count, state=names.EnemyRunSt):
		if not (type(enemy) in [EnemyModel, Enemy]): 
			print(enemy)
			raise WaveCreationEnemyModelTypeError
		return [Enemy(enemy.HP, self._path, enemy._image_dict, enemy.reward, enemy.name, enemy._speed, state, -i*self._period, enemy._voices) for i in range(0, count)]