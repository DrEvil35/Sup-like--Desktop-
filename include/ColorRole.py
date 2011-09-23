#coding:utf-8

DEFAULT=0x2

CAHT=0x1

DONATE_COLOR=(
	8421504,
	8388608,
	8388736,
	8421376,
	16753920,
	128,
	4177599
)

COLOR_DEP=(65535)

COLOR_BOY={
	0x1:5405117,
	0x2:3780326
}
COLOR_GIRL={
	0x1:16746412,
	0x2:16739996
}

COLOR_GREEN=6737012

COLOR_BLACK=2505037

COLOR_BLUE=1004185

COLOR_BORDE=10881085

GREE_USER=('v_43768752')

def TrueColor(_id,_color=None,male=None,ischat=default):
	return(_color and color(_color)  or colorRole(_id) or
			(male and (colorTop(_id,male) or '1'==male and COLOR_BOY[ischat] or COLOR_GIRL[ischat]) or COLOR_GIRL[ischat]))

def color(arg):
	if arg=='0':
		return None
	try:
		arg=int(arg)
	except ValueError:
		return None
	if arg in DONATE_COLOR:
		return arg
	elif arg in COLOR_DEP:
		return 4177599
	else :
		return None

def colorRole(Id):
	return (Id in GREE_USER and COLOR_GREEN or None)

def colorTop(id,male='0'):
	return None 
