import numpy as np


def gelman_rubin(x, return_var=False):
	if np.shape(x) < (2,):
		raise ValueError(
			'Gelman-Rubin diagnostic requires multiple chains of the same length.')

	try:
		m, n = np.shape(x)
	except ValueError:
		print(np.shape(x))
		return [gelman_rubin(np.transpose(y)) for y in np.transpose(x)]

	# Calculate between-chain variance
	B_over_n = np.sum((np.mean(x, 1) - np.mean(x)) ** 2) / (m - 1)

	# Calculate within-chain variances
	W = np.sum(
		[(x[i] - xbar) ** 2 for i,
		 xbar in enumerate(np.mean(x,
								   1))]) / (m * (n - 1))

	# (over) estimate of variance
	s2 = W * (n - 1) / n + B_over_n

	if return_var:
		return s2

	# Pooled posterior variance estimate
	V = s2 + B_over_n / m

	# Calculate PSRF
	R = V / W

	return np.sqrt(R)

def GL_converg(numb_param, list_cbrs, parameter_names):
	import readwritebinary as rwbin

	INFO = {'nopars':numb_param, 'latterhalf':0}
	flag =1
	for parname in parameter_names:
		list_of_values = []
		for cbr in list_cbrs:
			cbr_load = rwbin.read_cbr_file(cbr,  INFO = INFO)
			if parname == 'Bday' or parname == 'Fday':
				value = np.mod(cbr_load[-500:,parameter_names.index(parname)], 365.25)
			else:
				value = cbr_load[-500:,parameter_names.index(parname)]
			list_of_values.append(list(value))
		gr = gelman_rubin(list_of_values)
		if gr > 1.05:
			print(f'{parname:25} ==> {gr:2.4}')
			flag =0
	if flag:
		print('All parameters converge with GR metric < 1.05')
