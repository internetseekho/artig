from ast import Constant
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
import tkinter.ttk as ttk
import os
import subprocess
import threading
import time

FRAMERATE=15

open("tmp.txt","w").write("0,0,Ready_To_Run")

def darkstyle(root):
    ''' Return a dark style to the window'''
    
    style = ttk.Style(root)
    root.tk.call('source', 'breeze-dark/breeze-dark.tcl')
    style.theme_use('breeze-dark')
    style.configure("TButton", foreground='white')
    return style


def RunScript():
    csv=askopenfilename(initialdir= os.getcwd(),title="Select a CSV file")
    open("tmp.txt","w").write("0,0,Driver_Start")
    a=threading.Thread(target=lambda:exec("subprocess.run(['python', os.getcwd()+os.sep+'ArtiForgeScript.py','"+csv+"'])"))
    a.start()
root=Tk()
style=darkstyle(root)
root.title("ArtiForge")
root.geometry("300x150")
#root.iconbitmap("App.ico")
#Start Button
work=Label(root,text="Ready!")
totp=Label(root,text="Total Progress")
runbtn=Button(root,text="START",command=RunScript,style="TButton")
progress = Progressbar(root, orient = HORIZONTAL,length = 300, mode = 'determinate')
singleprogress = Progressbar(root, orient = HORIZONTAL,length = 200, mode = 'determinate')
#Packing
work.pack()

singleprogress.pack()

runbtn.pack()



progress.pack(side=BOTTOM)

totp.pack(side=BOTTOM)



while True:
    time.sleep(1/FRAMERATE)
    try:
        a=open("tmp.txt","r").read().split(",")
        progress['value'] = int(a[0])
        singleprogress['value']= int(round(float(a[1])))
        if a[2]=="Completed_Task_Successfully":
            work.config(text = "Completed All Tasks!")
        elif a[2]=="Process_Starting":
            work.config(text = "Starting Process...")
        elif a[2]=="New_Query_Search":
            work.config(text = "Searching New Query...")
        elif a[2]=="Driver_Start":
            work.config(text = "Starting Driver...")
        elif a[2]=="Ready_To_Run":
            work.config(text = "Ready To Run!")
            
        else:
            work.config(text = "Working on: "+a[2])
        
    except:
        pass
    root.update_idletasks()
    root.update()