from tkinter import *               
from tkinter import ttk, simpledialog, messagebox
from ChatGUI import ChatGUI, Bot
from multiprocessing.connection import Client
from multiprocessing import Process, Lock, Value
from spaceInvaders.spaceInvaders import JuegoIndividual
import Jugador
  
class VentanaGUI():  
    def __init__(self, conn, nUsuario):
        self.conn = conn
        self.nUsuario = nUsuario
        self.tabs = {}
        self.chats = {}
        self.creaVentana()
    
    def creaVentana(self):
        self.main = Tk()
        self.main['bg'] = 'black'
        self.main.title("Conversaciones")
        self.main.geometry("500x500")
        self.main.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main.resizable(height = None, width = None)
        self.main.bind_all("<Control-w>", lambda x: self.main.destroy())
        
        barra_menus = Menu()
        menu_acciones = Menu(barra_menus, tearoff=False)
        menu_acciones.add_command(label="Nuevo Servidor", accelerator = "Ctrl+N", command = self.creaChat)
        self.main.bind_all("<Control-n>", lambda x: self.creaChat())
        menu_acciones.add_command(label="Buscar Servidor", accelerator = "Ctrl+B", command = self.buscaChat)
        self.main.bind_all("<Control-b>", lambda x: self.creaChat())
        menu_acciones.add_command(label="Jugar solo", accelerator = "Ctrl+J", command = self.juegoSolo)
        self.main.bind_all("<Control-j>", lambda x: self.juegoSolo())
        menu_acciones.add_command(label="Jugar con otro", accelerator = "Ctrl+M", command = self.juegoCon)
        self.main.bind_all("<Control-m>", lambda x: self.juegoCon())
        barra_menus.add_cascade(menu=menu_acciones, label="Acciones")
        self.main.config(menu=barra_menus)
        
        self.tabControl = ttk.Notebook(self.main)
        self.nuevoChat('bot', False)
        Bot(self.nUsuario, self.tabs['bot'])
        self.nuevoChat('Default')
        self.tabControl.pack(expand = 1, fill ="both")            
        
        self.main.focus_force()
        self.abierto = Value('i',1)
        while self.abierto.value == 1:
            self.checkEscribe()
            
    def checkEscribe(self):
        for _,chat in self.chats.items():
            chat.checkEscribe()
        self.main.update()
        
    def on_closing(self):
        self.conn.send(-1)
        self.abierto.value = 0
        self.main.destroy()
        
    def ventanaInput(self, mensaje):
        m= simpledialog.askstring('Nombre', mensaje)
        return (m+' ').rsplit(' ')[0]
        
    def nuevoChat(self, usuario, x = True):
        self.tabs[usuario] = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tabs[usuario], text = usuario)
        self.tabControl.select(self.tabs[usuario])
        if x:
            self.chats[usuario] = ChatGUI(self.nUsuario, self.tabs[usuario], usuario)
            self.conn.send(6)
            self.conn.send(usuario)
    
    def creaChat(self):
        usuario = self.ventanaInput('Nombre del servidor a crear')
        if usuario != '':
            self.conn.send(1)
            self.conn.send(usuario)
            if self.conn.recv() == 0:
                self.nuevoChat(usuario)
            else:
                msg_box = messagebox.askquestion('Ya existe', 'El servidor ya existe, ¿unirse a ese?', icon='warning')
                if msg_box == 'yes':
                    self.nuevoChat(usuario)
            
    def buscaChat(self):
        usuario = self.ventanaInput('Nombre del servidor a buscar')
        if usuario != '':
            self.conn.send(1)
            self.conn.send(usuario)
            if self.conn.recv() == 1:
                self.nuevoChat(usuario)
            else:
                msg_box = messagebox.askquestion('No existe', 'Servidor no encontrado, ¿crear uno con ese nombre?', icon='warning')
                if msg_box == 'yes':
                    self.nuevoChat(usuario)

    def juegoSolo(self):
        JuegoIndividual()
            
    def juegoCon(self):
        messagebox.showinfo('Esperando', 'Esperando a que otro jugador se conecte')
        self.conn.send(2)
        if self.conn.recv() == 1: #si lo encuentra llamamos al juego para que se inicie pasándole self.conn 
            J = Jugador.empiezaJuego(self.conn)
        
