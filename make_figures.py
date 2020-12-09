import os,sys,math
import numpy as np
import matplotlib.pyplot as plt
import spacepy.pycdf as cdf
import datetime
import pandas as pd

# Select WFC file
filename = './cdf/2018/03/erg_pwe_wfc_l2_b_65khz_2018032306_v00_01.cdf'
file_data = cdf.CDF(filename)
#print(file_data)
epoch_data = file_data['epoch'][:]

wave_tmp = file_data['Bx_waveform'][:,:]
#delete outlier and interpolation 
wave_tmp = np.where((wave_tmp > -1e2) & (wave_tmp < 1e2),wave_tmp,np.nan)
wave = np.ravel(wave_tmp)
wave_pandas = pd.Series(wave)
wave = wave_pandas.interpolate()
#spectrogram settings
start = 0
end = 8192*100
nfft = 8192
Fs = 65536
noverlap = 4096
#make spectrogram
spec_data, spec_freq, spec_time, spec_img = plt.specgram(wave[start:end], NFFT=nfft, Fs=Fs, noverlap=noverlap, scale='dB',cmap='jet')

#time axis settings
time_s = math.floor(start/8192)
time_s_epoch = epoch_data[time_s]
time_array = np.zeros((spec_time.shape[0]),dtype=object)
for index,spec_time_tmp in enumerate(spec_time):
    time_trans = time_s_epoch+datetime.timedelta(seconds=spec_time_tmp)
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
plt.ylim(0,2000)
plt.clim(-10,10)
plt.show()

# use pycdf to read cdf file

