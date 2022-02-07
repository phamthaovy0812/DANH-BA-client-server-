import socket
import threading
from tkinter import ttk
from tkinter.ttk import *
import tkinter as sv
from tkinter import messagebox
import time
import os

from tkinter.constants import BOTH, RIGHT, W


FORMAT = "utf8"

ID=[]
Ad=[]

LiveAccount=[]


server_sk= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sk.bind((socket.gethostname(), 22222))
HostIp,port=server_sk.getsockname()
server_sk.listen(3)
            

def acceptClient():
    LiveAccount=server_sk.accept()
    pass
def CheckLiveAccount(ip):
    for row in LiveAccount:
        parse= row.find("-")
        parse_check= row[(parse+1):]
        if parse_check== ip:
            return False
    return True

def RemoveLiveAccount(connection,address):
    for row in LiveAccount:
        parse= row.find("-")
        parse_check=row[:parse]
        if parse_check== str(address):
            parse= row.find("-")
            Ad.remove(parse_check)
            ip= row[(parse+1):]
            ID.remove(ip)
            LiveAccount.remove(row)
            connection.sendall("True".encode(FORMAT))


def check_clientLogIn(ip):
    if CheckLiveAccount(ip)== False:
        return 0
    return 1


def clientConn(sket):

    ip = sket.recv(1024).decode(FORMAT)
    print("IP:--" + ip +"--")

    sket.sendall(ip.encode(FORMAT))
    
    accepted = check_clientLogIn(ip)
    if accepted == 1:
        print("lalalala")
        Accept(sket)
        account=str(Ad[Ad.__len__()-1])
        LiveAccount.append(account)
    if accepted==2:
        print(" ERROR Input !")

    print("accept:", accepted)
    sket.sendall(str(accepted).encode(FORMAT))
    print("end-logIn()")
    print("")

def senddata(server_sk):
    file_names=server_sk.recv(100).decode()    
    print('Send file name:',file_names)
    file_size=os.path.getsize(str(file_names))
    print('Size of file:',file_size)
    server_sk.send(str(file_size).encode())

    with open(file_names,"rb") as file:
        c=0
        start=time.time()
        while c< int(file_size):
            data=file.read(1024)
            if not (data):
                break
            server_sk.sendall(data)
            c+=len(data)
        end=time.time()
    file.close()
    print("File transfer complete! in ",end-start)
    
    

    
def controlClient(conn, addr, page):
        try:
            #x = server_sk.recv(1024).decode(FORMAT)
 
            page.data.insert(sv.END, addr)
            while True:
                senddata(conn)
            # msgy = "oke"
            # conn.send(msgy.encode(FORMAT))
                
            
            return
            #print(x)
            # sendData('thanhvien.json')
            # sendData('thanhvien.json')         

        except:
            page.messagebox(title="Error window",text="No client")
            print("O day co con bug")
        
def Accept(sket):
    bien= "s"
    sket.sendall(bien.encode(FORMAT))

def RUNServer(page): # cai dat da luong
    print(HostIp)
    print("Waiting for Client")

    nClient = 0;
    while (nClient < 3):
        try:
            conn, addr = server_sk.accept() # thread da luong trong python
            thr = threading.Thread(target= controlClient(conn, addr, page), args=(conn, addr))
            thr.daemon = False
            thr.start()
            print("inside: ", nClient)
        except:
            print("Can not connect to client")
            #conn.close()
        nClient += 1
        print("outside: ", nClient)
            
            

 

class ConnPageforSV(sv.Frame): # giao dien login cua server
    def __init__ (self, parent, Server_ctl): # truyen server_ctl vao de goi ham trong Server
        sv.Frame.__init__(self,parent)
        lb_title=sv.Label(self,text="CONNECTION OF SERVER", fg="#008080")
        lb_ip= sv.Label(self,text="IP - ADDRESS",fg="#20B2AA")
        lb_port= sv.Label(self,text="PORT",fg="#20B2AA")
        lb_temp1 = sv.Label(self, text="")

        
        self.set_ip= sv.Text(self, width=20,bg="light yellow",height=1,state='normal')
        self.set_port= sv.Text(self, width=20, bg="light yellow",height=1,state='normal')
        def handle_autobutton(self):  # cai dat nut auto va chuc nang tu dong lay ip va port
            self.set_ip.delete(1.0,sv.END)
            self.set_port.delete(1.0,sv.END)
            self.set_ip.insert(sv.INSERT,HostIp)
            self.set_port.insert(sv.INSERT,port)
        print(type(HostIp))

        autoButton=sv.Button(self,text="Auto",command=lambda:handle_autobutton(self), bg="#008080")
        autoButton.pack()
             
        
        self.lb_notice= sv.Label(self,text="")
        

        button_login= sv.Button(self,text="START",command=lambda:[Server_ctl.Connect(self), acceptClient],bg="#008080")
        button_login.configure(width=10)

        lb_temp1.pack()
        lb_title.pack()
        lb_ip.pack()
        self.set_ip.pack()
        lb_port.pack()
        self.set_port.pack()
        self.lb_notice.pack()
        button_login.pack()


def showData():
    pass
class DisplayInfosPage(sv.Frame): # man hinh hien thi cua server sau khi login thanh cong
    def __init__ (self,parent,Server_ctl):
        sv.Frame.__init__(self,parent)
        lb_temp1 = sv.Label(self, text="")
        lb_temp2 = sv.Label(self, text="")
        lb_temp3 = sv.Label(self, text="")
        
        lb_title = sv.Label(self, text="ACTIVE ACCOUNT ON SERVER", fg="#008080")

        self.conent =sv.Frame(self)
        self.data = sv.Listbox(self.conent, height = 10, 
                  width = 40, 
                  bg='floral white',
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg='#20639b')
        self.data.insert(sv.END,'Waiting for client...')
    
        button_exit=sv.Button(self,text="EXIT",command=lambda:Server_ctl.ShowFrame(ConnPageforSV) ,bg="#DC143C")
        button_refresh=sv.Button(self,text="REFRESH",bg="#008080",command=lambda:RUNServer(self))
        button_exit.configure(width=10)
        button_refresh.configure(width=10)
       
        lb_temp1.pack()
        lb_title.pack()
       
        self.conent.pack_configure()
        self.scroll= sv.Scrollbar(self.conent)
        self.scroll.pack(side =RIGHT, fill= BOTH)
        self.data.config(yscrollcommand = self.scroll.set)
        self.scroll.config(command = self.data.yview)
        self.data.pack()

        lb_temp2.pack()
        button_refresh.pack()
        lb_temp3.pack()
        button_exit.pack()
        
  
        

        
    
        

class Server (sv.Tk):
    def __init__ (self,*args):
        sv.Tk.__init__(self,*args)
        self.title("SERVER")
        self.geometry("500x400")
        self.resizable(width=True, height=True)
        

        container= sv.Frame()
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames= {}
        for F in (ConnPageforSV,DisplayInfosPage):
            frame= F(container,self)
            frame.grid(row=0,column=0,sticky="nsew")
            self.frames[F]=frame
        
        self.frames[ConnPageforSV].tkraise()
      
        
    def ShowFrame(self,FrameRaise ):
        self.frames[FrameRaise].tkraise()
    
    def NotiClose(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def Connect(self,tempFrame):
        ip = tempFrame.set_ip.get('1.0',sv.END)
        port = tempFrame.set_port.get('1.0',sv.END)

        if port == "\n" or ip == '\n':
            tempFrame.lb_notice["text"] = "ERROR: Fields cannot be empty!!!"
            return 
        else:
            self.ShowFrame(DisplayInfosPage)

            

            


   

#--------------------------------------------------------------------------------
#sThread = threading.Thread(target=RUNServer)
#sThread.daemon = True 
#sThread.start()

app=Server()
app.mainloop()



        

