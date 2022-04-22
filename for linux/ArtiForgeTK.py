from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
import os
import subprocess
import threading
open("tmp.txt","w").write("0,0,Nothing")

def RunScript():
    csv=askopenfilename(initialdir= os.getcwd(),title="Select a CSV file")
    open("tmp.txt","w").write("0,0,Starting Driver...")
    a=threading.Thread(target=lambda:exec("subprocess.run(['python3', '"+os.getcwd()+os.sep+"ArtiForgeScript.py','"+csv+"'])"))
    a.start()
root=Tk()
root.title("ArtiForge")
root.geometry("300x300")
#Start Button
work=Label(root,text="Working on: Nothing")
totp=Label(root,text="Total Progress")
runbtn=Button(root,text="START",command=RunScript)
progress = Progressbar(root, orient = HORIZONTAL,length = 300, mode = 'determinate')
singleprogress = Progressbar(root, orient = HORIZONTAL,length = 200, mode = 'determinate')
#Packing
work.pack()

singleprogress.pack()

runbtn.pack()



progress.pack(side=BOTTOM)

totp.pack(side=BOTTOM)



while True:
    try:
        a=open("tmp.txt","r").read().split(",")
        progress['value'] = int(a[0])
        singleprogress['value']= int(round(float(a[1])))
        work.config(text = "Working on: "+a[2])
        
    except:
        pass
    root.update_idletasks()
    root.update()