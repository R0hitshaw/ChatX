import socket
import threading
import tkinter as tk
import tkinter.scrolledtext
from tkinter import simpledialog

HOST='127.0.0.1'
PORT=9090

class Client:
    def __init__(self,host,port):

        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host, port))

        root=tk.Tk()
        root.withdraw()

        self.nickname=simpledialog.askstring("Nickname", "Please choose a Nickname",parent=root)

        self.gui_done=False

        self.running=True

        gui_thread=threading.Thread(target=self.gui_loop)
        recieve_thread=threading.Thread(target=self.receive)

        gui_thread.start()
        recieve_thread.start()

    def gui_loop(self):
        self.win=tk.Tk()
            
        self.win.configure(bg="black")
        
        self.chat_label=tk.Label(self.win,text="ChatX:",bg="lightgray")
        self.chat_label.config(font=("Arial",17))
        self.chat_label.pack(padx=20,pady=5)
       
        self.text_area=tk.scrolledtext.ScrolledText(self.win,height=35,width=170)
        self.text_area.pack(padx=20,pady=5)
        self.text_area.config(state='disabled') 

        self.msg_label=tk.Label(self.win,text="Type Message:",bg="lightgray")
        self.msg_label.config(font=("Arial",15))
        self.msg_label.pack(padx=20,pady=5,anchor="w")

        self.imput_area=tk.Text(self.win,height=5,width=170)
        self.imput_area.pack(padx=20,pady=5)

        self.send_button=tk.Button(self.win,text="Send",command=self.write) 
        self.send_button.config(font=("Arial",12))
        self.send_button.pack(padx=20,pady=5)

        self.gui_done=True
        self.win.protocol("WM_DELETE WINDOW",self.stop)
        self.win.mainloop()

    def write(self):
        message=f"{self.nickname}:{self.imput_area.get('1.0','end')}"
        self.sock.send(message.encode('utf-8'))
        self.imput_area.delete('1.0','end')
    def stop(self):
        self.running=False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message=self.sock.recv(1024).decode('utf-8')
                if message=="NICK":
                    self.sock.send(self.nickname.encode('utf-8'))

                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')

            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

client=Client(HOST,PORT)
