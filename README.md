# Practica 3
En la carpeta Servidor, los archivos correspondientes al Listener, que sirve como intermediario entre los clientes tanto para el chat como el juego.

En la carpeta Cliente, los del Client, los relacionados con los que se conectan para jugar/hablar.

## Chat

(Los chats con mqtt, la conexion para crear nuevos o buscar existentes con client-listener)

Se tienen chats a los que se puede conectar cualquier cliente, teniendo uno con todos en el que se les deja nada más iniciar por defecto.

Para el servidor hay que ejecutar _Servidor.py_.

Para los clientes, _Inicio.py_: Las acciones que pueden hacer los clientes son:
* Hablar con un bot
* Hablar por chats
* Crear nuevos chats
* Buscar chats ya existentes
* Jugar al juego de spaceInvaders (1 jugador)
* Jugar a un juego multijugador (al pulsar indica que está esperando a que se conecte otro, y hay que darle a aceptar para que se cierre el recuadro, sino no recibe la señal cuando otro jugador se conecta).
## Juego multijugador

(con client-listener)

Si se quiere ejecutar desde fuera del chat:

Para el servidor hay que ejecutar _SalaJuegos.py_.

Para los jugadores, _Jugador.py_: Consiste en pasar el sprite de un lado de la pantalla a otro sin chocar con los obstáculos. Si se llega al otro lado de la pantalla, se suma un punto. Si se choca contra un obstáculo, se resta. Gana el primero que llegue a 10 puntos.

## TODO
* Corregir error que hace que, cuando se abre el juego multijugador desde el chat, al terminar el juego caiga el cliente.
* Finalizar cuando algún jugador llegue a una cierta puntuación.

# Documentos
## En Cliente:
* ChatGUI.py: Contiene las clases chat que se emplean para los chats y la del bot. Se encarga de las funciones de enviar y recibir mensajes y de la interfaz que se muestra al usuario.
* Inicio.py: Crea una ventana de inicio en la que se solicita el nombre al usuario, al recibir el nombre de usuario conecta con el servidor y se lo pasa. Una vez conectado, crea un objeto VentanaGUI.
* Jugador.py: Crea una ventana de juego multijugador que actualiza según los datos que recibe del Listener. En el terminal se informa del lado en el que se encuentra nuestro sprite. Este, se mueve de arriba a abajo con las flechas del teclado y avanza para alejarse de la pared en la que empieza con las felchas de derecha e izquierda. El objetivo es pasar el sprite de un lado de la pantalla a otro sin chocar con los obstáculos. Si se llega al otro lado de la pantalla, se suma un punto. Si se choca contra un obstáculo, se resta.
* VentanaGUI.py: Encargado de la ventana que alberga los chats y el menú de acciones. Es responsable tanto de la lógica de funcionamiento de estos como de la interfaz gráfica del usuario. 
* spaceInvaders.py: Crea una ventana de juego. La nave se puede mover de derecha a izquierda con las flechas del teclado y se dispara con el espacio. El objetivo es destruir el máximo número de asteroides. 
## En Servidor:
* ClienteS.py: Contiene la clase cliente, de la que se crea un objeto por cada cliente que se conecta y que gestiona toda la lógica de los clientes. El objetivo de hacerlo a través de estos, es que se permite definirlos dentro de un BaseManager que protege las acciones que se hacen con estos objetos.
* MonitorClientes.py: Contiene la clase chat, que funciona de forma análoga a la de clientes pero para gestionar los chats. A parte, contiene una clase clientes, cuyo objetivo es contener la lista de clientes conectados al servidor y centralizar todas las funciones relacionadas con esta.
* SalaJuegos.py: Encargado de gestionar el listener en el juego multijugador, lleva la lógica interna del juego transmitiendo a ambos jugadores la situación en cada momento y recibiendo de ellos los datos de movimiento y colisión.
* Servidor.py: Encargado de gestionar el listener, alberga la lógica interna de todo lo relacionado con la comunicación con los clientes. Recive la conexión de clientes, y se queda escuchando las comunicaciones que le llegan para derivar en los objetos apropiados la acción correspondiente.
