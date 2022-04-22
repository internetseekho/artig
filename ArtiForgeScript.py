from AF_API import *
import sys
import os.path
import os

if not os.path.exists("LineBreaks"):
    os.mkdir("LineBreaks")

fname="LineBreaks/"+sys.argv[1].split("/")[-1].split(".")[0]

open("tmp.txt","w").write("0,0,Process_Starting")
if not os.path.isfile(f"{fname}.txt"):
    open(f"{fname}.txt","w").write("0")



f=open("LoginInfo.txt","r")
fields=f.read().split(";")[0].replace("\n","").split(",")
email=fields[0]

password=fields[1]

login(email,password)
lines=int(open(f"{fname}.txt","r").read())
f=open(sys.argv[1],"r")
num_lines = sum(1 for line in open(sys.argv[1]))-1
count=0
i=0
while count<lines:
    f.readline()
    print(count)
    count+=1

while True:
    count += 1
    open(f"{fname}.txt","w").write(str(count))
    # Get next line from file
    line = f.readline()
    # if line is empty
    # end of file is reached
    if not line:
        break
    
    if count==1:
        pass
    else:
        print(line)
        line=line.replace('"',"").replace("\n","").split(",")
        kw=line[:-6]
        title=True if line[-4] == "Yes" else False
        headings=True if line[-3] == "Yes" else False
        autogen=True if line[-2] == "Yes" else False
        words=str(line[-5].split(" ")[0])
        print(kw,words)
        kw.append(words)
        kw.append(title)
        item=kw
        print(item)
        a=open("tmp.txt","r").read().split(",")
        open("tmp.txt","w").write(str(int((i/num_lines)*100))+","+a[1]+","+a[2])
        createnewarticle()
        additem(item)
        l=1
        print(item[-2])
        if item[-2]=="50":
            l=1
        elif item[-2]=="250":
            l=2
        elif item[-2]=="500":
            l=3
        elif item[-2]=="750":
            l=4
        elif item[-2]=="1500":
            l=5
        defineoptions(lenght=int(l),titles=item[-1],headings=headings,autogen=autogen,language=line[-1])
        waitforcompletion(item[:-2],lenght=int(l))
        a=open("tmp.txt","r").read().split(",")
        open("tmp.txt","w").write(a[0]+",0,New_Query_Search")
        i+=1



os.remove(f"{fname}.txt")
open("tmp.txt","w").write("100,100,Completed_Task_Successfully")
driver.close()