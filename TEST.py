from Level import *

pg.init()
window = pg.display.set_mode((1000, 700))


path2 = PathList.create_by_points([(1000,300),(800,350),(700,300),(600,350),(500,300),(400,350),(300,300),(200,350),(100,300),(10,350)][::-1])
run_list = sprites('', '.png', 'sprts', 1, 6)
imgDict = {
	'run': run_list,
	'die': sprites('destroy', '.png', 'sprts', 1, 7)
}
shot_img_dict = {
	'flow': sprites('shot', '.png', 'sprts', 1, 6),
	'blast': sprites('blast', '.png', 'sprts', 1, 7)
}
crtr = WaveCreator(path2, 1200)
#Arrow = EnemyModel(UHPDO(25), imgDict, name='Arrow', speed = 0.5)
#Arrow.load_voice(names.EnemyDyingVoice, 'sounds\\maslina.ogg')
wave = crtr.create(Enemy.from_resources('pinky'), 12)


twr3 = Tower.from_resources('pac-man')
lvl = Level(window, wave, {twr3})
lvl.init_dependencies()
lvl.build_tower('pac-man', (450, 40))
lvl.build_tower('pac-man', (900, 450))
#lvl.build_tower('distant raper', (500, 50))
#lvl.build_tower('fast fucker', (400, 400))
#lvl.build_tower('fast fucker', (420, 420))
My_clock = pg.time.Clock()
def go():
	dt = 32
	fps = 1000/dt
	while True: 
		lvl.update(dt)
		pg.display.update()
		My_clock.tick_busy_loop(fps)
go()
try:
	
	
	pass
except WaveCreationPathError:
	print('WaveCreator.create method\'s attribute path must have PathList type')
except WaveCreationEnemyModelTypeError:
	print('WaveCreator.create method\'s attribute enemy must have EnemyModel type')
except Exception as err:
	pass
	#print(repr(err))
input()
#fps = second / dt   dt = second/fps