"""
Simple spectrum plotting GUI made by Ian
https://github.com/ianliu98/ERG-spectrum-generator/blob/main/ERG_spectrum_generator_ver2.py
"""
import os,sys,math,glob
import numpy as np
import matplotlib.pyplot as plt
os.environ["CDF_LIB"] = '/home/yuya/local/src/cdf38_0-dist/lib/'
import spacepy.pycdf as cdf
import datetime

#------------------------------------------------
PARAMETER = 1022    # for each time break, the lasting period of waveform data
DATA_NUMBER = 8192    # for each time break, the lasting period of waveform data
MGNT = np.zeros(0)  # MGF wave magnitude
MGF_EPOCH = np.zeros(0)  # MGF epoch
Q = 1.60217662e-19  # charge of electron
M = 9.10938356e-31  # mass of electron
TIME_SCALE = 8 #time scaling for plot(n seconds) 

nfft = 8192
Fs = 65536
noverlap = 4096

year = 2017
month = 4

upper_band = True
lower_band = True
is_half_fce = False
is_axis = False
# -----------------------------------------------

# data split
def split(wfc_epoch):
    epoch_stamp = [wfc_epoch[i].timestamp() for i in range(wfc_epoch.shape[0])]   # convert epoch to timestamp
    epoch_interval = np.where(np.diff(epoch_stamp) > 10)    # find interval of time
    position = np.insert(epoch_interval[0], 0, -1)   # insert initial time
    position = np.insert(position, position.shape[0], wfc_epoch.shape[0])    # insert end time
    number_segment = np.arange(1,position.shape[0])
    return position, number_segment

def time_setting(start,end):
    flag = 0
    ### time axis settings
    time_segment_start = int((start - PARAMETER)/DATA_NUMBER)  # start point of epoch segment
    time_segment_end =  int((end - PARAMETER)/DATA_NUMBER) # end point of epoch segment
    #time_segment_start = POSITION[split_tmp - 1] + 1  # start point of epoch segment
    #time_segment_end = POSITION[split_tmp]  # end point of epoch segment
    loc1, loc2 = 0, 0  # find position in MGF epoch <- for reading mgf magnitude data
    for loc1 in range(mgf_epoch.shape[0]):
        if wfc_epoch[time_segment_start] <= mgf_epoch[loc1]: break
    for loc2 in range(mgf_epoch.shape[0]):
        if wfc_epoch[time_segment_end-1] <= mgf_epoch[loc2]: break
    mgf_time = mgf_epoch[loc1-1:loc2+1]  # mgf time segment
    mgf_mgnt = mgf_B_field[loc1-1:loc2+1]  # mgf magnitude segment
    # make sure mgf file is not missed
    if mgf_mgnt.shape[0] < 1:
        print('No mgf data of this time!')
        flag = 1
    fce = Q / (M * 2 * np.pi) * mgf_mgnt * 1e-9
    #make time label
    time_s = math.floor(start/DATA_NUMBER)
    time_s_epoch = wfc_epoch[time_s]
    time_array = np.zeros((spec_time.shape[0]),dtype=object)
    for index,spec_time_tmp in enumerate(spec_time):
        time_trans = time_s_epoch-datetime.timedelta(seconds=(nfft-noverlap)/Fs)+datetime.timedelta(seconds=PARAMETER/65536)+datetime.timedelta(seconds=spec_time_tmp) #offseted by PARAMETER
        time_array[index] = time_trans.strftime('%H:%M:%S')+'\n' + time_trans.strftime('%f')+'\n'+time_trans.strftime('%Y.%m.%d')    # create time ticks
    return time_array, fce, flag

def initFigure():
    plt.rcParams["figure.figsize"] = (16, 9)

def get_fig_name(start,end,save_path,name,packet):
    s_num = str(start).zfill(8)
    e_num = str(end).zfill(8)
    return save_path+name+'_'+s_num+'_'+e_num+'_'+packet+'.png'

def saveFigure(fig_name):
    plt.savefig(fig_name)
    plt.clf()

def saveFigure_without_axis(fig_name):
    plt.savefig(fig_name,bbox_inches="tight", pad_inches=0.0)
    plt.clf()

def plot_setting(spec_time,time_array,fce):
    cbar = plt.colorbar()
    cbar.set_label('dB', rotation=270)
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (UTC)')
    plt.xticks(spec_time,time_array)
    plt.locator_params(axis='x', nbins=10)    # arrange time ticks
    ax_x, ax_y = plt.gca().get_position().x0, plt.gca().get_position().y0 
    plt.figtext(ax_x - 0.05, ax_y - 0.05, 'Time:\nms:\nDate:')  # label
    plt.clim(-50,20)

def fce_plot(spec_time,fce):
    ratio = spec_time[-1] / (fce.shape[0] - 1)  # for drawing fce line in specgram method
    mgf_time_tick = np.arange(0.1, spec_time[-1], ratio)
    mgf_time_tick = np.insert(mgf_time_tick, mgf_time_tick.shape[0], spec_time[-1])
    plt.plot(mgf_time_tick, fce/2, color="r", linestyle="--", label="half electron cyclotron freq.")

def get_name(file_name):
    #get save_path and save_name
    tmp_name = os.path.splitext(os.path.basename(file_name)) #get file name
    date = tmp_name[0][-17:-9]
    save_name = tmp_name[0][-17:-7]
    print(save_name)
    return date, save_name


#
save_dict = './figure/'+str(year)+'/'+str(month).zfill(2)+'/'
new_save_dict = './modified_figure/'+str(year)+'/'+str(month).zfill(2)+'/'
wfc_dict = './wfc/'+str(year)+'/'+str(month).zfill(2)+'/'
mgf_dict = './mgf/'+str(year)+'/'+str(month).zfill(2)+'/'
wfc_list = glob.glob(wfc_dict+'*b*')
mgf_list = glob.glob(mgf_dict+'*v03.04*')
os.makedirs(new_save_dict,exist_ok=True) #make directories to save

None_list = glob.glob(save_dict+'*None.png')
None_list = sorted(None_list)
None_num = len(None_list)
Structure_list = glob.glob(save_dict+'*Structure.png')
Structure_list = sorted(Structure_list)
Structure_num = len(Structure_list)
Rising_list = glob.glob(save_dict+'*Rising.png')
Rising_list = sorted(Rising_list)
Rising_num = len(Rising_list)
Falling_list = glob.glob(save_dict+'*Falling.png')
Falling_list = sorted(Falling_list)
Falling_num = len(Falling_list)
Hiss_list = glob.glob(save_dict+'*Hiss.png')
Hiss_list = sorted(Hiss_list)
Hiss_num = len(Hiss_list)
AS_list = glob.glob(save_dict+'*AS.png')
AS_list = sorted(AS_list)
AS_num = len(AS_list)
None_num = len(None_list)

total_num = None_num+Structure_num+Rising_num+Falling_num+Hiss_num+AS_num
if total_num>0:
    print("None     : ",None_num," ",round(None_num/total_num,3)*100,"%")
    print("Structure: ",Structure_num," ",round(Structure_num/total_num,3)*100,"%")
    print("Rising   : ",Rising_num," ",round(Rising_num/total_num,3)*100,"%")
    print("Falling  : ",Falling_num," ",round(Falling_num/total_num,3)*100,"%")
    print("Hiss     : ",Hiss_num," ",round(Hiss_num/total_num,3)*100,"%")
    print("AS       : ",AS_num," ",round(AS_num/total_num,3)*100,"%")
    print("Total    : ",total_num)
else:
    print('No Figures.')
    sys.exit()

# Select WFC file
old_fig_list = glob.glob(save_dict+'*.png')
old_fig_list = glob.glob(save_dict+'*Rising.png')
j=0
k=0
for old_fig_name in old_fig_list:
    wfc_date_time = old_fig_name[17:27]
    wfc_name = glob.glob(wfc_dict+'*b_65khz*'+wfc_date_time+'*.cdf')[0]
    wfc_data = cdf.CDF(wfc_name)
#read epoch data and data split
    wfc_epoch = wfc_data['epoch'][:]
    tsize = wfc_epoch.shape[0]
    POSITION , number_segment = split(wfc_epoch)
#read field data and change 2D array to 1D
    Bx_tmp = wfc_data['Bx_waveform'][:,:]
    By_tmp = wfc_data['By_waveform'][:,:]
    Bz_tmp = wfc_data['Bz_waveform'][:,:]
    Bx_raw = np.ravel(Bx_tmp)
    By_raw = np.ravel(By_tmp)
    Bz_raw = np.ravel(Bz_tmp)
    B = (Bx_raw+By_raw+Bz_raw)/3

#get save_path and save_name
    date, save_name= get_name(wfc_name)
# Select MGF file
    for mgf_name_tmp in mgf_list:
        if (date in mgf_name_tmp):
            mgf_name = mgf_name_tmp
            break
        continue

    mgf_data = cdf.CDF(mgf_name)
    mgf_epoch = mgf_data['epoch_8sec'][:]
    mgf_B_field = mgf_data['magt_8sec'][:]
    mgf_B_field = np.where((mgf_B_field>-1e10)&(mgf_B_field<1e10),mgf_B_field,np.nan)

    new_start = int(old_fig_name[36:44])
    new_end = int(old_fig_name[45:53])
    if 'None' in old_fig_name:
        packet = 'None'
    elif 'Rising' in old_fig_name:
        packet = 'Rising'
    elif 'Falling' in old_fig_name:
        packet = 'Falling'
    elif 'Structure' in old_fig_name:
        packet = 'Structure'
    elif 'Hiss' in old_fig_name:
        packet = 'Hiss'
    else:
        packet = 'AS'
    fig_name = get_fig_name(new_start, new_end, new_save_dict, save_name, packet)
    if os.path.exists(fig_name) == True: 
        continue
    initFigure()
    spec_data, spec_freq, spec_time, spec_img = plt.specgram(B[new_start:new_end], NFFT=nfft, Fs=Fs, noverlap=noverlap, scale='dB',cmap='jet')
    time_array, fce, flag = time_setting(new_start,new_end)
    if flag == 1:
        continue
    if is_axis == True:
        plot_setting(spec_time,time_array,fce)
    else:
        plt.axis('off')
        plt.clim(-50,20)

    if lower_band == True:
        if upper_band == True:
            plt.ylim(0,np.max(fce))
            if is_half_fce == True:
                fce_plot(spec_time,fce)
        else:
            plt.ylim(0,np.max(fce/2))
    else:
            plt.ylim(np.min(fce/2),np.max(fce))


    if is_axis == True:
        saveFigure(fig_name)
    else:
        saveFigure_without_axis(fig_name)

    print(fig_name)
