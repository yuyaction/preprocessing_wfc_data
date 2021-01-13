import os, sys, shutil, glob
import tkinter as tk
from tkinter import font

# set year and month ----------------------------
year = 2017
month = 4
# -----------------------------------------------

fig_num = 0 #initialization

def labeling(name,file_path_local): #labeling files
    global fig_num
    global file_path
    new_name = file_path_local[:-4]+'_'+name+'.png'
    os.rename(file_path_local,new_name)
    fig_num += 1
    print(fig_num)
    if fig_num > last_num-1:
        root.quit()
    file_path = fig_name_list[fig_num]
    plot_figrues(file_path)

def move_dict(dict,file_path_local): #move a file from current directory to another directory
    global fig_num
    global file_path
    shutil.move(file_path_local,dict)
    fig_num += 1
    print(fig_num)
    if fig_num > last_num:
        root.quit()
    file_path = fig_name_list[fig_num]
    plot_figrues(file_path)

def plot_figrues(file_path): #display figures on TKinter
    global chorus_fig
    chorus_fig = tk.PhotoImage(file=file_path)
    canvas = tk.Canvas(bg="black", width=1600, height=900)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, image=chorus_fig, anchor=tk.NW)
    label = tk.Label(root, text=file_path, font=font1)
    label.place(x=0, y=900)

save_dict = './figure/'+str(year)+'/'+str(month).zfill(2)+'/'
error_dict = save_dict+'error/'
unknown_dict = save_dict+'unknown/'
os.makedirs(error_dict,exist_ok=True) #make directories to save
os.makedirs(unknown_dict,exist_ok=True) #make directories to save
fig_name_list = glob.glob(save_dict+'*[0-9].png')
fig_name_list = sorted(fig_name_list)
last_num = len(fig_name_list)
print("The number of remaining figures: ",last_num)


root = tk.Tk()
root.title('Labeling chorus types')
#root.minsize(1800,900)
root.geometry("1800x900")
#font settings
font1 = font.Font(family='Helvetica', size=20, weight='bold')
font2 = font.Font(family='Helvetica', size=14, weight='bold')
#plot figures
file_path = fig_name_list[fig_num]
plot_figrues(file_path)

#buttons
#if you want to add or change buttons, please change below.
#labeling 
#e.g. button_name = tk.Button(text=u'Display_name',font=font2, anchor=tk.W, width=50, height = 8, command=lambda: labeling('labeling_name',file_path))
#move file to another directory
#e.g. button_name = tk.Button(text=u'Display_name',font=font2, anchor=tk.W, width=50, height = 8, command=lambda: move_dict(another_directory_path,file_path))

Button0 = tk.Button(text=u'None',font=font2, anchor=tk.W, width=20, height = 8, command=lambda: labeling('None',file_path))
Button0.place(x=1600, y=0)
Button1 = tk.Button(text=u'Structure',font=font2 , anchor=tk.W, width=20, height = 8, command=lambda: labeling('Structure',file_path))
Button1.place(x=1600, y=120)
Button2 = tk.Button(text=u'Rising',font=font2 , anchor=tk.W, width=20, height = 8, command=lambda: labeling('Rising',file_path))
Button2.place(x=1600, y=240)
Button3 = tk.Button(text=u'Falling',font=font2 , anchor=tk.W, width=20, height = 8, command=lambda: labeling('Falling',file_path))
Button3.place(x=1600, y=360)
Button4 = tk.Button(text=u'Hiss',font=font2 , anchor=tk.W, width=20, height = 8, command=lambda: labeling('Hiss',file_path))
Button4.place(x=1600, y=480)
Button5 = tk.Button(text=u'Artificial Signal',font=font2 , anchor=tk.W, width=20, height = 8, command=lambda: labeling('AS',file_path))
Button5.place(x=1600, y=600)
Button6 = tk.Button(text=u'Unknown',font=font2 , anchor=tk.W, width=20, height = 8, command=lambda: move_dict(unknown_dict,file_path))
Button6.place(x=1600, y=720)
Button7 = tk.Button(text=u'Error',font=font2 , anchor=tk.W, width=20, height = 8, command=lambda: move_dict(error_dict,file_path))
Button7.place(x=1600, y=840)

#keyboard Input
root.bind('<Key-n>', lambda x: labeling('None',file_path))
root.bind('<Key-s>', lambda x: labeling('Structure',file_path))
root.bind('<Key-r>', lambda x: labeling('Rising',file_path))
root.bind('<Key-f>', lambda x: labeling('Falling',file_path))
root.bind('<Key-h>', lambda x: labeling('Hiss',file_path))
root.bind('<Key-a>', lambda x: labeling('AS',file_path))
root.bind('<Key-u>', lambda x: move_dict(unknown_dict,file_path))
root.bind('<Key-e>', lambda x: move_dict(error_dict,file_path))

root.mainloop()
