import numpy as np

def p_s(atmospheric_pressure, water_vapor_pressure = 0.):
#
# both atmospheric_pressure and water_vapor_pressure are input in atmospheres.
# output is converted to millibars
#

	effective_pressure = 760. * 1.333224 * (atmospheric_pressure - water_vapor_pressure)

	return effective_pressure


def p_w(water_vapor_pressure = 0.):
	water_vapor_pressure_millibar = 760. * 1.333224 * water_vapor_pressure
	return water_vapor_pressure_millibar


def d_s(atmospheric_pressure, water_vapor_pressure, temperature):
	# calculate dry air pressure term to refractive index calculation
	T_use = 273.15 + temperature

	return ((1. + p_s(atmospheric_pressure, water_vapor_pressure) * 
		(57.90E-8 - (9.3250E-4 / T_use) + 0.25844 / T_use**2.)) * 
		p_s(atmospheric_pressure, water_vapor_pressure) / T_use)


def d_w(water_vapor_pressure, temperature):
	# calculate water vapor pressure term to refractive index calculation
	T_use =	273.15 + temperature

	return ((1. + p_w(water_vapor_pressure) * (1.+3.7E-4 * p_w(water_vapor_pressure)) * 
		(-2.37321E-3 + (2.23366 / T_use) - (710.792 / T_use**2.) + (7.75141E-4 / T_use**3.))) * 
		p_w(water_vapor_pressure) / T_use)


def n_delta(wavelength, atmospheric_pressure, water_vapor_pressure, temperature):
	# calculate difference of refractive index of air from 1, multiplied by 1E8

	# want wave number in units 1/micron
	# wavelength is input in nm
	wave_num=1E3 / wavelength

	dry_air = 2371.34 + (683939.7 / (130. - wave_num**2.)) + (4547.3 / (38.9 - wave_num**2.))
	wet_air = 6487.31 + 58.058 * wave_num**2. - 0.71150 * wave_num**4. +0.08851 * wave_num**6.

	# print "dry_air"
	# print dry_air
	# print "wet_air"
	# print wet_air

	return (dry_air * d_s(atmospheric_pressure, water_vapor_pressure, temperature) +
		wet_air * d_w(water_vapor_pressure, temperature))


def refraction(zenith_angle, wavelength, atmospheric_pressure, water_vapor_pressure, 
	temperature, latitude = -30.244639, altitude = 2663.):
	
	reduced_n = n_delta(wavelength, atmospheric_pressure, water_vapor_pressure, temperature) * 1E-8

	atmos_scale = 0.001254 * ((273.15 + temperature) / 273.15) # eqn 9 of Stone 1996
	relative_gravity = (1. + 0.005302 * np.sin(np.radians(latitude))**2. + 
		-0.00000583 * np.sin(np.radians(2.*latitude))**2. - 0.000000315 * altitude)

	tanZ = np.tan(np.radians(zenith_angle))

	return np.degrees(reduced_n * relative_gravity * (1. - atmos_scale) * tanZ	+
		reduced_n * relative_gravity * (atmos_scale - reduced_n / 2.) * tanZ**3.)



def diff_refraction(zenith_angle, wavelength, bandwidth = None, atmospheric_pressure = 1., water_vapor_pressure = 0.02,
	temperature = 20. , latitude = -30.244639, altitude = 2663.):
	
	if bandwidth is None: 
		bandwidth = wavelength / 4.
	wavelength_start = wavelength - bandwidth / 2.
	wavelength_end = wavelength + bandwidth / 2.

	refraction_start = refraction(zenith_angle, wavelength_start, atmospheric_pressure, water_vapor_pressure,
		temperature, latitude, altitude)
	refraction_end = refraction(zenith_angle, wavelength_end, atmospheric_pressure, water_vapor_pressure,
		temperature, latitude, altitude)

	return refraction_start - refraction_end	