from MovingObjects import *

class VoicedObj:
	pg.mixer.init()
	pg.mixer.set_num_channels(20)
	def __init__(self, voices = {}):
		self._voices = voices


	def voice(self, voice_name):
		if voice_name in self._voices.keys():
			self._voices[voice_name].play()
		else:
			print('sound '+voice_name+' is not set')


	def change_voice(self, voice_name, new_voice):
		self._voices[voice_name] = new_voice
		pass


	def add_voice(self, voice_name, voice):
		if voice_name in self._voices.keys(): return
		self._voices[voice_name] = voice


	def load_voice(self, voice_name, directory):
		try:
			new_voice = pg.mixer.Sound(directory)
			self._voices[voice_name] = new_voice
			return True
		except Exception:
			print('can\'t load sound as file '+directory+'\nperhaps directory is False or unsuported format (must be .ogg or .wav)')
			return False
'''print(pg.mixer.get_num_channels())
print(pg.mixer.get_busy())
my_Voices = VoicedObj()
my_Voices.load_voice('song', 'sounds\\1.ogg')
my_Voices.load_voice('tresh', 'sounds\\2.ogg')
my_Voices.voice('song')
print(pg.mixer.get_num_channels())
print(pg.mixer.get_busy())
while True:
	my_Voices.voice('tresh')
	pg.time.delay(15000)
	pass
input()'''