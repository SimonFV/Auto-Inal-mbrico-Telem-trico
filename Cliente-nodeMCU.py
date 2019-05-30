#Libreria que permite la conexion
import socket

def connect():
    """Función que recibe las entradas del usuario por medio de inputs, y en base a esto le envía una orden al esp8266.

    Entradas: Como tal, esta función no recibe parámetros, ya que se encarga de ejecutar un ciclo solamente. Además las variables
    utilizadas son locales. Esta trabaja con inputs que el usuario puede realizar en base a una lista de opciones sugeridas
    por el programa, tomando luego ciertas decisiones en base a esta.
    
    Salidas: Un string de un valor codificado en utf-8 para ser procesado por el esp8266, dicho valor varía dependiendo de la
    opción escogida durante los inputs.
    
    Restricciones: Solo procesan las opciones sugeridas por el programa, caso contrario se devolvera un mensaje de error. Es
    importante, también, que la red WiFi a utilizar se encuentre activa antes de iniciar el programa, de lo contrario no podrá
    conectarse, generando un error.

    Punto de parada: El ciclo está hecho para seguir continuamente, aún cuando se ingresa un valor incorrecto, sin embargo, el
    ciclo puede finalizar al desactivarse la red WiFi, o al ingresar el mensaje close.

    """

    #Variable tipo lista que se utiliza para controlar con mayor facilidad los 8 LEDs del auto.
    byte =  [0, 0, 1, 1, 1, 1, 1, 1]
    #Objeto socket que crea el cliente y se conecta al servidor
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Se conecta a la IP y puerto especificados
    s.connect(("192.168.43.200", 7070))
    print("pwm")
    print("dire")
    print("lf")
    print("lb")
    print("ll")
    print("ld")
    print("blvl")
    print("ldr")
    print("close")
    print("circle")
    print("infinite")
    print("zigzag")
    print("especial")
    
    while(True):
        selec = input("Seleccione una opción: ")  ##Selec
        #POTENCIA Y DIRECCION DEL AUTO
        #VALOR NEGATIVO INDICA REVERSA
        if(selec == "pwm"):
            valor = int(input("pwm[-600 - 600]: "))
            if(valor <= 600 and valor >= 0):
                s.send(str(valor+423).encode("utf-8"))
            elif(valor >= -600 and valor < 0):
                s.send(str(-valor+1423).encode("utf-8"))
            else:
                print("Valor incorrecto")
        #DIRECCION: IZQUIERDA / CENTRADO / DERECHA 
        elif(selec ==  "dire"):
            valor  =  input("dire[-1,0,1]: ")
            if(valor == "-1"):
                s.send("402".encode("utf-8"))
            elif(valor == "0"):
                s.send("400".encode("utf-8"))
            elif(valor == "1"):
                s.send("401".encode("utf-8"))
            else:
                print("Valor incorrecto")
        #LUCES FRONTALES
        elif(selec ==  "lf"):
            valor = int(input("lf[0,1]: "))
            if(valor == 1):
                byte[2], byte[3] = 0, 0
                s.send(str(convec(byte,0,0,-1)).encode("utf-8"))
            elif(valor == 0):
                byte[2], byte[3] = 1, 1
                s.send(str(convec(byte,0,0,-1)).encode("utf-8"))
            else:
                print("Valor incorrecto")
        #LUCES DE FRENO
        elif(selec ==  "lb"):
            valor = int(input("lb[0,1]: "))
            if(valor == 1):
                byte[4], byte[5] = 0, 0
                s.send(str(convec(byte,0,0,-1)).encode("utf-8"))
            elif(valor == 0):
                byte[4], byte[5] = 1, 1
                s.send(str(convec(byte,0,0,-1)).encode("utf-8"))      
            else:
                print("Valor incorrecto")
        #LUZ DIRECCIONAL IZQUIERDA
        elif(selec ==  "ll"):
            valor  = int(input("ll[0,1]: "))            
            if(valor == 1):
                byte[7] = 0
                s.send(str(convec(byte,0,0,-1)).encode("utf-8"))
            elif(valor == 0):
                byte[7] = 1
                s.send(str(convec(byte,0,0,-1)).encode("utf-8"))
            else:
                print("Valor incorrecto")
        #LUZ DIRECCIONAL DERECHA
        elif(selec ==  "lr"):
            valor = int(input("lr[0,1]: "))
            if(valor == 1):
                byte[6] = 0
                s.send(str(convec(byte,0,0,-1)).encode("utf-8"))
            elif(valor == 0):
                byte[6] = 1
                s.send(str(convec(byte,0,0,-1)).encode("utf-8"))
            else:
                print("Valor incorrecto")
        #VALOR DE CARGA DE BATERIA
        elif(selec == "blvl"):
            s.send("350".encode("utf-8"))
            carga = s.recv(128)
            carga=str(carga, "utf-8")
            carga=int(carga)
            carga=carga-780
            carga=int((carga/140)*100)
            if(carga>=100):
                print("Nivel de bateria: 100")
            elif(carga<=0):
                print("Nivel de bateria: 0")
            else:
                print("Nivel de bateria: ",carga)
        #NIVEL DE LUZ AMBIENTE
        elif(selec == "ldr"):
            s.send("300".encode("utf-8"))
            luz = s.recv(128)
            luz=int.from_bytes(luz, byteorder='big')
            if(luz==1):
                print("Iluminado")
            else:
                print("Oscuro")
        #MOVIMIENTO CIRCULAR
        elif(selec == "circle"):
            valor=input("circle[-1,1]: ")
            if(valor=="1"):
                s.send("360".encode("utf-8"))
            elif(valor=="-1"):
                s.send("365".encode("utf-8"))
            else:
                print("Valor incorrecto")
        #MOVIMIENTO INFINITO
        elif(selec == "infinite"):
            s.send("370".encode("utf-8"))
        #MOVIMIENTO ZIGZAG
        elif(selec == "zigzag"):
            s.send("380".encode("utf-8"))
        #MOVIMIENTO ESPECIAL
        elif(selec == "especial"):
            s.send("390".encode("utf-8"))
        #CIERRA EL LOOP PARA FINALIZAR LA CONEXION
        elif(selec == "close"):
                break
        else:
            print("Valor incorrecto")
            
    print("Desconectado.")
    s.close()

def convec(b,i,o,s):
    """Función que transforma a entero decimal el resultado de la modificación de la variable byte
    Entradas: b = byte, y es la lista que se recibe, i, o y s son contadores que permiten la transformación de manera recursiva.
    
    Salidas: la transformación de la variable b.

    Restricciones: b solo puede ser una lista con elementos enteros 1 o 0.

    Punto de parada: cuando se alcance el largo de b y se retorne 0.

    """
    
    if(len(b) >= i+1):
        num = b[s]
        build = (2**o)*num       
        return build +  convec(b,i+1,o+1,s-1)
    else:
        return 0

#Auto-documentacion
Auto_Docu1=connect.__name__
document1=connect.__doc__
print(Auto_Docu1, ":")
print(document1)
Auto_Docu2=convec.__name__
document2=convec.__doc__
print(Auto_Docu2, " : ")
print(document2)

#Inicia el programa
connect()
