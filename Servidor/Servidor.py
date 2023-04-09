from ClienteS import Cliente
from multiprocessing.connection import Listener, AuthenticationError
from multiprocessing import Process
from MonitorClientes import Clientes, CustomManager, Chats
import sys

class Servidor():
    def __init__(self, ip_address):
        CustomManager.register('Cliente', Cliente)
        CustomManager.register('Clientes', Clientes)
        CustomManager.register('Chats', Chats)
        with CustomManager() as manager:
            clientes =  manager.Clientes()
            servidores = manager.Chats()
            
            with  Listener(address=(ip_address, 6000), authkey=b'secret password') as listener:
                cs=0
                while True:
                    try:
                        conn = listener.accept()
                        print ('Conectado con', listener.last_accepted)
                        usuario = conn.recv()
                        c = manager.Cliente(conn, usuario)                        
                        p = Process(target=self.atiende, args=(c, clientes,servidores,))
                        p.start()
                        cs+=1
                    except AuthenticationError:
                        print ('Contraseña incorrecta, conexion rechazada')    
                        
    def atiende(self, c, lClientes, lChats):
        while c.estaEnChat():
            try:
                m = c.recivirMensaje()
                print(m)
                if m == 1: #    quiere comprobar si un nombre de chat ya está registrado
                    print('a')
                    nombre = c.recivirMensaje()
                    c.enviarMensaje(lChats.esta(nombre))
                elif m == 2:  #Quiere entrar a esperar para jugar
                    lClientes.anade(c)
                    c.espera()
                    print(f'{c.getUsuario()} teminado el juego')
                elif m == 6:  #Quiere entrar a esperar para jugar
                    lChats.anade(c.recivirMensaje())
                    print(lChats)
                elif m == -1:
                    c.setEnChat(0)
                    print(f'{c.getUsuario()} ha salido')
                else:
                    c.setEnChat(0)
                    print(f'{c.getUsuario()} instruccion no reconocida, desconectando')                        
            except EOFError:
                print('Conexion cortada')
                break  
        print(f'{c.getUsuario()} ha salido')    
        c.salir() 

if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    Servidor(ip_address)
