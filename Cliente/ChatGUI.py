from tkinter import *               
from tkinter import ttk
from paho.mqtt.client import Client
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
from multiprocessing import Process, Lock, Value, Queue

hostname = 'simba.fdi.ucm.es'
base_topic = '/clients/Practica3Chats/'

"""
Clase para gestionar los chats, tanto lo que se muestra por pantalla como la recepción y 
envío de mensajes, que se hace con mqtt.
"""
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
        
        #Inicializamos el chat con el nombre del usuario, la pestaña en la que se abre y el nombre de esta
    def inicializa(self, yo, tab, topic):
        self.queue = Queue()
        self.yo = yo
        self.main = tab
        self.f1 = Frame(self.main )
        self.f2 = Frame(self.main )
        self.scrollbar = Scrollbar(self.f1) #Barra para poder desplazar la pantalla del chat arriba y abajo
        self.scrollbar.pack( side = RIGHT, fill = Y )
        
        self.mylist = Text(self.f1, yscrollcommand = self.scrollbar.set, bg = '#08385e', fg = 'white') #Donde se muestra el chat
        
        self.mylist.pack( side = LEFT, expand = 1, fill = BOTH )
        self.scrollbar.config( command = self.mylist.yview )
        
        self.t = Entry(self.f2)#Cuadro de texto para escribir mensajes
        self.t.pack(side=LEFT, expand = 1, fill ="both")  
        
        self.b = Button(self.f2, command = self.lee, text = "Enviar", width = 10)#Boton enviar
        self.b.pack(side=RIGHT, fill = Y)    
        #self.main.bind("<Return>", lambda x: self.lee())
        
        self.f1.pack(side=TOP,expand = 1, fill = BOTH)    
        self.f2.pack(side = BOTTOM, fill = X)    
        
        #Lee el mensaje en el cuadro de texto y lo publica
    def lee(self):
        me = self.t.get()
        self.t.delete(0, END)  
        m = Mensaje(self.yo, me)      
        publish.single(self.topic,  m.muestra(' '), hostname=hostname)
        
        #recibe un objeto mensaje y lo introduce en el chat
    def escribe(self, mensaje):
        self.mylist.config(state = NORMAL)
        self.mylist.insert(END, mensaje.muestra(self.yo) +'\n')
        self.mylist.config(state = DISABLED)
        
        """
        Cuando hay un mensaje nuevo en el servidor, lo añade a la cola de mensajes para que cuando se llegue al proceso
        que actualiza la ventana, esta se actualice con los nuevos mensajes escritos
        """
    def on_message(self,mqttc,userdata,msg):
        rec = str(msg.payload)[2:-1].split(': ')
        m = Mensaje(rec[0],rec[1])
        self.queue.put(m)
        
        #Lee la cola de mensajes recibidos y los escribe por el chat.
    def checkEscribe(self):
        if not self.queue.empty():
            self.escribe(self.queue.get())

 """ 
Clase para gestionar los chats con un bot, tanto lo que se muestra por pantalla como la recepción y 
envío de mensajes.
 """
class Bot():
    def __init__(self, yo, tab):
        self.inicializa(yo, tab, 'Bot')
    
    """
    lee los mensajes, los escribe por pantalla y escribe la respuesta que corresponda,
    """
    def lee(self):
        me = self.t.get()
        m = Mensaje(self.yo, me)
        self.escribe(m)
        self.t.delete(0, END)
        self.escribe(Mensaje('Bot', self.responde(me)))
        
    """
    Respuestas ya creadas del bot para ciertos mensajes,
    si no tiene ninguna dice que es desconocida.
    """
    def responde(self, m):
        m = m.lower()
        if m == 'hola' or m == 'adios':
            return m
        elif 'nuevo servidor' in m:
            return 'Pulsar CTRL+N para crear un nuevo servidor'
        elif 'buscar servidor' in m:
            return 'Pulsar CTRL+B para buscar un servidor'
        elif 'jugar' in m:
            return 'Pulsar CTRL+J para jugar un juego individual. \n Pulsar CTRL+M para jugar un juego multijugador.'
        else:
            return "Instrucción desconocida"
    
    """
    Se inicializa con el nombre del bot, la pestaña en la que se encuentra y el nombre de la pestaña
    """
    def inicializa(self, yo, tab, nombre):
        self.yo = yo
        self.main = tab
        self.nombre = nombre
        self.f1 = Frame(self.main )
        self.f2 = Frame(self.main )
        self.scrollbar = Scrollbar(self.f1)  #Barra para poder desplazar la pantalla del chat arriba y abajo
        self.scrollbar.pack( side = RIGHT, fill = Y )
        
        self.mylist = Text(self.f1, yscrollcommand = self.scrollbar.set, bg = '#08385e', fg = 'white') #Espacio en el que se muestran los mensajes
        
        self.mylist.pack( side = LEFT, expand = 1, fill = BOTH )
        self.scrollbar.config( command = self.mylist.yview )
        
        self.t = Entry(self.f2) #Espacio en el que escribe el usuario el mensaje
        self.t.pack(side=LEFT, expand = 1, fill ="both")  
        
        self.b = Button(self.f2, command = self.lee, text = "Enviar", width = 10) #Boton enviar mensaje
        self.b.pack(side=RIGHT, fill = Y)    
        #self.main.bind("<Return>", lambda x: self.lee())
        
        self.f1.pack(side=TOP,expand = 1, fill = BOTH)    
        self.f2.pack(side = BOTTOM, fill = X)    
        
        #recibe un objeto mensaje y lo introduce en el chat
    def escribe(self, mensaje):
        self.mylist.config(state = NORMAL)
        self.mylist.insert(END, mensaje.muestra(self.yo))
        self.mylist.config(state = DISABLED)
            
"""
Clase para asegurar que los mensajes del chat siguen la estructura usuario: contenido
"""
class Mensaje():
    def __init__(self, usuario, contenido):
        self.usuario = usuario
        self.contenido = contenido
        
        #Formatea el mensaje para mostrar por el chat
    def muestra(self, yo):
        u = 'Yo' if self.usuario == yo else self.usuario
        return f"{u}: {self.contenido}"
     
     #Avisa si el mensaje es de salida
    def deSalida(self):
        return (self.usuario, self.contenido.lower()) != ('', 'adios')
