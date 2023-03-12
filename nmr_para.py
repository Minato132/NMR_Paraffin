import numpy as np
import scipy.optimize as py
import matplotlib.pyplot as plt
import pandas as pd


def T1(t, a, b, c, d):
	y = 1 - np.exp(-1/b * t + c) + d  
	return y


def T2(t, a, b, c, d):
	y = np.exp(-1/b * t + c) +d
	return y

def T2p(t, a, b, c, d):
	y = np.exp(-1/b * t + c) + d
	return y 

def param_get(ar1, ar2, func, err):
	a, b = py.curve_fit(func, ar1, ar2, sigma = err, method = 'trf')
	return a, b 


#________________________________u can suck on deez nuts,,,,,,,,,huuuuuhhhhhhh.........NOT LIKE THAT NOT MINE f ...........DAYUUUM GURL........... ITS OKAY EVERYONE WANTS TO SUCK ON DEEZ NUTS *shock pikachuface__________________sorry me and my brother are just super fun fresh and aesthetic siblings ......cap______built difffffff_________________

#Measurement of T1 of Paraffin Oil

with open('/home/minato132/Documents/Data/para/para_t1') as file:
	data = pd.read_csv(file)
	data.drop(data.loc[:, 'Unnamed: 2':], axis = 1, inplace = True)
	data = data.rename(columns = {'t ms':'time', 'Amplitude':'amp'})
	data.loc[:19, 'amp'] = -1 * data.loc[:19, 'amp']

error = []
for i in data['amp']:
	if i < 0:
		i *= -.01
	else:
		i *= .01
	error.append(i)



def t1(ar1, ar2, ar3):
	a, b = param_get(ar1, ar2, T1, ar3)

	plt.errorbar(ar1, ar2, yerr = ar3, fmt = ',', color = 'green', label = 'Error')
	plt.scatter(ar1, ar2, marker = 'x', color = 'purple', label = 'Data')
	plt.plot(ar1, T1(ar1,*a), color = 'red', label = 'Fitted Data')
	plt.xlabel('Time (ms)')
	plt.ylabel('Maximum Amplitude')
	plt.title('T1 of Paraffin Oil')
	plt.legend()

	print(*a, f'\n Error of b is {np.sqrt(b[1,1])}')
	plt.show()
	return 0 

#print(t1(data['time'],data['amp'], error))





#________________________________________________________________________

#Measurement of T2 of Paraffin Oil

with open('/home/minato132/Documents/Data/para/para_t2') as file:
	data = pd.read_csv(file)
	data.drop(data.loc[:, 'Unnamed: 2':], axis = 1, inplace = True)
	data = data.rename(columns = {'t us' : 'time', 'amp (V)' : 'amp'})
	data['time'] = data['time'] / 1000


error = []
for i in data['amp']:
	i *= .01
	error.append(i)


def t2(ar1, ar2, ar3):
	a, b = param_get(ar1, ar2, T2, ar3)

	plt.errorbar(ar1, ar2, yerr = ar3, fmt = ',', color = 'green', label = 'Error')
	plt.scatter(ar1, ar2, marker = 'x', color = 'purple', label = 'Data')
	plt.plot(ar1, T2(ar1, *a), color = 'red', label = 'Fitted Data')
	plt.xlabel('Time(ms)')
	plt.ylabel('Voltage (v)')
	plt.title('T2 of Paraffin Oil')
	plt.legend()

	print(*a, f'\n Error of b is {np.sqrt(b[1,1])}')
	plt.show()
	return 0 

#print(t2(data['time'], data['amp'], error)) 



#_________________________________________________________________________

#Measurement of T2' of Paraffin Oil

with open('/home/minato132/Documents/Data/para/parat2p_ne.csv') as file:
	data = pd.read_csv(file)
	data['CH1'] = pd.to_numeric(data.loc[1:,'CH1'])
	
	time = []
	x = data.loc[0, 'Start']
	i = 0
	while i < len(data['X'])-1:
		x += data.loc[0, 'Increment'] 
		time.append(x)
		i += 1 
	time = pd.Series(time,index = np.arange(1, 1201))

	error = []
	for i in data['CH1']:
		i *= .01
		error.append(i)

	d = {'time': time, 'amp': data['CH1'], 'err' : error}
	

data = pd.DataFrame(d)
data = data.loc[data['amp'] > .2]


#pd.set_option('display.max_rows', None)

data1 = data.loc[data['amp'] > .65]
data1 = data1.loc[data1['amp'] > -5/.1 * data1['time'] + 5]
data1.drop([594, 173, 630, 905], axis = 0, inplace = True)



def t2p(ar1, ar2, ar3):
	a, b = param_get(ar1, ar2, T2p, ar3)

	plt.errorbar(ar1, ar2, yerr = .38/3, fmt = ',', color = 'green', label = 'Error')
	plt.scatter(ar1, ar2, color = 'purple', marker = 'x', label = 'Data')
	plt.plot(ar1, T2p(ar1, *a), color = 'red', label = 'Fitted Data')
	plt.xlabel('Time (ms)')
	plt.ylabel('Maximum Amplitude of Each Echo')
	plt.title("T2' of Paraffin Oil")
	plt.legend()

	print(*a, f'\n Error of b is {np.sqrt(b[1,1])}')
	plt.show()
	return 0

data = data.loc[data['time'] > 0]
data['time'] = data['time'] * 1000 
data1['time'] = data1['time'] * 1000 

print(t2p(data1['time'], data1['amp'], data1['err']))


