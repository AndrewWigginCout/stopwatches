# import tkinter
#to install tkinter in linux do:
# sudo apt-get install python3-tk
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
try:
    from tkinter import *
except ImportError:
    print("import error")
try:
    from tkinter import filedialog
except ImportError:
    print("import error2")

import os
from datetime import datetime, timedelta

#stopwatch description
# it's a tuple where the second item is a list of pair tuples

#delta,start end
#      start end
#      start end










#import datetime
#from datetime import datetime
#from datetime import timedelta
#import time
tic_time=200
time_delta_zero=timedelta()

stopwatches=[]
gui_stopwatch_elements=[]
fn='blank'
appfont=("Consolas","15")
ledfont=("Consolas","30")
def buzz():
    for j in range(3):
        for i in range(3):
            Beep(480,300)
        #time.sleep(.400)
def time_format(n):
    s=int(n%60)
    m=int(n//60)
    h=int(m//60)
    m=m%60
    return '{:02d}:{:02d}:{:02d}'.format(h,m,s)
def time_format_time_delta(n):
    return datetime.utcfromtimestamp(n.seconds).strftime("%H:%M:%S")
def sum_stopwatch(n):
    sum=time_delta_zero
    for e in n['stamps']:
        sum+=e[1]-e[0]
    return sum
def write_file(data,fn,flags):
    fh=open(fn,flags)
    fh.write(data)
    fh.close()
def read_file(fn,flags):
    fh=open(fn,flags)
    rv=fh.read()
    fh.close()
    return rv
def str_stopwatches():
    rv=''
    for sw in stopwatches:
        rv+='name:'+sw['name']+'\n'
        rv+='elapsed:'+str(sw['elapsed'])+'\n'
        for stamp in sw['stamps']:
            rv+='\t'+str(stamp[0])+'\t'+str(stamp[1])+'\n'
    return rv
def save_timestamps():
    for i,gui_stopwatch in enumerate(gui_stopwatch_elements):
        stopwatches[i]['name']=gui_stopwatch[0].get()
    fn=str(datetime.now())
    fn=fn.replace(":",".")
    fn=fn[0:19]
    write_file(str_stopwatches(),fn+".ts.txt","wt")
def load_file(fn):
    s=read_file(fn,"rt")
    load_stopwatches(s)
def load_stopwatches(s):
    stopwatches.clear()
    for line in s.splitlines():
        if line[0:5]=="name:":
            stopwatches.append({"name":line[5:]})
            stopwatches[-1]["stamps"]=[]
        elif line[0:8]=="elapsed:":
            #stopwatches[-1]["elapsed"]=line[8:]
            stopwatches[-1]["elapsed"]=time_delta_zero
        else:
            v=line.split('\t')
            t1=datetime.strptime(v[1],'%Y-%m-%d %H:%M:%S.%f')
            t2=datetime.strptime(v[2],'%Y-%m-%d %H:%M:%S.%f')            
            stopwatches[-1]["stamps"].append([t1,t2])
    for stopwatch in stopwatches:
        for stamp in stopwatch['stamps']:
            stopwatch["elapsed"]+=stamp[1]-stamp[0]
def on_closing():
    for i,gui_stopwatch in enumerate(gui_stopwatch_elements):
        stopwatches[i]['name']=gui_stopwatch[0].get()
    save_timestamps()
    root.destroy()
def donothing():
    pass

class Timer:
    def __init__(self, parent):
        self.sroot=parent
        self.active=False
        self.button_create = tk.Button(parent,
                                       font=appfont,
                                       text="CREATE NEW STOPWATCH",
                                       command=self.create_new_stopwatch_gui)
        self.button_create.grid(column=0,row=0,columnspan=2)
        menubar = tk.Menu(parent)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load", command=self.ui_load_file)
        filemenu.add_command(label="Save", command=save_timestamps)
        filemenu.add_command(label="Debug", command=self.debug)
        filemenu.add_command(label="Destroy",command=self.destroy)
        filemenu.add_command(label="Exit",command=self.sroot.destroy)
        menubar.add_cascade(label="File",menu=filemenu)
        parent.config(menu=menubar)

    def create_new_stopwatch_gui(self):
        stopwatches.append({'name':'','elapsed':time_delta_zero,'stamps':[]})
        self.create_new_stopwatch()
    def create_new_stopwatch(self):
        gui_stopwatch_elements.append([])
        i=len(gui_stopwatch_elements)-1
        gui_stopwatch_elements[-1].append(tk.Entry(root,font=appfont))
        gui_stopwatch_elements[-1][-1].grid(column=0,row=i+1)

        gui_stopwatch_elements[-1].append(tk.Button(root,font=appfont,text="START",command=lambda: self.start_stopwatch(i)))
        gui_stopwatch_elements[-1][-1].grid(column=1,row=i+1)

        gui_stopwatch_elements[-1].append(tk.Button(root,font=appfont,text="STOP",command=lambda: self.stop_stopwatch(i)))
        gui_stopwatch_elements[-1][-1].grid(column=2,row=i+1)

        gui_stopwatch_elements[-1].append(tk.Label(root,font=ledfont,text="0:00:00"))
        gui_stopwatch_elements[-1][-1].grid(column=3,row=i+1)

    def destroy(self):
        #for i in range (len(gui_stopwatch_elements)):
        #    del(gui_stopwatch_elements[i])
        if gui_stopwatch_elements==[]: return
        for each in gui_stopwatch_elements[0]:
            each.destroy()
        gui_stopwatch_elements.pop(0)
        
    def ui_load_file(self):
        self.sroot.filename=tk.filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
        fn=self.sroot.filename
        if fn!='': load_file(fn)
        while gui_stopwatch_elements!=[]:
            self.destroy()
        for stopwatch in stopwatches:
            self.create_new_stopwatch()
            print("sw")
            gui_stopwatch_elements[-1][0].insert(0,stopwatch["name"])
        self.render_all()
        
    def start_stopwatch(self,i):
        was_active=self.active
        self.active=True
        now = datetime.now()
        print('start',i,end=' ')
#        self.debug()
        print(gui_stopwatch_elements[i][0].get(),end=' ')
        print(str(now))
        # if stopwatch is brand new with zero
        if stopwatches[i]['stamps']==[]:
            stopwatches[i]['stamps'].append([now,None])
            if not was_active: self.tick()
        else:
            # if end stamp exists, ie if not already open
            if stopwatches[i]['stamps'][-1][1] is not None:
                stopwatches[i]['stamps'].append([now,None])
                if not was_active: self.tick()
        #self.debug()

    def stop_stopwatch(self,i):
        now = datetime.now()
        print('stop',i,str(now))
        if stopwatches[i]['stamps']!=[] and stopwatches[i]['stamps'][-1][1] is None:
            stopwatches[i]['stamps'][-1][1]=now
            stopwatches[i]['elapsed']+=stopwatches[i]['stamps'][-1][1]-stopwatches[i]['stamps'][-1][0]
        self.active=self.is_active()
        #self.debug()

    def debug(self):
        for i,gui_stopwatch in enumerate(gui_stopwatch_elements):
            stopwatches[i]['name']=gui_stopwatch[0].get()
        print(stopwatches,str_stopwatches(),sep='\n')
        print('len(gui_stopwatch_elements)=',len(gui_stopwatch_elements))
    def render(self,now):
        for i,stopwatch in enumerate(stopwatches):
            if stopwatch['stamps']==[]: continue
            if stopwatch['stamps'][-1][1] is None:
                q=stopwatch['elapsed']+now-stopwatch['stamps'][-1][0]
                #s=time_format(q.total_seconds())
                s=str(q)[0:-7]
                gui_stopwatch_elements[i][3].configure(text=s)
    def render_all(self):
        for i,stopwatch in enumerate(stopwatches):
            #s=str(stopwatch["elapsed"])
            #s=s[0:7]
            gui_stopwatch_elements[i][3].configure(text=str(stopwatch["elapsed"])[0:7])
    def is_active(self):
        for stopwatch in stopwatches:
            if stopwatch['stamps']==[]: continue
            if stopwatch['stamps'][-1][1] is None: return True
        return False

    def tick(self):
        #print('.',end='')
        now=datetime.now()
        if self.active:
            self.render(now)
            self.sroot.after(tic_time, self.tick)


if 1:
    root = tk.Tk()
    root.geometry('600x400')
    timer = Timer(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    print(str_stopwatches())

