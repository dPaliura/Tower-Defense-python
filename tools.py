from math import *

def distance_cmp_radius(dot1, dot2, radius):
	distance=0
	for i in range(0, len(dot1)):
		distance +=(dot1[i]-dot2[i])**2
		cmp_expression = distance - radius**2
	return copysign(1, cmp_expression) if cmp_expression else 0

def offcut_angle(looking_dot, observed_dot):
	return degrees(atan2(observed_dot[1]-looking_dot[1], observed_dot[0]-looking_dot[0]))
