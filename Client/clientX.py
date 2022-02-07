from ctypes import pointer
import socket,os,time
import threading
from tkinter import messagebox
from tkinter import *
import time
#from PIL import ImageTk, Image
from tkinter.messagebox import showinfo
import tkinter as tk
import json
from tkinter import ttk
from tkinter import *
from typing import Sized
import PIL
from PIL import ImageTk, Image
from tkinter.messagebox import showinfo

def requestdata(file_names,client_sk):
    client_sk.send(file_names.encode())
    file_size=client_sk.recv(100).decode()
    print("Size of File Receive :",file_size)

    with open(file_names,'wb') as file:
        c=0
        start=time.time()
        while c<int(file_size):
            data=client_sk.recv(1024)
            if not (data): 
                break
            file.write(data)
            c+=len(data)
        end=time.time()
    file.close()
    #client_sk.close()
    print("File transfer complete! in ",end-start)

FORMAT = "utf8"

def createFrame(Frame,Client):
    for widges in Client.winfo_children():
        widges.destroy()
    container= tk.Frame()
    container.pack(side='top',fill="both",expand=True)
    container.grid_rowconfigure(0,weight=1)
    container.grid_columnconfigure(0,weight=1)
    frame=Frame(container,Client)
    frame.grid(row=0,column=0,sticky="nsew")
    Client.frames[Frame]=frame
    print(Client.frames[Frame])

def ShowFrame(Client,FrameRaise):
    Client.frames[FrameRaise].tkraise()
        
def printPage(Frame,Client):
    createFrame(Frame,Client)
    ShowFrame(Client,Frame)


listOriginal = ['ID','Name','Phone Number','Email', 'Avatar']

def searchID(list, name):
    for e in list:
        if e["ID"] == name:
            listOriginal[0] = e["ID"]
            listOriginal[1] = e["Name"]
            listOriginal[2] = e["PhoneNumber"]
            listOriginal[3] = e["Email"]
            listOriginal[4] = e["Avatar"]
            return e
    return None


def searchName(list, name):
    for e in list:
        if e["Name"] == name:
            listOriginal[0] = e["ID"]
            listOriginal[1] = e["Name"]
            listOriginal[2] = e["PhoneNumber"]
            listOriginal[3] = e["Email"]
            listOriginal[4] = e["Avatar"]
            return e
    return None


def searchPhone(list, name):
    for e in list:
        if e["Phone"] == name:
            listOriginal[0] = e["ID"]
            listOriginal[1] = e["Name"]
            listOriginal[2] = e["PhoneNumber"]
            listOriginal[3] = e["Email"]
            listOriginal[4] = e["Avatar"]
            return e
    return None

def searchMail(list, name):
    for e in list:
        if e["Email"] == name:
            listOriginal[0] = e["ID"]
            listOriginal[1] = e["Name"]
            listOriginal[2] = e["PhoneNumber"]
            listOriginal[3] = e["Email"]
            listOriginal[4] = e["Avatar"]
            return e
    return None

def readImage3(tkt):
    img = PIL.ImageTk.PhotoImage(file="Resource/0.jpg")
    buttomImg = tk.Button(tkt, image=img)
    buttomImg.configure(width=160, height=160)
    buttomImg.image = img
    buttomImg.place(x=700,y=100, anchor='center', bordermode='inside')

def readImage4(tkt, name):
    img = PIL.ImageTk.PhotoImage(file=name)
    buttomImg = tk.Button(tkt, image=img)
    buttomImg.configure(width=300, height=600)
    buttomImg.image = img
    buttomImg.place(x=650,y=300, anchor='center', bordermode='inside')

def readImage5(tkt, name):
    img = PIL.ImageTk.PhotoImage(file=name)
    buttomImg = tk.Button(tkt, image=img)
    buttomImg.configure(height=500)
    buttomImg.image = img
    buttomImg.pack()
    
def jsonRead():
    data = {}
    with open('Resource/thanhvien.json') as f:
        data = json.load(f)
    return data


    




    
      
def pathImage(id):
    data = jsonRead()
    i = 1
    for e in data['people']:
        i = i + 1
        if ( i == id):
            return e["Avatar"]
        
def upDataFrame(showInf, data):
    try:
        requestdata(data[4],client_sk)

        labelId = tk.Label(showInf, text="ID\t\t: "+data[0], font=('Century',14),bg='#20B2AA')
        labelName = tk.Label(showInf, text="Name\t\t: "+data[1], font=('Century',14),bg='#20B2AA')
        labelPhone = tk.Label(showInf, text="Phone Number\t: "+data[2], font=('Century',14),bg='#20B2AA')
        labelEmail = tk.Label(showInf, text="Email\t\t: "+data[3], font=('Century',14),bg='#20B2AA')
        
        labelId.place(x=20, y = 50+50+10+50);
        labelName.place(x=20, y = 80+50+20+50);
        labelPhone.place(x=20, y = 110+50+30+50);
        labelEmail.place(x=20, y = 140+50+40+50);
        readImage4(showInf, data[4])
    except: 
        tk.messagebox.showinfo("Title", "Can not find this person")


def searchInf(name_var, box, showInf):
    name=name_var.get()
    type = box.get()
    data = jsonRead()
    if type == "ID":
        nameFound = searchID(data['people'], name)
    elif type =="Name":
        nameFound = searchName(data['people'], name)
    elif type =="PhoneNumber":
        nameFound = searchPhone(data['people'], name)
    elif type =="Email":
        nameFound = searchMail(data['people'], name)
    
    if nameFound == None:
        tk.messagebox.showinfo("Title", "Can not find this person")
    else: 
        # upDataFrame(ShowInfor,nameFound)
        printPage(ShowInfor,app)

    name_var.set("")
    
def tableScrollbar(tk):
    
    tree = ttk.Treeview(tk)
    tree['show'] = 'headings'
    tree["columns"] = ("No.", "ID", "Name", "Phone Number", "Email")

    s = ttk.Style(tk)
    s.theme_names()
    s.theme_use('xpnative')
    s.configure(".", font=('Helvetica',11), bg="aqua")
    s.configure("Treeview.Heading", foreground='darkred', font=('Helvetica',11, "bold"))
    tk.grid(column=20, row=20, sticky="ns")
    tree.columnconfigure(200, weight=200)

    #tree.geometry("400x300")
    tree.column("No.", width=100, minwidth=100, anchor='center')
    tree.column("ID", width=100, minwidth=100, anchor='center')
    tree.column("Name", width=150, minwidth=100, anchor='center')
    tree.column("Phone Number", width=200, minwidth=150, anchor='center')
    tree.column("Email", width=250, minwidth=150, anchor='center')

    tree.heading("No.", text="No.", anchor='center')
    tree.heading("ID", text="ID", anchor='center')
    tree.heading("Name", text="Name", anchor='center')
    tree.heading("Phone Number", text="Phone Number", anchor='center')
    tree.heading("Email", text="Email", anchor='center')

    data = jsonRead()
 
    i = 1
    for e in data['people']:
        tree.insert('', i, text=e["Avatar"], values=(i, e["ID"], e["Name"], e["PhoneNumber"], e["Email"]))
        i = i + 1
    tree.place(relx=0, rely=0.6, anchor='w', bordermode='inside')
    
    return tree


class ShowInfor(tk.Frame):
    def __init__(self, parent, DataPointer):
        tk.Frame.__init__(self, parent)
        labelTitle = tk.Label(self, text="THE INFORMATION VIEW",bg="#20B2AA", font=('Century',18))
        self.configure(bg="#20B2AA")
        
        buttomLog = tk.Button(self, text="BACK", command= lambda: [printPage(DataPage,app)])
        buttomLog.configure(width=10,bg="#B22222",fg="black")
        
        
        labelTitle.place(relx=0.3, rely=0.1, anchor='center', bordermode='inside')
        
        buttomLog.place(relx=0.5, rely=0.95, anchor='center', bordermode='inside')
        
        

    def clear_frame(self):
       for widgets in ShowInfor.winfo_children():
            widgets.destroy()


class DataPage(tk.Frame):
    def __init__(self, parent, appPointer):
        # requestdata('Resource/thanhvien.json')
        # requestdata('Resource/0.jpg')
        tk.Frame.__init__(self, parent)
        labelTitle3 = tk.Label(self, text="DANH BA SO",fg="#008080", font=('Century',18))
        nameLabel = tk.Label(self, text="ENTER:",bg="#008080", fg="black")
        
       
        self.configure()  
        
        data = "name"
        buttomLog = tk.Button(self, text="EXIT", command= lambda: exit(0))
        buttomShow = tk.Button(self, text="Show Last Person",bg="#AFEEEE",fg="black", command= lambda: [printPage(ShowInfor,app), upDataFrame(ShowFrame(app,ShowInfor), listOriginal)],)
        buttomLog.configure(width=10,bg="#B22222")
        name_var = tk.StringVar()
        buttomSearch = tk.Button(self, text="Search",bg="#008080",fg="black",activeforeground="red", command= lambda: [searchInf(name_var, self.ListType, ShowInfor),upDataFrame(appPointer.ShowFrame(ShowInfor), listOriginal)]) 
        self.entryName = tk.Entry(self,textvariable = name_var, bg="white")

        self.ListType=ttk.Combobox(self,state='readonly')
        list=['ID','Name','Phone Number','Email']
        self.ListType['values']=list
        self.ListType.current(0)

        
        
        labelTitle3.pack(padx=5, pady=20)
        buttomLog.place(relx=0.5, rely=0.9, anchor='center', bordermode='inside')
        nameLabel.place(x=25, y=120+20,   width=100,height=40)
        self.entryName.place(x=127, y=120+20,  width=200,height=40)
        buttomSearch.place(x=490, y=120+20,width=100,height=40)
        #labelAvt.place(x=700,y=200, anchor='center', bordermode='inside')
        buttomShow.place(x=700,y=200, anchor='center', bordermode='inside')
        self.ListType.place(width=150,height=40,x=330,y=120+20)


        tree = tableScrollbar(self)
        list2 = ["ID", "Name", "Phone", "Email", "Avatar"]
        
        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item, "text")
                item2 = tree.item(selected_item, "values")
                list2[0] = item2[1]
                list2[1] = item2[2]
                list2[2] = item2[3]
                list2[3] = item2[4]
                readImage3(self)
                print(list2)

        tree.bind('<<TreeviewSelect>>', item_selected)
        readImage3(self)
        self.showInfPage()
        
    def showInfPage(self):
        container = tk.Frame()
        a = ShowInfor(container, self)
        a.tkraise()

class ConnPageforCL(tk.Frame):
    def __init__ (self, parent, Client_ctl): # truyen server_ctl vao de goi ham trong Server
        tk.Frame.__init__(self,parent)
        lb_title=tk.Label(self,text="CONNECT TO SERVER ", fg="#008080")
        lb_ip= tk.Label(self,text="IP",fg="#20B2AA")
      
 
        lb_temp1 = tk.Label(self, text="")
     
        name_var = tk.StringVar()
        self.set_ip= tk.Entry(self, width=20,bg="light yellow", textvariable=name_var)


        self.lb_notice= tk.Label(self,text="")
        button_login= tk.Button(self,text="START",command=lambda:[Client_ctl.Connect(self)], bg="#008080")
        button_login.configure(width=10)

        lb_temp1.pack()
        lb_title.pack()
        lb_ip.pack()
        self.set_ip.pack()
        self.lb_notice.pack()
        button_login.pack()

   
class Client(tk.Tk):
    def ShowFrame(self,FrameRaise):
        self.frames[FrameRaise].tkraise()
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("CLIENT")
        self.geometry("800x600+250+20")
        self.resizable(width=False, height=False)


        self.frames= {}
        
        
        printPage(ConnPageforCL,self)

    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            try:
                option = "EXIT"
                client_sk.sendall(option.encode(FORMAT))
            except:
                pass
        
    def Connect(self,tempFrame):
        ip= tempFrame.set_ip.get()
        if ip=="":
            tempFrame.lb_notice["text"]="ERROR!!!"
            return
        else:
            try:
                server_address = ((ip, 22222))
                client_sk.connect(server_address) 
                tempFrame.lb_notice["text"]="Connect Successfull "

                requestdata("Resource/thanhvien.json",client_sk)
                requestdata("Resource/0.jpg",client_sk)
                # note = client_sk.recv(100).decode(FORMAT)
                # print(note)
                #requestdata("Resource/0.jpg",client_sk)
                # mgx = "Nan vl"
                # client_sk.sendall(mgx.encode(FORMAT))
                # mgy = client_sk.recv(100).decode(FORMAT)
                # print(mgy)
                # mgx2 = "Nan p2"
                # client_sk.sendall(mgx2.encode(FORMAT))
                # mgx = "exit"
                # client_sk.sendall(mgx.encode(FORMAT))
                printPage(DataPage,app)
            except:
                tempFrame.lb_notice["text"]="Can not Connect to Server!!!"
                return
        #notice server for starting connect

        


    def DisConn(self,curFrame, sck):
        try:
            option = "EXIT"
            sck.sendall(option.encode(FORMAT))
            accepted = sck.recv(1024).decode(FORMAT)
            if accepted == "True":
                self.showFrame(ConnPageforCL)
        except:
            curFrame.lb_notice["text"] = "Error: ha3"




#------------------------- main-----------------

print("CLIENT SIDE")
client_sk= socket.socket(socket.AF_INET, socket.SOCK_STREAM)


if not os.path.exists('Resource'):
    os.makedirs('Resource')
    
app= Client()
try:
    app.mainloop()
except:
    client_sk.close()

finally:
    client_sk.close()
        