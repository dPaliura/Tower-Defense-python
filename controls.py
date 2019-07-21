import pygame as pg


class controls:
	__top_row_of_chars = [pg.K_Q, pg.K_W, pg.K_E, pg.K_R, pg.K_T, pg.K_Y, pg.K_U, pg.K_I, pg.K_O, pg.K_P]
	__row_of_numbers = [i for i in range(pg.K_1, pg.K_0)] + [pg.K_0]

	def __init__(self, chars_mode = False, pause = pg.K_SPACE, change_fire = pg.K_LALT, change_playback_speed = pg.K_LSHIFT,):
