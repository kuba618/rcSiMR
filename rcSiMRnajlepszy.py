from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import socket
import time
import threading
import queue
from threading import Thread


s = socket.socket()

        
class rcSiMR(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
 
        okno = Frame(self)
        okno.pack(side = "top", fill = "both", expand = True)
        okno.grid_rowconfigure(0, weight = 1)
        okno.grid_columnconfigure(0, weight = 1)


        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(okno, self)
            self.frames[F] = frame
            frame.grid(row = 0, column =0, sticky = "nsew")

        self.show_frame(StartPage)

    def show_frame(self, okienko):
        frame = self.frames[okienko]
        frame.tkraise()
        

class StartPage(Frame):

    
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.hostt=StringVar()
        self.portt=IntVar()
        tyt2label = Label(self).pack()

        tytlabel = Label(self, font='16',text = "Witaj w programie ").pack()
        tyt1label = Label(self, font='16',text = "do sterowania pojazdem typu RC").pack()
        tyt2label = Label(self).pack()

        self.photo = PhotoImage(file = "logo1.png")
        self.foto=Label(self, image = self.photo)
        self.foto.pack()

        self.udp = ttk.Button(self, text = "Start",
                         command = lambda: controller.show_frame(PageOne))
        polBtn=ttk.Button(self, text = "Połącz",command = self.polaczenie)

        hostLabel = Label(self, text = "Podaj adres IP sieci:").pack()
        hostEntry = Entry(self, textvariable = self.hostt ).pack()
        portLabel = Label(self, text = "Podaj port sieci:").pack()
        portEntry = Entry(self, textvariable = self.portt ).pack()

        tyt2label = Label(self).pack()

        polBtn.pack()


        self.photo2 = PhotoImage(file = "car.png")
        self.photo1 = Label(self, image = self.photo2).pack()

        
    def polaczenie(self):
        try:
            self.host = self.hostt.get()       
            self.port = self.portt.get()    
            s.connect((self.host, self.port))
            s.send('połączono'.encode())
            tkinter.messagebox.showinfo("RC SiMR" ,"Połączono")
            self.udp.pack()


            
        except OSError:
            
            tkinter.messagebox.showinfo("RC SiMR" , "Wprowadź poprawny adres/port lub sprawdź dostępność sieci")

      

class PageOne(Frame, Thread):
    zawart=''
    zawart2=''


    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        Thread.__init__(self)
        
        self.daemon = True
        self.start()
        
        self.serwpis=IntVar()
        self.silwpis=IntVar()

        startBtn = ttk.Button(self, text = "Powrót",
                              command = lambda: controller.show_frame(StartPage))
        servoBtn = ttk.Button(self, text = "servo",
                             command = self.servo)
      
        silnikBtn = ttk.Button(self, text = "silnik",
                             command = self.silnik)


        napisservLabel = Label(self, text = "Wartość na servo:").pack()
        self.suwak=Scale(self, from_=1200, to=1800,resolution = 50, tickinterval=100, orient=HORIZONTAL,
                         length=300, command=self.suwak_wart)
        self.suwak.set(1500)
        self.suwak.pack()
        
        napissilnLabel = Label(self, text = "Wartość na silnik:").pack()
        self.suwak2=Scale(self, from_=1023, to=-1023, tickinterval=250, 
                         length=300, command=self.suwak2_wart)
        self.suwak2.set(0)
        self.suwak2.pack()

        servoLabel = Label(self, text = "Podaj wartość na servo:").pack()        
        servowpis = Entry(self, textvariable = self.serwpis).pack()
        silnikLabel = Label(self, text = "Podaj wartość na silnik:").pack()
        silnikwpis = Entry(self, textvariable = self.silwpis).pack()

        servoBtn.pack()        
        silnikBtn.pack()
        startBtn.pack()
    


    def suwak_wart(self, wart_suwak):
        try:
            self.zawart=wart_suwak
            self.after(10, self.process_queue1)
        except (AttributeError,OSError):
            tkinter.messagebox.showinfo("RC SiMR" , "Czy napewno się połączyłeś?")



    def suwak2_wart(self, wart_suwak2):
        try:
            self.zawart2=wart_suwak2
            self.after(10, self.process_queue2)
        except (AttributeError,OSError):
            tkinter.messagebox.showinfo("RC SiMR" , "Czy napewno się połączyłeś?")

        
    
    def process_queue1(self):
        try:
            
            msg2='ch0 '+self.zawart+'\n'
            s.send(msg2.encode())
            s.close
            
        except (OSError,queue.Empty):
            self.after(10, self.process_queue1)

    def process_queue2(self):
        try:
            msg3='cp1 '+self.zawart2+'\n'
            s.send(msg3.encode())
            s.close            
        except (OSError,queue.Empty):
            self.after(10, self.process_queue2)

  
    def servo(self):
        try:
            if self.serwpis.get() >2300 or self.serwpis.get()<700:
                tkinter.messagebox.showinfo("RC SiMR" , "Podaj poprawną wartość")
            else:
                self.zawart=str(self.serwpis.get())
        except (AttributeError,OSError):
            tkinter.messagebox.showinfo("RC SiMR" , "Czy napewno się połączyłeś?")

            
    def silnik(self):
        try:
            if self.silwpis.get()>1000 or self.silwpis.get()<-1000:
                tkinter.messagebox.showinfo("RC SiMR" , "Podaj poprawną wartość")
            else:
                self.zawart2 = str(self.silwpis.get())
        except (AttributeError,OSError):
            tkinter.messagebox.showinfo("RC SiMR" , "Czy napewno się połączyłeś?")

    def run(self):
        while True:
            time.sleep(0.1)
            self.process_queue1()
            self.process_queue2()



okno=rcSiMR()
okno.geometry("400x600")
okno.title("RC SiMR")
i=PhotoImage(file="logo.ico")
okno.tk.call('wm','iconphoto',okno._w,i)
okno.mainloop()

