"""
Simple spectrum plotting GUI made by Ian
https://github.com/ianliu98/ERG-spectrum-generator/blob/main/ERG_spectrum_generator_ver2.py
"""
import os,sys,math
import numpy as np
import matplotlib.pyplot as plt
import spacepy.pycdf as cdf
import datetime

#------------------------------------------------
PARAMETER = 1022    # for each time break, the lasting period of waveform data
MGNT = np.zeros(0)  # MGF wave magnitude
MGF_EPOCH = np.zeros(0)  # MGF epoch
Q = 1.60217662e-19  # charge of electron
M = 9.10938356e-31  # mass of electron
# -----------------------------------------------

# data split
def split(epoch_data):
    epoch_stamp = [epoch_data[i].timestamp() for i in range(epoch_data.shape[0])]   # convert epoch to timestamp
    epoch_interval = np.where(np.diff(epoch_stamp) > 10)    # find interval of time
    position = np.insert(epoch_interval[0], 0, -1)   # insert initial time
    position = np.insert(position, position.shape[0], epoch_data.shape[0])    # insert end time
    number_segment = np.arange(1,position.shape[0])
    return position, number_segment

#calculation of fce
def fce(start,end):
    fce = Q / (M * 2 * np.pi) * mgf_mgnt * 1e-9
    fce_half = fce / 2

# Select WFC file
filename = './wfc/2018/03/erg_pwe_wfc_l2_b_65khz_2018032306_v00_01.cdf'
file_data = cdf.CDF(filename)
#read epoch data and data split
epoch_data = file_data['epoch'][:]
tsize = epoch_data.shape[0]
POSITION , number_segment = split(epoch_data)
#read field data and change 2D array to 1D
Bx_tmp = file_data['Bx_waveform'][:,:]
By_tmp = file_data['By_waveform'][:,:]
Bz_tmp = file_data['Bz_waveform'][:,:]
Bx_raw = np.ravel(Bx_tmp)
By_raw = np.ravel(By_tmp)
Bz_raw = np.ravel(Bz_tmp)

# Select MGF file
mgf_name = './mgf/2018/03/erg_mgf_l2_8sec_20180323_v03.04.cdf'
mgf_data = cdf.CDF(mgf_name)
print(mgf_data)
mgf_epoch = mgf_data['epoch_8sec'][:]
mgf_B_field = mgf_data['magt_8sec'][:]
mgf_B_field = np.where((mgf_B_field>-1e10)&(mgf_B_field<1e10),mgf_B_field,np.nan)

split_tmp = number_segment[0]
time_segment_start = POSITION[split_tmp - 1] + 1  # start point of epoch segment
time_segment_end = POSITION[split_tmp]  # end point of epoch segment
loc1, loc2 = 0, 0  # find position in MGF epoch <- for reading mgf magnitude data
for loc1 in range(mgf_epoch.shape[0]):
    if epoch_data[time_segment_start] <= mgf_epoch[loc1]: break
for loc2 in range(mgf_epoch.shape[0]):
    if epoch_data[time_segment_end-1] <= mgf_epoch[loc2]: break
mgf_time = mgf_epoch[loc1-1:loc2+1]  # mgf time segment
mgf_mgnt = mgf_B_field[loc1-1:loc2+1]  # mgf magnitude segment
# make sure mgf file is not missed
if mgf_mgnt.shape[0] < 1:
    msg.showwarning('Warning', 'Please select MGF data!')
    sys.exit()
fce = Q / (M * 2 * np.pi) * mgf_mgnt * 1e-9
fce_half = fce / 2


#spectrogram settings
split_tmp = number_segment[0]
start = (POSITION[split_tmp - 1] + 1) * 8192 + PARAMETER  # calculate start point of one segment
end = (POSITION[split_tmp]) * 8192  # end point of one segment
nfft = 8192
Fs = 65536
noverlap = 4096
#make spectrogram
B = (Bx_raw+By_raw+Bz_raw)/3
spec_data, spec_freq, spec_time, spec_img = plt.specgram(B[start:end], NFFT=nfft, Fs=Fs, noverlap=noverlap, scale='dB',cmap='jet')

#fce plotting
ratio = spec_time[-1] / (mgf_mgnt.shape[0] - 1)  # for drawing fce line in specgram method
mgf_time_tick = np.arange(0.1, spec_time[-1], ratio)
mgf_time_tick = np.insert(mgf_time_tick, mgf_time_tick.shape[0], spec_time[-1])
#plt.plot(mgf_time_tick, fce, color="r", linestyle="--", label="electron cyclotron freq.")
plt.plot(mgf_time_tick, fce_half, color="r", linestyle="--", label="half electron cyclotron freq.")

#time axis settings
time_s = math.floor(start/8192)
time_s_epoch = epoch_data[time_s]
time_array = np.zeros((spec_time.shape[0]),dtype=object)
print(datetime.timedelta(seconds=PARAMETER/65536))
for index,spec_time_tmp in enumerate(spec_time):
    time_trans = time_s_epoch+datetime.timedelta(seconds=PARAMETER/65536)+datetime.timedelta(seconds=spec_time_tmp) #offseted by PARAMETER
    time_array[index] = time_trans.strftime('%H:%M:%S')+'\n' + time_trans.strftime('%f')+'\n'+time_trans.strftime('%Y.%m.%d')    # create time ticks
#appearances
cbar = plt.colorbar()
cbar.set_label('dB', rotation=270)
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time (UTC)')
time_tick = []
plt.xticks(spec_time,time_array)
plt.locator_params(axis='x', nbins=10)    # arrange time ticks
ax_x, ax_y = plt.gca().get_position().x0, plt.gca().get_position().y0 
plt.figtext(ax_x - 0.05, ax_y - 0.05, 'Time:\nms:\nDate:')  # label
plt.ylim(0,np.max(fce))
plt.clim(-50,20)
plt.show()

# use pycdf to read cdf file

