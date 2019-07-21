from Level import *
import os

clear = lambda: os.system('cls')


def copy_file(source, order, filename, new_filename):
	file = open(source+filename, 'rb')
	data = file.read()
	file.close()
	file = open(order+new_filename, 'wb')
	file.write(data)
	file.close


def copy_sprites(source, order, sprts_name, sprts_format, sprts_amount, sprts_new_name=None):
	if sprts_new_name == None: sprts_new_name = sprts_name
	for i in range(1, sprts_amount + 1):
		copy_file(source, order, sprts_name+str(i)+sprts_format, sprts_new_name+str(i)+sprts_format)


def get_sprites_description(message1, message2, message3, required = False):
	OK = False
	while not OK:
		clear()
		sprt_name = input(message1)
		clear()
		if not required: 
			if sprt_name == '': return ('sprt', '.jpg', 0)
		sprt_format = input(message2)
		clear()
		sprt_amount = input(message3)
		clear()
		if int_valid(sprt_amount): 
			sprt_amount = int(sprt_amount)
			if sprt_amount <= 0: continue 
		else: continue
		try:
			sprites(sprt_name, sprt_format, 'files buffer', 1, sprt_amount)
			OK=True
		except Exception:
			OK = False
	return (sprt_name, sprt_format, int(sprt_amount))


def coeff(summa, dam):
	return dam/summa if summa != 0 else 0
	pass


def get_audio(message):
	while True:
		clear()
		filename = input(message)
		if filename == '': return False
		try:
			file = open('files buffer\\'+filename, 'rb')
			file.close()
			if filename.find('.ogg')>0 or filename.find('.wav')>0:
				return filename
			else: continue
		except Exception:
			continue


def _write_tower(twr_name, twr_radius, shots_delay, twr_cost, shot_speed, damage,
	twr_calm_sprts, twr_building_sprts, twr_shooting_sprts,shot_flow_sprts, shot_blast_sprts,
	twr_build_start_sound, twr_build_end_sound, twr_shooting_sound, shot_hit_sound):
	twr_dir = 'resources\\towers\\'+twr_name
	buff_dir = 'files buffer\\'
	os.system('md '+twr_dir)
	os.system('md '+twr_dir+'\\sprites')
	os.system('md '+twr_dir+'\\sounds')
	#write characteristics of tower to a file:
	file = open(twr_dir+'\\characteristics.txt', 'wt')
	file.write('radius:'+str(twr_radius)+'\n')
	file.write('shots_delay:'+str(shots_delay)+'\n')
	file.write('cost:'+str(twr_cost)+'\n')
	file.write('shot_speed:'+str(shot_speed)+'\n')
	file.write('damage:'+str(damage).replace('(','').replace(')','')+'\n')
	file.close()
	sprts_dir = twr_dir+'\\sprites\\'
	#copying sprites to our directory
	copy_sprites(buff_dir, sprts_dir, twr_calm_sprts[0], twr_calm_sprts[1], twr_calm_sprts[2], 'calm')
	copy_sprites(buff_dir, sprts_dir, twr_building_sprts[0], twr_building_sprts[1], twr_building_sprts[2], 'build')
	copy_sprites(buff_dir, sprts_dir, twr_shooting_sprts[0], twr_shooting_sprts[1], twr_shooting_sprts[2], 'shooting')
	copy_sprites(buff_dir, sprts_dir, shot_flow_sprts[0], shot_flow_sprts[1], shot_flow_sprts[2], 'shot_flow')
	copy_sprites(buff_dir, sprts_dir, shot_blast_sprts[0], shot_blast_sprts[1], shot_blast_sprts[2], 'shot_blast')
	#write numbers and formats of sprites to a file:
	file = open(twr_dir+'\\visualisation.txt', 'wt')
	file.write('calm:'+str(twr_calm_sprts[1])+','+str(twr_calm_sprts[2])+'\n')
	file.write('build:'+str(twr_building_sprts[1])+','+str(twr_building_sprts[2])+'\n')
	file.write('shooting:'+str(twr_shooting_sprts[1])+','+str(twr_shooting_sprts[2])+'\n')
	file.write('shot_flow:'+str(shot_flow_sprts[1])+','+str(shot_flow_sprts[2])+'\n')
	file.write('shot_blast:'+str(shot_blast_sprts[1])+','+str(shot_blast_sprts[2])+'\n')
	file.close()
	#copying sounds to our directory
	sounds_dir = twr_dir+'\\sounds\\'
	if twr_build_start_sound: copy_file(buff_dir, sounds_dir, twr_build_start_sound, 'build_start.'+twr_build_start_sound.split('.')[-1])
	if twr_build_end_sound: copy_file(buff_dir, sounds_dir, twr_build_end_sound, 'build_end.'+twr_build_end_sound.split('.')[-1])
	if twr_shooting_sound: copy_file(buff_dir, sounds_dir, twr_shooting_sound, 'shooting.'+twr_shooting_sound.split('.')[-1])
	if shot_hit_sound: copy_file(buff_dir, sounds_dir, shot_hit_sound, 'shot_hit.'+shot_hit_sound.split('.')[-1])
	#write information about sounds to a file:
	file = open(twr_dir+'\\sounds.txt', 'wt')
	file.write('build_start:'+(str(twr_build_start_sound.split('.')[-1]) if twr_build_start_sound else 'False') +'\n')
	file.write('build_end:'+(str(twr_build_end_sound.split('.')[-1]) if twr_build_end_sound else 'False') +'\n')
	file.write('shooting:'+(str(twr_shooting_sound.split('.')[-1]) if twr_shooting_sound else 'False') +'\n')
	file.write('shot_hit:'+(str(shot_hit_sound.split('.')[-1]) if shot_hit_sound else 'False'))
	file.close()


def create_tower_model():
	OK = False
	other_sentence = 'or just press Enter to fill it as default\n'
	print('Make sure, that all files (sprites and sounds) where \n'+
		'added to folder \'files buffer\'')
	input('press Enter to continue\n')
	clear()
	while not OK:
		tower_name = input('Enter name of new tower\n').replace(' ', '_').replace('\t', '_')
		OK = True if len(tower_name) > 2 else False
		clear()
	OK = False
	while not OK:
		tower_radius = input('Enter firing radius (pixels) of your tower \'' + tower_name+'\' (by default 500)\n'+other_sentence)
		if len(tower_radius) == 0: tower_radius = 50
		if int_valid(tower_radius):
			tower_radius = int(tower_radius)
			OK = True if tower_radius>=50 else False
		clear()
	OK = False
	while  not OK:
		tower_shots_delay = input('Enter time delay (miliseconds) between each \n'+
			'two shots of your tower (by default 1000)\n'+other_sentence)
		if len(tower_shots_delay) == 0: tower_shots_delay = 1000
		if int_valid(tower_shots_delay):
			tower_shots_delay = int(tower_shots_delay)
			OK = True if tower_shots_delay >=35 else False
		clear()
	OK = False
	while not OK:
		tower_cost = input('Enter the cost of your tower \'' + tower_name+'\' (by default 15)\n' + other_sentence)
		if len(tower_cost) == 0: tower_cost = 15
		if int_valid(tower_cost):
			tower_cost = int(tower_cost)
			OK = True if tower_cost > 0 else False
		clear()
	OK = False
	while not OK:
		shot_movement_speed = input('Enter coefficient for shot\'s movement speed (by default 1)\n'+
			'(recomended to be set as default)\n'+other_sentence)
		if len(shot_movement_speed) == 0: shot_movement_speed = 1
		if float_valid(shot_movement_speed):
			shot_movement_speed = float(shot_movement_speed)
			OK = True if shot_movement_speed > 0 else False
		clear()
	input('Next step: bulding tower\'s damage.\n'+
			'Now you have to input 5 not-negative numbers,\n'+
			'which are match 5 types of damage.\n'+
			'Notice that at least one damage must be positive\n'+
			'Press Enter to continue\n')
	clear()
	summa = 0
	while not summa:
		summa = 0
		damages = []
		for i in range(0, 5):
			OK = False
			while not OK:
				new_one = input('Damage type '+str(i+1)+': set it\'s value\n')
				if float_valid(new_one):
					new_one = float(new_one)
					if new_one >= 0:
						summa += new_one
						damages.append(new_one)
						OK = True
				clear()
		summa = int(summa)
	damage = (summa, coeff(summa,damages[0]), coeff(summa,damages[1]), coeff(summa,damages[2]), coeff(summa,damages[3]), coeff(summa,damages[4]))
	mssg2 = 'Enter format of sprites\' files\n'
	mssg3 = 'And enter amount of them\n'

	mssg1_1 = 'Enter the name of sprites for visualisation '
	mssg1_2 = 'If you have no sprites, you can press Enter and skip this step.\n'
	mssg1_3 = 'Those sprites are required\n'

	input('Now the penult step: visualisation of your tower.\nPress Enter to start this step\n')
	clear()

	tower_calm_sprts = get_sprites_description('1) '+mssg1_1+'calm state of your tower.\n'+mssg1_3, mssg2, mssg3, True)
	tower_building_sprts = get_sprites_description('2) '+mssg1_1+'process of building tower.\n'+mssg1_2, mssg2, mssg3)
	tower_shooting_sprts = get_sprites_description('3) '+mssg1_1+'shooting state of your tower.\n'+mssg1_2, mssg2, mssg3)
	tower_shot_flow_sprts = get_sprites_description('4) '+mssg1_1+'flowing state of bullet\nwich was shot by your tower.\n'+mssg1_3, mssg2, mssg3, True)
	tower_shot_blast_sprts = get_sprites_description('5) '+mssg1_1+'blast of this bullet when it hits the enemy.\n'+mssg1_2, mssg2, mssg3)
	if input('And now the last step: sounds.\nYou can make your tower voiceless by entering word \'cancel\'\nNotice that all sound files must have format .ogg or .wav\n').lower() == 'cancel':
		tower_build_start_sound = False
		tower_build_end_sound = False
		tower_shooting_sound = False
		tower_shot_hit_sound = False
	else:
		skip_mssg = 'Or press Enter to skip this sound\n'
		tower_build_start_sound = get_audio('1) Enter full filename of sound displaying beggining of building tower.\n'+skip_mssg) 
		tower_build_end_sound = get_audio('2) Enter full filename of sound displaying ending of building tower.\n'+skip_mssg)
		tower_shooting_sound = get_audio('3) Enter full filename of sound displaying shot of tower.\n'+skip_mssg)
		tower_shot_hit_sound = get_audio('4) Enter full filename of sound displaying shot hits enemy.\n'+skip_mssg)
	clear()
	print('Now information about your tower is writing to our filesystem.\n'+
		'Don\'t close the programm and delete any files from \n'+
		'folder \'files buffer\' until process ends.\n')
	_write_tower(tower_name, tower_radius, tower_shots_delay, tower_cost, shot_movement_speed, #tower characteristics
				damage,	#tower damage
				tower_calm_sprts, tower_building_sprts, tower_shooting_sprts,	#visualisation of tower
				tower_shot_flow_sprts, tower_shot_blast_sprts,					#visualisation of tower's bullet
				tower_build_start_sound,#tower's sounds
				tower_build_end_sound,
				tower_shooting_sound,	
				tower_shot_hit_sound)	#tower's bulet's sounds
	clear()
	input('\nPROCESS IS OVER\n\nPress Enter to finish')


def _write_enemy(name, reward, speed, HP_UHPDO, run_sprts, die_sprts, hit_sound, die_sound, pass_sound):
	enemy_dir = 'resources\\enemies\\'+name
	buff_dir = 'files buffer\\'
	os.system('md '+enemy_dir)
	os.system('md '+enemy_dir+'\\sprites')
	os.system('md '+enemy_dir+'\\sounds')
	#write characteristics of enemy to a file:
	file = open(enemy_dir+'\\characteristics.txt', 'wt')
	file.write('reward:'+str(reward)+'\n')
	file.write('speed:'+str(speed)+'\n')
	file.write('HP:'+str(HP_UHPDO).replace('(','').replace(')','')+'\n')
	file.close()
	sprts_dir = enemy_dir+'\\sprites\\'
	#copying sprites to our directory
	copy_sprites(buff_dir, sprts_dir, run_sprts[0], run_sprts[1], run_sprts[2], names.EnemyRunSt)
	copy_sprites(buff_dir, sprts_dir, die_sprts[0], die_sprts[1], die_sprts[2], names.EnemyDyingSt)
	#write numbers and formats of sprites to a file:
	file = open(enemy_dir+'\\visualisation.txt', 'wt')
	file.write(names.EnemyRunSt+':'+str(run_sprts[1])+','+str(run_sprts[2])+'\n')
	file.write(names.EnemyDyingSt+':'+str(die_sprts[1])+','+str(die_sprts[2])+'\n')
	#copying sounds to our directory
	sounds_dir = enemy_dir+'\\sounds\\'
	if hit_sound: copy_file(buff_dir, sounds_dir, hit_sound, 'enemy_hit.'+hit_sound.split('.')[-1])
	if die_sound: copy_file(buff_dir, sounds_dir, die_sound, 'enemy_die.'+die_sound.split('.')[-1])
	if pass_sound: copy_file(buff_dir, sounds_dir, pass_sound, 'enemy_pass.'+pass_sound.split('.')[-1])
	#write information about sounds to a file:
	file = open(enemy_dir+'\\sounds.txt', 'wt')
	file.write('enemy_hit:'+(str(hit_sound.split('.')[-1]) if hit_sound else 'False') +'\n')
	file.write('enemy_die:'+(str(die_sound.split('.')[-1]) if die_sound else 'False') +'\n')
	file.write('enemy_pass:'+(str(pass_sound.split('.')[-1]) if pass_sound else 'False') +'\n')
	file.close()


def create_enemy_model():#name, reward, speed, HealthUHPDO, image_dict, voices
	OK = False
	other_sentence = 'or just press Enter to fill it as default\n'
	print('Make sure, that all files (sprites and sounds) where \n'+
		'added to folder \'files buffer\'')
	input('press Enter to continue\n')
	clear()
	while not OK:
		enemy_name = input('Enter NAME of your new enemy\n').replace(' ', '_').replace('\t', '_')
		OK = True if len(enemy_name) > 0 else False
		clear()
	OK = False
	while not OK:
		reward = input('Enter REWARD FOR KILLING your enemy \'' + enemy_name+'\' (by default 2)\n'+other_sentence)
		if len(reward) == 0: reward = 2
		if int_valid(reward):
			reward = int(reward)
			OK = True if reward>=0 else False
		clear()
	OK = False

	while not OK:
		movement_speed = input('Enter coefficient for enemie\'s MOVEMENT SPEED (by default 0.5)\n'+
			'(recomended to be set between 0.2 and 1)\n'+other_sentence)
		if len(movement_speed) == 0: movement_speed = 0.5
		if float_valid(movement_speed):
			movement_speed = float(movement_speed)
			OK = True if movement_speed > 0 else False
		clear()
	OK = False
	input('Next step: bulding enemy HIT POINTS\n'+
			'Now you have to input 1 not-negative number and 5 real numbers no more than 1,\n'+
			'which are match full enemy HP and 5 coefficients\n'+
			'of resistance to 5 types of damage.\n\n'+
			'All coefficients must have values less then 1\n'+
			'1 means that enemy has total invulnerability to this damage.\n'+
			'0 - enemy has no resistance to this damage\n'+
			'less than 0 means that enemy is vulnerable to this damage (be careful using it)\n'+
			'Notice that at least one coefficient must be less than 1\n'+
			'and enemy must have more than 0 HP\n'+
			'Press Enter to continue\n')
	clear()
	while not OK:
		full_HP = input('Enter AMOUNT of enemy HIT POINTS (more than 0).\n')
		if int_valid(full_HP):
			full_HP = int(full_HP)
			OK = True if full_HP > 0 else False
		clear()
	OK = False
	while not OK:
		coefficients = []
		for i in range(0, 5):
			OK1 = False
			while not OK1:
				new_one = input('RESISTANCE to damage type '+str(i+1)+': set it\'s value\n')
				if float_valid(new_one):
					new_one = float(new_one)
					if new_one <= 1:
						coefficients.append(new_one)
						OK1 = True
						clear()
			OK = True if sum(coefficients) < 5 else False
	
	HP = tuple([full_HP] + [1 - coeff for coeff in coefficients])
	mssg2 = 'Enter FORMAT of sprites\' files\n'
	mssg3 = 'And enter AMOUNT of them\n'

	mssg1_1 = 'Enter the NAME of sprites for visualisation '
	mssg1_2 = 'If you have no sprites, you can press Enter and skip this step.\n'
	mssg1_3 = 'Those sprites are REQUIRED\n'

	input('Now the penult step: visualisation of your tower.\nPress Enter to start this step\n')
	clear()

	enemy_run_sprts = get_sprites_description('1) '+mssg1_1+'\nenemy just WHILE MOVING on the way.\n'+mssg1_3, mssg2, mssg3, True)
	enemy_die_sprts = get_sprites_description('2) '+mssg1_1+'DYING enemy.\n'+mssg1_2, mssg2, mssg3)

	if input('And now the last step: sounds.\nYou can make your enemy voiceless by entering word \'cancel\'\nNotice that all sound files must have format .ogg or .wav\n').lower() == 'cancel':
		enemy_hit_sound = False
		enemy_die_sound = False
		enemy_pass_sound = False
	else:
		skip_mssg = 'Or press Enter to skip this sound\n'
		enemy_hit_sound = get_audio('1) Enter full filename of sound displaying enemy REACTION FOR HIT\n'+skip_mssg) 
		enemy_die_sound = get_audio('2) Enter full filename of sound displaying enemy DEATH.\n'+skip_mssg)
		enemy_pass_sound = get_audio('3) Enter full filename of sound when enemy PASSED ALL PATH.\n'+skip_mssg)
	clear()
	print('Now information about your enemy is writing to our filesystem.\n'+
		'Don\'t close the programm and delete any files from \n'+
		'folder \'files buffer\' until process ends.\n')
	_write_enemy(enemy_name, reward, movement_speed, HP,
		enemy_run_sprts, enemy_die_sprts,
		enemy_hit_sound, enemy_die_sound, enemy_pass_sound)
	input('\nPROCESS IS OVER\n\nPress Enter to finish')


chosen = False
while not chosen:
	clear()
	choose = input('Enter\n1 - to create new enemy\n2 - to create new tower\n')
	chosen = True if choose in ['1', '2'] else False
clear()
if choose == '1': 
	create_enemy_model()
elif choose == '2':
	create_tower_model()