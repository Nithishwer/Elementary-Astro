import numpy as np
from numpy import sin
from numpy import cos
from numpy import deg2rad as d2r
from binascii import hexlify

def compute_baseline(lat1,lon1,lat2,lon2):
    '''
	A fuction to compute the baseline vector between two telescopes
    in the East-North-Up coordinate system.

	Input:
	------
	lat1 - The latitude of telescope 1.
    lon1 - The longitude of telescope 1.
    lat1 - The latitude of telescope 2.
    lon1 - The longitude of telescope 2.

	Output:
	------
	Tuple of form (x,y,z)
	'''
    e_m_per_lat  =110567
    tc_m_per_lat =110948
    e_m_per_lon = 40075*1000/360
    m_per_lat=( e_m_per_lat+tc_m_per_lat )/2
    x = (lon2-lon1)*cos(lat1)*e_m_per_lon
    y = (lat2-lat1)*m_per_lat
    return (x,y,0)

def source(hor):
	'''
	A fuction to compute the source vector of an astronomical object in
    the East-North-Up coordinate system.

	Input:
	------
	hor - coordinates of the object in a tuple of the form:
    (altitude, azimuthal)

	Output:
	------
	Tuple of form (x,y,z)

	'''
    x= cos(hor[0])*cos(hor[1])
    y= cos(hor[0])*sin(hor[1])
    z= sin(hor[0])
    return (x,y,z)

def EW_baseline(b_vec):
    '''
	A fuction to compute the East-West component of the baseline vector
    between two telescopes in the East-North-Up coordinate system.

	Input:
	------
	b_vec - Baseline vector in the EWU coordinate system.

	Output:
	------
	Tuple of the form (x,y,z)

	'''
    ew_unit=(1,0,0)
    mag = np.dot(b_vec,ew_unit)
    return np.multiply(ew_unit,mag)

def NS_baseline(b_vec):
    '''
	A fuction to compute the North-South component of the baseline vector
    between two telescopes in the East-North-Up coordinate system.

	Input:
	------
	b_vec - Baseline vector in the EWU coordinate system.

	Output:
	------
	Tuple of the form (x,y,z)

	'''
    ns_unit=(0,1,0)
    mag = np.dot(b_vec,ns_unit)
    return np.multiply(mag,ns_unit)
