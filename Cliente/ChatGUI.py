from tkinter import *               
from tkinter import ttk
from paho.mqtt.client import Client
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
from multiprocessing import Process, Lock, Value, Queue

hostname = 'simba.fdi.ucm.es'
base_topic = '/clients/Practica3Chats/'

class ChatGUI():
    def __init__(self, yo, tab, topic):
        self.inicializa(yo, tab, topic)
        userdata = {}
        mqttc = Client(userdata = userdata)
        mqttc.on_message = self.on_message
        mqttc.connect(hostname)
        self.topic = base_topic+topic
        mqttc.subscribe(self.topic)
        m = Mensaje(self.yo, 'Ha entrado')      
        publish.single(self.topic,  m.muestra(' '), hostname=hostname)
        mqttc.loop_start()
        
    def inicializa(self, yo, tab, topic):
        self.queue = Queue()
        self.yo = yo
        self.main = tab
        self.f1 = Frame(self.main )
        self.f2 = Frame(self.main )
        self.scrollbar = Scrollbar(self.f1)
        self.scrollbar.pack( side = RIGHT, fill = Y )
        
        self.mylist = Text(self.f1, yscrollcommand = self.scrollbar.set, bg = '#08385e', fg = 'white')
        
        self.mylist.pack( side = LEFT, expand = 1, fill = BOTH )
        self.scrollbar.config( command = self.mylist.yview )
        
        self.t = Entry(self.f2)
        self.t.pack(side=LEFT, expand = 1, fill ="both")  
        
        self.b = Button(self.f2, command = self.lee, text = "Enviar", width = 10)
        self.b.pack(side=RIGHT, fill = Y)    
        #self.main.bind("<Return>", lambda x: self.lee())
        
        self.f1.pack(side=TOP,expand = 1, fill = BOTH)    
        self.f2.pack(side = BOTTOM, fill = X)    
        
    def lee(self):
        me = self.t.get()
        self.t.delete(0, END)  
        m = Mensaje(self.yo, me)      
        publish.single(self.topic,  m.muestra(' '), hostname=hostname)
        
    def escribe(self, mensaje):
        self.mylist.config(state = NORMAL)
        self.mylist.insert(END, mensaje.muestra(self.yo) +'\n')
        self.mylist.config(state = DISABLED)
        
    def on_message(self,mqttc,userdata,msg):
        rec = str(msg.payload)[2:-1].split(': ')
        m = Mensaje(rec[0],rec[1])
        self.queue.put(m)
        
    def checkEscribe(self):
        if not self.queue.empty():
            self.escribe(self.queue.get())

class Bot():
    def __init__(self, yo, tab):
        self.inicializa(yo, tab, 'Bot')
        
    def lee(self):
        me = self.t.get()
        m = Mensaje(self.yo, me)
        self.escribe(m)
        self.t.delete(0, END)
        self.escribe(Mensaje('Bot', self.responde(me)))
        
    def responde(self, m):
        m = m.lower()
        if m == 'hola' or m == 'adios':
            return m
        elif m == 'nuevo servidor':
            return 'Pulsar CTRL+N para crear un nuevo servidor'
        elif m == 'buscar servidor':
            return 'Pulsar CTRL+B para buscar un servidor'
        else:
            return "Instrucción desconocida"
        
    def inicializa(self, yo, tab, nombre):
        self.yo = yo
        self.main = tab
        self.nombre = nombre
        self.f1 = Frame(self.main )
        self.f2 = Frame(self.main )
        self.scrollbar = Scrollbar(self.f1)
        self.scrollbar.pack( side = RIGHT, fill = Y )
        
        self.mylist = Text(self.f1, yscrollcommand = self.scrollbar.set, bg = '#08385e', fg = 'white')
        
        self.mylist.pack( side = LEFT, expand = 1, fill = BOTH )
        self.scrollbar.config( command = self.mylist.yview )
        
        self.t = Entry(self.f2)
        self.t.pack(side=LEFT, expand = 1, fill ="both")  
        
        self.b = Button(self.f2, command = self.lee, text = "Enviar", width = 10)
        self.b.pack(side=RIGHT, fill = Y)    
        #self.main.bind("<Return>", lambda x: self.lee())
        
        self.f1.pack(side=TOP,expand = 1, fill = BOTH)    
        self.f2.pack(side = BOTTOM, fill = X)    
        
    def escribe(self, mensaje):
        self.mylist.config(state = NORMAL)
        self.mylist.insert(END, mensaje.muestra(self.yo))
        self.mylist.config(state = DISABLED)
            
class Mensaje():
    def __init__(self, usuario, contenido):
        self.usuario = usuario
        self.contenido = contenido
        
    def muestra(self, yo):
        u = 'Yo' if self.usuario == yo else self.usuario
        return f"{u}: {self.contenido}"
        
    def deSalida(self):
        return (self.usuario, self.contenido.lower()) != ('', 'adios')
