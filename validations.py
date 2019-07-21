def int_valid(number):
	try: int(number)
	except Exception: 
		print('Rised exception in int validation of', number)
		return False
	else: return True

def float_valid(number):
	try: float(number)
	except Exception: 
		print('Rised exception in float validation of', number)
		return False
	else: return True

def isiterable(obj):
	try: 
		for key in obj: break
	except Exception: 
		print('Rised exception while trying to iterate', obj)
		return False
	else: return True
