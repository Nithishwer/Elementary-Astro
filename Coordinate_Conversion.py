import numpy as np
from numpy import sin
from numpy import cos
from numpy import deg2rad as d2r
from binascii import hexlify

def cls2hrz(ra,dec,lst,lat,lon):
    '''
	A fuction which converts celestial coordinates to horizontal coordinates.

	Input:
	------
	ra  - The Right ascension of the object.
    dec - The declination of the object.
    lst - The local sidereal time .
    lat - The latitude of the place of observation.
    lon - The longitude of the place of observation.

	Output:
	------
	Touple of form (altitude, azimuthal)

	'''
    ha=lst-ra
    ha=54.382617
    if(ha>360):
        ha=ha-360
        print("HA is ",ha)
    if(ha<0):
        ha=ha+360
        print("HA is ",ha)
    sin_dec= sin(d2r(dec))
    sin_lat= sin(d2r(lat))
    cos_dec= cos(d2r(dec))
    cos_lat= cos(d2r(lat))
    cos_ha = cos(d2r(ha))
    sin_ha = sin(d2r(ha))
    sin_alt= sin_dec*sin_lat+cos_dec*cos_lat*cos_ha
    alt = np.rad2deg(np.arcsin(sin_alt))
    cos_alt=cos(d2r(alt))
    cosA=(sin_dec-sin_alt*sin_lat)/(cos_alt*cos_lat)
    A=np.rad2deg(np.arccos(cosA))
    #print("A = ",A)
    if(sin_ha>0):
        az=360-A
    else:
        az=A
    #print("alt = ",alt)
    #print("az = ",az)
    return (alt,az)
