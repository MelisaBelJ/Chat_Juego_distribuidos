from tkinter import *               
from tkinter import ttk 
from VentanaGUI import VentanaGUI
from multiprocessing.connection import Client
from multiprocessing import Process, Lock, Value
import sys

    """
    
    Abre ventana con título y tamaño indicados para selección de
    nombre de usuario para el chat a través de VentanaGUI.
    Finalmente, cierra la ventana de selección de nombre de usuario.
    
    """

class Inicio():
    
    """
    
    Especificaciones de título, tamaño y botones de selección
    
    """
    
    def __init__(self, ip_address):   
        print ('Intentando conectar')
        self.conn = Client(address=(ip_address, 6000), authkey=b'secret password')
        self.main = Tk()
        self.main['bg'] = '#c3c4c7'
        self.main.title("Inicio")
        self.main.geometry("200x50")
        self.main.resizable(False, False)
        self.main.eval('tk::PlaceWindow . center')
        self.main.resizable(height = None, width = None)   
        self.main.bind_all("<Control-w>", lambda x: self.main.destroy())
        
        name = Label(self.main, text='Nombre de usuario')  
        name.pack(expand=1, side = TOP, fill = BOTH)
        
        self.t = Entry(self.main)
        self.t.pack(side=LEFT, expand = 1, fill = BOTH)
        
        b = Button(self.main, command = self.lee, text = "Aceptar", width = 10)
        self.main.bind_all("<Return>", lambda x: self.lee())
        b.pack(side = RIGHT, fill = Y)
        
        self.main.focus_force()
        self.t.focus_force()
        self.main.mainloop()
        
    """
    
    Lee el contenido y se lo manda al servidor y cierra al terminar
    
    """
    
    def lee(self):
        self.name = self.t.get().rsplit(' ')[0]
        self.conn.send(self.name)
        self.main.destroy()
        self.ventana = VentanaGUI(self.conn, self.name)
        print('salir')
        self.conn.send('Q')
        self.conn.close()
  
    """
    
    Conecta con la dirección IP indicada
    
    """
    
if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    i = Inicio(ip_address)
