import pygame as pg

def sound(src):
	return pg.mixer.Sound(src)


def img(src):
	return pg.image.load(src)

#allows loading arrays of images with names in format: MySprite1.jpg, MySprite2.jpg, MySprite3.jpg, MySprite4.jpg and so on 
def sprites(name, dim, folder = '', first = 1, last = 1):
	result = []
	for i in range(first, last+1): result.append(img(folder + '\\' + name + str(i) + dim))
	return result
'''
sound('l.mp3').play()
pg.time.delay(5000)
#sound('sounds\\2.mp3').play()
input()'''