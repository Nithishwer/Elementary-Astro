import numpy as np
from numpy import sin
from numpy import cos
from numpy import deg2rad as d2r
from binascii import hexlify

# Importing functions from read_data.py
def process_header(header):
	'''
	A function which processes header in binary format and returns various header
	information in appropriate format.

	Input:
	------
	32-byte string in following sequence:
	MDRDSP(ID) = 8 bytes
	Source Name = 10 bytes
	Attenuator values = 4 bytes
	LO Frequency = 2 bytes
	FPGA Mon = 2 bytes
	GPS count = 2 bytes
	Packet count = 4 bytes

	Output:
	------
	Tuple of form (DSP_id, source_name, att_val, LO_freq, FPGA_Mon, GPSC, packet_count)
	'''
	DSP_id = header[:8].decode('ascii')
	source_name = header[8:18].decode('ascii')
	att_val = header[18:22]
	LO_freq = header[22:24]
	FPGA_Mon = header[24:26]
	GPSC = int(hexlify(header[26:28]), 16)
	packet_count = header[28:]
	return (DSP_id, source_name, att_val, LO_freq, FPGA_Mon, GPSC, packet_count)

def process_data(packet):
	'''
	A fuction which processes body in binary format and returns X and Y polarization
	converted as 8-bit signed integer using 2's complement.

	Input:
	------
	1024-byte string. With alternate X and Y polarizations.

	Output:
	------
	Touple of form (x_polarization, y_polarization)
	'''
	X = []
	Y = []
	for i in range(len(packet)):
		if i%2 == 0:
			X.append(packet[i])
		else:
			Y.append(packet[i])
	return X,Y

def read_mbr_file(filename):
    '''
    This function reads the entire contents of a radio telescope observation
    file and returns headers, x polarizations and y polarizations.

    Input:
    ------

    Name of MBR file

	Output:
	------

    headers : a list of headers of all packets in the tuple format used in read_data.py
    x_pol   : a list of X polarizations of all the packets in the MBR file.
    y_pol   : a list of Y polarizations of all the packets in the MBR file.

    '''
    headers = []
    #x_pol_t1 = []
    #y_pol_t1 = []
    print('Reading Headers of file: ',filename)
    with open(filename, 'rb') as f:
        while True:
            header = f.read(32)
            body = f.read(1024)
            if len(header) < 32:
                break
            else:
                headers.append(process_header(header))
#				processed_packet = process_data(body)
#				x_pol.append(processed_packet[0])
#				y_pol.append(processed_packet[1])
    print('Reading of file ',filename, " complete!\n")
    return headers#,x_pol,y_pol

def cls2hrz(ra,dec,lst,lat,lon):
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

def compute_baseline(lat1,lon1,lat2,lon2):
    e_m_per_lat  =110567
    tc_m_per_lat =110948
    e_m_per_lon = 40075*1000/360
    m_per_lat=( e_m_per_lat+tc_m_per_lat )/2
    x = (lon2-lon1)*cos(lat1)*e_m_per_lon
    y = (lat2-lat1)*m_per_lat
    return (x,y,0)

def source(hor):
    x= cos(hor[0])*cos(hor[1])
    y= cos(hor[0])*sin(hor[1])
    z= sin(hor[0])
    return (x,y,z)

def EW_baseline(b_vec):
    ew_unit=(1,0,0)
    mag = np.dot(b_vec,ew_unit)
    return np.multiply(ew_unit,mag)

def NS_baseline(b_vec):
    ns_unit=(0,1,0)
    mag = np.dot(b_vec,ns_unit)
    return np.multiply(mag,ns_unit)

print("\nScript Running...\n")

#alt_s,az_s = cls2hrz(300,36.466667,800,52.5,12)
#source_vector = source(alt_s,az_s)
#CHD=[30.7046,76.7179]
#PY=[11.9416,79.8083]
#ns_baseline_vector = NS_baseline(baseline_vector)
#ew_baseline_vector = EW_baseline(baseline_vector)

ra_CasA  =300
dec_CasA =36.466667
lat_t1=30.7046
lon_t1=76.7179
lat_t2=11.9416
lon_t2=79.8083

headers_t1=read_mbr_file('cropped_CAS-A_ch03')
headers_t2=read_mbr_file('cropped_CAS-A_ch05')

lst_t1=[]
lst_t2=[]
print("Obtaining LST values from the list of Headers..")
for header in headers_t1:
    lst_t1.append(header[5])
#for header in headers_t2:
#    lst_t2.append(header[5])
print("Obtaining LST values complete!\n")

hor_t1=[]
hor_t2=[]
print("Computing horizontal coordinates of scource from RA,dec,LST,lat & lon..")
for lst_val in lst_t1:
    hor_t1.append(cls2hrz(ra_CasA,dec_CasA,lst_val,lat_t1,lon_t1))
#for lst_val in lst_t2:
#    hor_t2.append(cls2hrz(ra_CasA,dec_CasA,lst_val,lat_t2,lon_t2))
print("Computing horizontal coordinates complete!\n")

srcvecs_t1=[]
srcvecs_t2=[]
print("Computing source vectors from horizontal coordinates..")
for hor_value in hor_t1:
    srcvecs_t1.append(source(hor_value))
#for hor_value in hor_t2:
#    srcvecs_t2.append(source(hor_value))
print("Computing source vectors complete!\n")

print("Computing baseline vectors..")
bsln_vec=compute_baseline(lat_t1,lon_t1,lat_t2,lon_t2)
print("Computing baseline vectors complete!\n")

delay=[]
print("Computing delay from source and baseline vectors..")
for src_vec in srcvecs_t1:
    delay.append(np.dot(src_vec,bsln_vec))
print("Computing delays complete!")
