import os, sys, shutil, glob
import tkinter as tk

# -----------------------------------------------
year = 2017
month = 4
fig_num = 0
# -----------------------------------------------

def labeling(name,file_path_local):
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

def move_dict(dict,file_path_local):
    global fig_num
    global file_path
    shutil.move(file_path_local,dict)
    fig_num += 1
    print(fig_num)
    if fig_num > last_num:
        root.quit()
    file_path = fig_name_list[fig_num]
    plot_figrues(file_path)

def plot_figrues(file_path):
    global chorus_fig
    chorus_fig = tk.PhotoImage(file=file_path)
    canvas = tk.Canvas(bg="black", width=1600, height=900)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, image=chorus_fig, anchor=tk.NW)

save_dict = './figure/'+str(year)+'/'+str(month).zfill(2)+'/'
error_dict = save_dict+'error/'
unknown_dict = save_dict+'unknown/'
os.makedirs(error_dict,exist_ok=True) #make directories to save
os.makedirs(unknown_dict,exist_ok=True) #make directories to save
fig_name_list = glob.glob(save_dict+'*[0-9].png')
last_num = len(fig_name_list)

root = tk.Tk()
root.title('Labeling chorus types')
#root.minsize(1800,900)
root.geometry("1800x900")
#plot figures
file_path = fig_name_list[fig_num]
plot_figrues(file_path)

#buttons
Button0 = tk.Button(text=u'None', anchor=tk.W, width=50, height = 10, command=lambda: labeling('None',file_path))
Button0.place(x=1600, y=0)
Button1 = tk.Button(text=u'Rising', anchor=tk.W, width=50, height = 10, command=lambda: labeling('Rising',file_path))
Button1.place(x=1600, y=150)
Button2 = tk.Button(text=u'Falling', anchor=tk.W, width=50, height = 10, command=lambda: labeling('Falling',file_path))
Button2.place(x=1600, y=300)
Button3 = tk.Button(text=u'Hiss', anchor=tk.W, width=50, height = 10, command=lambda: labeling('Hiss',file_path))
Button3.place(x=1600, y=450)
Button4 = tk.Button(text=u'Unknown', anchor=tk.W, width=50, height = 10, command=lambda: move_dict(unknown_dict,file_path))
Button4.place(x=1600, y=600)
Button5 = tk.Button(text=u'Error', anchor=tk.W, width=50, height = 10, command=lambda: move_dict(error_dict,file_path))
Button5.place(x=1600, y=750)

root.bind('<Key-n>', lambda x: labeling('None',file_path))
root.bind('<Key-r>', lambda x: labeling('Rising',file_path))
root.bind('<Key-f>', lambda x: labeling('Falling',file_path))
root.bind('<Key-h>', lambda x: labeling('Hiss',file_path))
root.bind('<Key-u>', lambda x: move_dict(unknown_dict,file_path))
root.bind('<Key-e>', lambda x: move_dict(error_dict,file_path))

root.mainloop()
