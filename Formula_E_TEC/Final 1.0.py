docu = """INSTITUTO TECNOLÓGICO DE COSTA RICA.
CURSO DE TALLER DE PROGRAMACIÓN
TERCER PROYECTO PROGRAMADO: FÓRMULA E CE
PROFESOR: Msc. PEDRO GUITIERREZ
ESTUDIANTES: MARCO PICADO 2018310184
SIMÓN FALLAS 2019324313
BRANDON MUÑOZ CAMPOS 2018087204
PRIMER SEMESTRE 2019
FECHA DE ENTREGA 18 DE JUNIO DE 2019
FECHA DE EMISIÓN: 03 DE JUNIO DE 2019
FECHA DE ÚLTIMA MODIFICACIÓN: 
VERSIÓN 0.1.4"""


####################################Bibliotecas necesarias####################
from tkinter import *
import os
from shutil import copyfile
from tkinter import ttk
from tkinter import filedialog
import shutil
import time
import socket
import winsound

#######################################################################
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.43.200", 7070))
lista =["Alfa Romeo Racing","Ferrari", "Toyota", "McLaren", "Haas F1 Team", "Red Bull", "Honda", "Lotus", "BMW Sauber"]
filename = ""
byte =  [0, 0, 1, 1, 0, 0, 1, 1]
avanzar = 0
retrocede = 0
giraD = 0
giraI = 0
vel = 0
contadorLuz = -1
blink_izq = -1  #Varable para controlar las luces direccionales
blink_der = -1

def cargarImg(nombre):
    """Recibe una imagen que carga desde la ruta especificada
       Entradas: Nombre de la imagen que se quiera cargar
       Salidas: imagen que se cargó
       Restricciones: solo recibe un nombre dado desde otra función.
       """
    ruta=os.path.join('imag',nombre)
    imagen=PhotoImage(file=ruta)
    return imagen

def cargarImg2(nombre):
    """Recibe una imagen que carga desde la ruta especificada
       Entradas: Nombre de la imagen que se quiera cargar
       Salidas: imagen que se cargó
       Restricciones: solo recibe un nombre dado desde otra función.
       """
    ruta=os.path.join('autos_img',nombre)
    imagen=PhotoImage(file=ruta)
    return imagen

######### Crea la tabla de posiciones de pilotos y autos #########
def tabla():
    """Función que crea la tabla de posiciones de pilotos y autos
    Entradas: no recibe parámetros, solo continúa bajo el hilo de ejecución
    Salidas: una ventana con sus configuraciones y un objeto instanciado a una clase
    Restricciones: Solo crea la nueva ventana"""
    #Conf de la ventana
    ven=Toplevel()
    ven.title("Tabla de posiciones de pilotos y autos")
    ven.minsize(800,600)
    ven.resizable(width=NO, height=NO)
    C_ve=Canvas(ven, width = 800, height = 600, bg= "black")
    car=cargarImg("pilotos_img2.gif")
    fondo=Label(ven, bg="black")
    fondo.place(x=0,y=0)
    fondo.config(image=car)
    
    objeto_lista=clase_lista(ven)
    
class clase_lista():
    """Clase lista que mueve el carro
    Entradas: no tiene parámetros como entrada aunque lee las teclas
    Salidas: una señal de movimiento, una nueva aventana "master"
    Restricciones: solamente opera siguiendo el hilo de ejecición
    """
    def __init__(self, master):
        #llaves
        self.key=-5
        self.key_pi=5
        self.pos=0
        self.lock=0
        self.bandera=0
        #Diccionario para los labels de pilotos y autos
        self.di={}
        #ventana
        self.ve=master
        self.car=cargarImg("pilotos_img2.gif")
        self.fondo=Label(self.ve, bg="black")
        self.fondo.place(x=0,y=0)
        self.fondo.config(image=self.car)
        #Botones: piloto, auto, salir
        self.boton_autos = Button(self.ve, text="AUTOS", command=lambda:self.control(),fg='yellow',bg='blue')
        self.boton_autos.grid(pady=2, padx=2, row=0, column=3, columnspan=3)
        self.boton_volver = Button(self.ve, text="Volver", command=lambda:self.ve.destroy(),fg='yellow',bg='blue')
        self.boton_volver.grid(pady=2, padx=2, row=0, column=5)

        self.main_pilotos()
        self.ve.mainloop()
        
    #Funcion que permite cambiar de listas entre pilotos y autos
    def control(self):
        if(self.lock==0):
            self.key=-3
            self.pi_destroy(0,0)
            self.car=cargarImg("formula e.gif")
            self.fondo.config(image=self.car)
            self.boton_autos.configure(text="PILOTOS")
            self.main_autos()
        elif(self.lock==1):
            self.key=-5
            self.au_destroy(0,0)
            self.car=cargarImg("pilotos_img2.gif")
            self.fondo.config(image=self.car)
            self.boton_autos.configure(text="AUTOS")
            self.main_pilotos()

    #Funcion principal que muestra la lista de pilotos
    def main_pilotos(self):
        self.lock=0
        self.posicion=Label(self.ve, text="Posición", wraplength=100)
        self.posicion.grid(pady=2, padx=2, row=1, column=0)
        self.name=Label(self.ve, text="Nombre", wraplength=100)
        self.name.grid(pady=2, padx=2, row=1, column=1)
        self.age=Label(self.ve, text="Edad", wraplength=100)
        self.age.grid(pady=2, padx=2, row=1, column=2)
        self.nat=Label(self.ve, text="Nacionalidad", wraplength=100)
        self.nat.grid(pady=2, padx=2, row=1, column=3)
        self.tem=Label(self.ve, text="Temporada", wraplength=100)
        self.tem.grid(pady=2, padx=2, row=1, column=4)
        self.comp=Label(self.ve, text="Competencias", wraplength=100)
        self.comp.grid(pady=2, padx=2, row=1, column=5)
        self.l_rgp=Button(self.ve,text="RGP",command=lambda:self.main_pilotos1(-5))
        self.l_rgp.grid(pady=2, padx=2, row=1, column=6)
        self.l_rep=Button(self.ve,text="REP",command=lambda:self.main_pilotos1(-6))
        self.l_rep.grid(pady=2, padx=2, row=1, column=7)
        #Matriz con los datos de los pilotos procesados del texto
        self.m_plt=self.matriz_pilotos()
        self.ordenar_pi()
        self.constr_tabla_pi(0,0)
    #Controla la forma en que se ordenan los pilotos dependiendo del boton presionado
    def main_pilotos1(self,k):
        if(k==-5):
            if(self.key==-5):
                self.key=5
                self.pos=10
            else:
                self.key=-5
                self.pos=0
        if(k==-6):
            if(self.key==-6):
                self.key=6
                self.pos=10
            else:
                self.key=-6
                self.pos=0
        self.pi_destroy(0,0)
        self.main_pilotos()

    #Construye los labels de la tabla de pilotos en la interfaz
    def constr_tabla_pi(self,b,c):
        if(b<len(self.m_plt)):
            if(len(self.m_plt[b])>c):
                self.di[str(b)+str(c)]=Label(self.ve, text=self.m_plt[b][c], bd=2, relief="ridge") #Labels
                self.di[str(b)+str(c)].grid(pady=2, padx=2, row=b+2, column=c+1)
                self.constr_tabla_pi(b,c+1)
            else:
                if(self.pos>0):
                    self.di[str(b)+str(c+1)]=Label(self.ve, text=str(self.pos))
                else:
                    self.di[str(b)+str(c+1)]=Label(self.ve, text=str(b+1))
                self.di[str(b)+str(c+1)].grid(pady=2, padx=2, row=b+2, column=0) #Posicion
                self.di[str(b)+str(c)]=Button(self.ve,text="Modificar",command=lambda:self.mod_pil(b)) #Boton Modificar
                self.di[str(b)+str(c)].grid(pady=2, padx=2, row=b+2, column=c+2)
                self.di[str(b)+str(c+2)]=Button(self.ve,text="Prueba",command=lambda:self.autos_disp(b))#Boton TEST
                self.di[str(b)+str(c+2)].grid(pady=2, padx=2, row=b+2, column=c+3)
                if(self.m_plt[b][3]!="2019"):
                    self.di[str(b)+str(c+2)].configure(state="disable")
                self.pos-=1
                self.constr_tabla_pi(b+1,0)
    #Guarda los datos de pilotos desde el txt
    def matriz_pilotos(self):
        self.pilotos=open("pilotos.txt", "r")
        self.sc=self.pilotos.readlines()
        self.pilotos.close()
        return self.mc_plt(0,[])
    #Construye la matriz de los datos de los pilotos
    def mc_plt(self,b,m):
        if(len(self.sc)>b):
            t=int(self.sc[b+4][:-1]) #competencias
            v=int(self.sc[b+5][:-1]) #primer lugar
            p=int(self.sc[b+6][:-1]) #segundo lugar
            a=int(self.sc[b+7][:-1]) #abandonos
            li=[]
            li=li+[self.sc[b][:-1]] #nombre
            li=li+[self.sc[b+1][:-1]] #edad
            li=li+[self.sc[b+2][:-1]] #nacionalidad
            li=li+[self.sc[b+3][:-1]] #año temporada
            li=li+[t]               #competencias
            li=li+[int(((v+p)/(t-a))*100)] #RGP
            li=li+[int(((v)/(t-a))*100)] #REP
            m=m+[li]
            return self.mc_plt(b+8,m)
        else:
            return m
    #Ventana para modificar los datos de pilotos
    def mod_pil(self,b):
        self.ve_pi=Toplevel()
        self.ve_pi.title("Modificando datos...")
        self.ve_pi.minsize(420,360)
        self.ve_pi.resizable(width=NO, height=NO)
        self.ve_pi.config(bg="gray60")
        Label(self.ve_pi, text="Datos").grid(pady=2, padx=2, row=0, column=0)
        Label(self.ve_pi, text="Antiguos").grid(pady=2, padx=2, row=0, column=1)
        Label(self.ve_pi, text="Nuevos").grid(pady=2, padx=2, row=0, column=2)
        Label(self.ve_pi, text="Nombre").grid(pady=2, padx=2, row=1, column=0)
        Label(self.ve_pi, text="Edad").grid(pady=2, padx=2, row=2, column=0)
        Label(self.ve_pi, text="Nacionalidad").grid(pady=2, padx=2, row=3, column=0)
        Label(self.ve_pi, text="Año de Temporada").grid(pady=2, padx=2, row=4, column=0)
        Label(self.ve_pi, text="Cant. Competencias").grid(pady=2, padx=2, row=5, column=0)
        Label(self.ve_pi, text="Veces 1er Lugar").grid(pady=2, padx=2, row=6, column=0)
        Label(self.ve_pi, text="Veces 2/3er Lugar").grid(pady=2, padx=2, row=7, column=0)
        Label(self.ve_pi, text="Cant. Abandonos").grid(pady=2, padx=2, row=8, column=0)
        Label(self.ve_pi, text=self.sc[(b*8)]).grid(pady=2, padx=2, row=1, column=1)
        Label(self.ve_pi, text=self.sc[(b*8)+1]).grid(pady=2, padx=2, row=2, column=1)
        Label(self.ve_pi, text=self.sc[(b*8)+2]).grid(pady=2, padx=2, row=3, column=1)
        Label(self.ve_pi, text=self.sc[(b*8)+3]).grid(pady=2, padx=2, row=4, column=1)
        Label(self.ve_pi, text=self.sc[(b*8)+4]).grid(pady=2, padx=2, row=5, column=1)
        Label(self.ve_pi, text=self.sc[(b*8)+5]).grid(pady=2, padx=2, row=6, column=1)
        Label(self.ve_pi, text=self.sc[(b*8)+6]).grid(pady=2, padx=2, row=7, column=1)
        Label(self.ve_pi, text=self.sc[(b*8)+7]).grid(pady=2, padx=2, row=8, column=1)
        self.di_get_pi(0)
        self.acep_pi = Button(self.ve_pi, text="GUARDAR", command=lambda:self.piloto_get(b,0),fg='yellow',bg='blue')
        self.acep_pi.grid(pady=2, padx=2, row=9, column=0)
        self.voler_pi = Button(self.ve_pi, text="VOLVER", command=lambda:self.ve_pi.destroy(),fg='yellow',bg='blue')
        self.voler_pi.grid(pady=2, padx=2, row=9, column=1)
    def di_get_pi(self,b):
        if(b<8):
            self.di["get"+str(b)]=Entry(self.ve_pi)
            self.di["get"+str(b)].grid(row=b+1, column=2)
            self.di_get_pi(b+1)
    #Reccoje los datos nuevos ingresados
    def piloto_get(self,b,z):
        if(z<8):
            self.input_pi=self.di["get"+str(z)].get()
            if(self.input_pi!=""):
                self.sc[(b*8)+z]=str(self.input_pi)+'\n'
            self.piloto_get(b,z+1)
        self.write_pi()
        self.pi_destroy(0,0)
        self.main_pilotos()
        self.ve_pi.destroy()
    #Sobreescribe los datos al txt de pilotos
    def write_pi(self):
        self.pilotos=open("pilotos.txt", "w")
        self.pilotos.write("")
        self.pilotos.close()
        self.pilotos=open("pilotos.txt", "a")
        self.escr_pi(0)
        self.pilotos.close()
    def escr_pi(self,b):
        if(b<len(self.sc)):
            self.pilotos.write(self.sc[b])
            self.escr_pi(b+1)
    #Destruye los labels de los pilotos para agregar nuevos
    def pi_destroy(self,b,c):
        if(b<len(self.m_plt)):
            if(len(self.m_plt[b])>c):
                self.di[str(b)+str(c)].grid_remove()
                self.pi_destroy(b,c+1)
            else:
                self.di[str(b)+str(c+1)].grid_remove()
                self.di[str(b)+str(c)].grid_remove()
                self.di[str(b)+str(c+2)].grid_remove()
                self.pi_destroy(b+1,0)
        self.posicion.grid_remove()
        self.name.grid_remove()
        self.age.grid_remove()
        self.nat.grid_remove()
        self.tem.grid_remove()
        self.comp.grid_remove()
        self.l_rgp.grid_remove()
        self.l_rep.grid_remove()

    #Ordena la lista dependiendo del valor de key
    def ordenar_pi(self):
        if(self.key==5): #RGP asc
            self.key_pi=5
            self.m_plt=self.pil_merge(self.m_plt)
            self.sc=self.update_pi(self.m_plt,self.sc,0,0)
            self.write_pi()
        elif(self.key==-5): #RGP desc
            self.key_pi=5
            self.m_plt=self.pil_merge2(self.m_plt)
            self.sc=self.update_pi(self.m_plt,self.sc,0,0)
            self.write_pi()
        elif(self.key==6):  #REP asc
            self.key_pi=6
            self.m_plt=self.pil_merge(self.m_plt)
            self.sc=self.update_pi(self.m_plt,self.sc,0,0)
            self.write_pi()
        elif(self.key==-6): #REP desc
            self.key_pi=6
            self.m_plt=self.pil_merge2(self.m_plt)
            self.sc=self.update_pi(self.m_plt,self.sc,0,0)
            self.write_pi()
    #Actualiza la variable con los datos del texto de pilotos, en base a la matriz
    def update_pi(self,x,y,b,c):
        if(len(x)>b):
            if(x[b][0]==y[c*8][:-1]):
                i=0
                while(i<8):
                    m=y[b*8+i]
                    y[b*8+i]=y[c*8+i]
                    y[c*8+i]=m
                    i+=1
                return self.update_pi(x,y,b+1,0)
            else:
                return self.update_pi(x,y,b,c+1)
        else:
            return y
            
    #Ordena los pilotos de forma ascendente usando merge sort
    def pil_merge(self,mat):
        if(len(mat)>=2):
            li1=mat[:len(mat)//2]
            li2=mat[-(len(mat)-len(li1)):]
            return self.sort(self.pil_merge(li1), self.pil_merge(li2))
        elif(len(mat)==1):
            return mat
    def sort(self, li1, li2):
        if(len(li1)>0 and len(li2)>0):
            if(li1[0][self.key_pi]>li2[0][self.key_pi]):
                return [li2[0]] + self.sort(li1, li2[1:])
            else:
                return [li1[0]] + self.sort(li1[1:], li2)
        else:
            return li1 + li2
    #Ordena los pilotos de forma descendente
    def pil_merge2(self,mat):
        if(len(mat)>=2):
            li1=mat[:len(mat)//2]
            li2=mat[-(len(mat)-len(li1)):]
            return self.sort2(self.pil_merge2(li1), self.pil_merge2(li2))
        elif(len(mat)==1):
            return mat
    def sort2(self, li1, li2):
        if(len(li1)>0 and len(li2)>0):
            if(li1[0][self.key_pi]<li2[0][self.key_pi]):
                return [li2[0]] + self.sort2(li1, li2[1:])
            else:
                return [li1[0]] + self.sort2(li1[1:], li2)
        else:
            return li1 + li2

######## AUTOS ###################################################################################
    #Selecciona un auto disponible para test drive
    def autos_disp(self, b):
        self.env_au=Toplevel()
        self.env_au.title("Seleccionando auto...")
        self.env_au.minsize(150,200)
        self.env_au.resizable(width=NO, height=NO)
        self.env_au.config(bg="gray60")
        self.autostxt=open("autos.txt", "r")
        self.sc2=self.autostxt.readlines()
        self.autostxt.close()
        self.autos_disp2(0,b)
    def autos_disp2(self,z,b):
        if(len(self.sc2)>z*12):
            if(self.sc2[z*12+4][:-1]=="Disponible"):
                self.di["auto"+str(b)]=Button(self.env_au,text=self.sc2[z*12])
                self.di["auto"+str(b)].configure(command=lambda:self.init_test(z,b)) #Boton Test
                self.di["auto"+str(b)].grid(pady=2, padx=2, row=z, column=0)
            self.autos_disp2(z+1,b)
        else:
            self.di["auto"+str(b)]=Button(self.env_au,text="Cancelar",command=lambda:self.env_au.destroy()) #Boton Test
            self.di["auto"+str(b)].grid(pady=2, padx=2, row=z, column=0)
    def init_test(self,z,b):
        test_drive(self.sc[b*8][:-1],self.sc[b*8+2][:-1],z)
        
    #Manipula los labes principales de la lista de autos
    def main_autos(self):
        self.lock=1
        self.marca=Label(self.ve, text="Marca", wraplength=100)
        self.marca.grid(pady=2, padx=2, row=1, column=0)
        self.modelo=Label(self.ve, text="Modelo", wraplength=100)
        self.modelo.grid(pady=2, padx=2, row=1, column=1)
        self.tempo=Label(self.ve, text="Temporada", wraplength=100)
        self.tempo.grid(pady=2, padx=2, row=1, column=2)
        self.efic=Button(self.ve,text="Eficiencia",command=lambda:self.main_autos1(-3))
        self.efic.grid(pady=2, padx=2, row=1, column=3)
        self.estado=Label(self.ve, text="Estado", wraplength=100)
        self.estado.grid(pady=2, padx=2, row=1, column=4)
        self.foto=Label(self.ve, text="Foto", wraplength=100)
        self.foto.grid(pady=2, padx=2, row=1, column=5)

        #Matriz con los datos de los autos procesados del texto
        self.m_au=self.matriz_autos()
        self.ordenar_au()
        self.constr_tabla_au(0,0)
    #Cambia lo valores de key para reordenar la tabla
    def main_autos1(self,k):
        if(k==-3):
            if(self.key==-3):
                self.key=3
            else:
                self.key=-3
        self.au_destroy(0,0)
        self.main_autos()
        
    #Construye los labels de la tabla de autos en la interfaz
    def constr_tabla_au(self,b,c):
        if(b<len(self.m_au)):
            if(len(self.m_au[b])-1>c):
                self.di[str(b)+str(c)]=Label(self.ve, text=self.m_au[b][c], bd=2, relief="ridge") #Labels
                self.di[str(b)+str(c)].grid(pady=2, padx=2, row=b+2, column=c)
                self.constr_tabla_au(b,c+1)
            else:
                self.di[str(b)+str(c+2)]=Button(self.ve,text="Modificar",command=lambda:self.mod_au(b)) #Boton Modificar
                self.di[str(b)+str(c+2)].grid(pady=2, padx=2, row=b+2, column=c+1)
                self.di[str(b)+str(c+1)]=Button(self.ve,text="Ver",command=lambda:self.ver_foto(b))#FOTO
                self.di[str(b)+str(c+1)].grid(pady=2, padx=2, row=b+2, column=c)
                self.constr_tabla_au(b+1,0)
        else:
            self.bot_agre=Button(self.ve,text="Agregar Auto",command=lambda:self.agregar_au(b))
            self.bot_agre.grid(pady=2, padx=2, row=b+2, column=3)
    #Guarda los datos de autos desde el txt
    def matriz_autos(self):
        self.autostxt=open("autos.txt", "r")
        self.sc2=self.autostxt.readlines()
        self.autostxt.close()
        return self.mc_au(0,[])
    #Construye la matriz de los datos de los autos
    def mc_au(self,b,m):
        if(len(self.sc2)>b):
            li=[]
            li=li+[self.sc2[b][:-1]] #marca
            li=li+[self.sc2[b+1][:-1]] #modelo
            li=li+[self.sc2[b+2][:-1]] #temporada
            li=li+[self.sc2[b+3][:-1]] #eficiencia
            li=li+[self.sc2[b+4][:-1]] #estado
            li=li+[self.sc2[b+5][:-1]] #foto
            m=m+[li]
            return self.mc_au(b+12,m)
        else:
            return m
    #Ventana para modificar los datos de los autos
    def mod_au(self,b):
        self.ve_au=Toplevel()
        self.ve_au.title("Modificando datos...")
        self.ve_au.minsize(420,360)
        self.ve_au.resizable(width=NO, height=NO)
        self.ve_au.config(bg="gray60")
        Label(self.ve_au, text="Datos").grid(pady=2, padx=2, row=0, column=0)
        Label(self.ve_au, text="Antiguos").grid(pady=2, padx=2, row=0, column=1)
        Label(self.ve_au, text="Nuevos").grid(pady=2, padx=2, row=0, column=2)
        Label(self.ve_au, text="Marca").grid(pady=2, padx=2, row=1, column=0)
        Label(self.ve_au, text="Modelo").grid(pady=2, padx=2, row=2, column=0)
        Label(self.ve_au, text="Temporada").grid(pady=2, padx=2, row=3, column=0)
        Label(self.ve_au, text="Eficiencia").grid(pady=2, padx=2, row=4, column=0)
        Label(self.ve_au, text="Estado").grid(pady=2, padx=2, row=5, column=0)
        Label(self.ve_au, text="Foto").grid(pady=2, padx=2, row=6, column=0)
        Label(self.ve_au, text="País").grid(pady=2, padx=2, row=7, column=0)
        Label(self.ve_au, text="Baterias").grid(pady=2, padx=2, row=8, column=0)
        Label(self.ve_au, text="Tensión").grid(pady=2, padx=2, row=9, column=0)
        Label(self.ve_au, text="Consumo").grid(pady=2, padx=2, row=10, column=0)
        Label(self.ve_au, text="Sensores").grid(pady=2, padx=2, row=11, column=0)
        Label(self.ve_au, text="Peso").grid(pady=2, padx=2, row=12, column=0)
        Label(self.ve_au, text=self.sc2[(b*12)]).grid(pady=2, padx=2, row=1, column=1)
        Label(self.ve_au, text=self.sc2[(b*12)+1]).grid(pady=2, padx=2, row=2, column=1)
        Label(self.ve_au, text=self.sc2[(b*12)+2]).grid(pady=2, padx=2, row=3, column=1)
        Label(self.ve_au, text=self.sc2[(b*12)+3]).grid(pady=2, padx=2, row=4, column=1)
        Label(self.ve_au, text=self.sc2[(b*12)+4]).grid(pady=2, padx=2, row=5, column=1)
        Label(self.ve_au, text=self.sc2[(b*12)+5]).grid(pady=2, padx=2, row=6, column=1)
        Label(self.ve_au, text=self.sc2[(b*12)+6]).grid(pady=2, padx=2, row=7, column=1)
        Label(self.ve_au, text=self.sc2[(b*12)+7]).grid(pady=2, padx=2, row=8, column=1)
        Label(self.ve_au, text=self.sc2[(b*12)+8]).grid(pady=2, padx=2, row=9, column=1)
        Label(self.ve_au, text=self.sc2[(b*12)+9]).grid(pady=2, padx=2, row=10, column=1)
        Label(self.ve_au, text=self.sc2[(b*12)+10]).grid(pady=2, padx=2, row=11, column=1)
        Label(self.ve_au, text=self.sc2[(b*12)+11]).grid(pady=2, padx=2, row=12, column=1)
        self.di_get_au(0,b)
        self.acep_au = Button(self.ve_au, text="GUARDAR", command=lambda:self.auto_get(b,0,1),fg='yellow',bg='blue')
        self.acep_au.grid(pady=2, padx=2, row=5, column=3)
        self.voler_au = Button(self.ve_au, text="VOLVER", command=lambda:self.ve_au.destroy(),fg='yellow',bg='blue')
        self.voler_au.grid(pady=2, padx=2, row=6, column=3)
    def di_get_au(self,b,c):
        if(b<12 and b!=5):
            self.di["geta"+str(b)]=Entry(self.ve_au)
            self.di["geta"+str(b)].grid(row=b+1, column=2)
            self.di_get_au(b+1,c)
        elif(b==5):
            self.di["geta"+str(b)]=Button(self.ve_au,text="Cambiar",command=lambda:self.foto_carro(c)) #Mod Foto
            self.di["geta"+str(b)].grid(row=b+1, column=2)
            self.di_get_au(b+1,c)
    #Reccoje los datos nuevos ingresados
    def auto_get(self,b,z,p):
        if(p==1):
            if(z<12):
                if(z!=5):
                    self.input_au=self.di["geta"+str(z)].get()
                    if(self.input_au!=""):
                        self.sc2[(b*12)+z]=str(self.input_au)+'\n'
                    self.auto_get(b,z+1,p)
                else:
                    self.auto_get(b,z+1,p)
            self.write_au()
            self.au_destroy(0,0)
            self.main_autos()
            self.ve_au.destroy()
        elif(p==2):
            if(z<12):
                if(z!=5):
                    self.input_au=self.di["geta"+str(z)].get()
                    if(self.input_au!=""):
                        self.sc2[(b*12)+z]=str(self.input_au)+'\n'
                        self.auto_get(b,z+1,p)
                    elif(self.input_au==""):
                        self.bandera=1
                        self.auto_get(b,z+1,p)
                else:
                    self.auto_get(b,z+1,p)
            elif(self.bandera==0):
                self.write_au()
                self.au_destroy(0,0)
                self.main_autos()
                self.ve_add.destroy()
            elif(self.bandera==1):
                self.sc2=self.sc2[:-12]
                self.bandera=0
                self.ve_add.destroy()
    #Sobreescribe los datos al txt de autos
    def write_au(self):
        self.autostxt=open("autos.txt", "w")
        self.autostxt.write("")
        self.autostxt.close()
        self.autostxt=open("autos.txt", "a")
        self.escr_au(0)
        self.autostxt.close()
    def escr_au(self,b):
        if(b<len(self.sc2)):
            self.autostxt.write(self.sc2[b])
            self.escr_au(b+1)
    #Destruye los labels de los autos para agregar nuevos
    def au_destroy(self,b,c):
        if(b<len(self.m_au)):
            if(len(self.m_au[b])>c):
                self.di[str(b)+str(c)].grid_remove()
                self.au_destroy(b,c+1)
            else:
                self.di[str(b)+str(c+1)].grid_remove()
                self.di[str(b)+str(c)].grid_remove()
                self.au_destroy(b+1,0)
        self.marca.grid_remove()
        self.modelo.grid_remove()
        self.tempo.grid_remove()
        self.efic.grid_remove()
        self.estado.grid_remove()
        self.foto.grid_remove()
        self.bot_agre.grid_remove()

    #Ordena la lista dependiendo del valor de key
    def ordenar_au(self):
        if(self.key==3): #Eficiencia asc
            self.m_au=self.au_merge(self.m_au)
            self.sc2=self.update_au(self.m_au,self.sc2,0,0)
            self.write_au()
        elif(self.key==-3): #Eficiencia desc
            self.m_au=self.au_merge2(self.m_au)
            self.sc2=self.update_au(self.m_au,self.sc2,0,0)
            self.write_au()
    #Actualiza la variable con los datos del texto de autos, en base a la matriz
    def update_au(self,x,y,b,c):
        if(len(x)>b):
            if(x[b][0]==y[c*12][:-1]):
                i=0
                while(i<12):
                    m=y[b*12+i]
                    y[b*12+i]=y[c*12+i]
                    y[c*12+i]=m
                    i+=1
                return self.update_au(x,y,b+1,0)
            else:
                return self.update_au(x,y,b,c+1)
        else:
            return y
            
    #Ordena los autos de forma ascendente usando merge sort
    def au_merge(self,mat):
        if(len(mat)>=2):
            li1=mat[:len(mat)//2]
            li2=mat[-(len(mat)-len(li1)):]
            return self.sort3(self.au_merge(li1), self.au_merge(li2))
        elif(len(mat)==1):
            return mat
    def sort3(self, li1, li2):
        if(len(li1)>0 and len(li2)>0):
            if(li1[0][3]>li2[0][3]):
                return [li2[0]] + self.sort3(li1, li2[1:])
            else:
                return [li1[0]] + self.sort3(li1[1:], li2)
        else:
            return li1 + li2
    #Ordena los autos de forma descendente
    def au_merge2(self,mat):
        if(len(mat)>=2):
            li1=mat[:len(mat)//2]
            li2=mat[-(len(mat)-len(li1)):]
            return self.sort4(self.au_merge2(li1), self.au_merge2(li2))
        elif(len(mat)==1):
            return mat
    def sort4(self, li1, li2):
        if(len(li1)>0 and len(li2)>0):
            if(li1[0][3]<li2[0][3]):
                return [li2[0]] + self.sort4(li1, li2[1:])
            else:
                return [li1[0]] + self.sort4(li1[1:], li2)
        else:
            return li1 + li2
        
    #Cambia la foto del auto
    def foto_carro(self,c):
        self.foto_au=self.sele_archivo()
        if(self.foto_au!=''):
            self.dest="autos_img/"+self.sc2[c*12][:-1]+str(c)+".gif"
            shutil.copy(self.foto_au,self.dest)
            self.sc2[c*12+5]=self.sc2[c*12][:-1]+str(c)+".gif"+'\n'
    def sele_archivo(self):
        filename = filedialog.askopenfilename(initialdir="Users",title="Selecione una foto: ",defaultextension=(("gif","*.gif")))
        return filename
    #Crea una ventana para ver la foto del auto
    def ver_foto(self, b):
        self.au_foto=Toplevel()
        self.au_foto.title(self.sc2[b*12][:-1])
        self.au_foto.minsize(640,360)
        C_au=Canvas(self.au_foto, width = 640, height = 360, bg= "black")
        self.car2=cargarImg2(self.sc2[b*12+5][:-1])
        self.fondo_au2=Label(self.au_foto, bg="black")
        self.fondo_au2.place(x=0,y=0)
        self.fondo_au2.config(image=self.car2)
    #Ventana que permite ingresar los datos de un nuevo auto
    def agregar_au(self, b):
        self.ve_add=Toplevel()
        self.ve_add.title("Agregando auto...")
        self.ve_add.minsize(420,360)
        self.ve_add.resizable(width=NO, height=NO)
        self.ve_add.config(bg="gray60")

        Label(self.ve_add, text="Marca").grid(pady=2, padx=2, row=1, column=0)
        Label(self.ve_add, text="Modelo").grid(pady=2, padx=2, row=2, column=0)
        Label(self.ve_add, text="Temporada").grid(pady=2, padx=2, row=3, column=0)
        Label(self.ve_add, text="Eficiencia").grid(pady=2, padx=2, row=4, column=0)
        Label(self.ve_add, text="Estado").grid(pady=2, padx=2, row=5, column=0)
        Label(self.ve_add, text="Foto").grid(pady=2, padx=2, row=6, column=0)
        Label(self.ve_add, text="País").grid(pady=2, padx=2, row=7, column=0)
        Label(self.ve_add, text="Baterias").grid(pady=2, padx=2, row=8, column=0)
        Label(self.ve_add, text="Tensión").grid(pady=2, padx=2, row=9, column=0)
        Label(self.ve_add, text="Consumo").grid(pady=2, padx=2, row=10, column=0)
        Label(self.ve_add, text="Sensores").grid(pady=2, padx=2, row=11, column=0)
        Label(self.ve_add, text="Peso").grid(pady=2, padx=2, row=12, column=0)
        self.sc2=self.sc2+["__\n","__\n","__\n","__\n","__\n","__\n","__\n","__\n","__\n","__\n","__\n","__\n"]
        
        self.di_get_au2(0,b)
        self.acep_au = Button(self.ve_add, text="GUARDAR", command=lambda:self.auto_get(b,0,2),fg='yellow',bg='blue')
        self.acep_au.grid(pady=2, padx=2, row=5, column=3)
        self.voler_au = Button(self.ve_add, text="VOLVER", command=lambda:self.ve_add.destroy(),fg='yellow',bg='blue')
        self.voler_au.grid(pady=2, padx=2, row=6, column=3)
    def di_get_au2(self,b,c):
        if(b<12 and b!=5):
            self.di["geta"+str(b)]=Entry(self.ve_add)
            self.di["geta"+str(b)].grid(row=b+1, column=2)
            self.di_get_au2(b+1,c)
        elif(b==5):
            self.di["geta"+str(b)]=Button(self.ve_add,text="Seleccionar",command=lambda:self.foto_carro(c)) #Mod Foto
            self.di["geta"+str(b)].grid(row=b+1, column=2)
            self.di_get_au2(b+1,c)
    
##Funcion de la ventana de inicio
def main():
    """Función principal del juego
    Entradas: ninguna
    Salidas: Crea un objeto que instancia a una clase
    Restricciones: dada la baja complejidad de la función, no se han encontrado restricciones"""
    
    root = Tk()
    objeto = principal(root)

class principal:
    """Función principal
        Entradas: ventana principal
        Salidas: creación de archivos, y salidas en pantalla
        Restricciones: No tiene una restriccion clara"""
    def __init__(self, master):
        self.root=master
        self.root.title("Tercer proyecto Marco, Simón y Brandon. 2019")
        self.root.minsize(800, 600)
        self.root.resizable(width=NO, height=NO)

        self.archivo = open("patrocinadores.txt", "r")
        self.text = self.archivo.readlines()
        self.archivo.close()


        self.C_root=Canvas(self.root, width = 800, height = 600, bg= "white")
        self.lista_patrocinio = []
        self.patrocinio = StringVar()

        #####imagen de pantalla principal####################
        self.carg=cargarImg("formula e.gif")#extraida de: https://www.kienyke.com/deportes/mas-deportes/disenos-carros-de-formula-1-en-el-mundial-de-rusia
        self.imag_prin=Label(self.root, bg='white')
        self.imag_prin.place(x=0,y=0)
        self.imag_prin.config(image=self.carg)

        self.cargaLogo=cargarImg("logo.gif")
        self.L_logo=Label(self.root)
        self.L_logo.config(image=self.cargaLogo)
        self.L_logo.place(x=200, y=160)
        
        self.L_escuderia = Label(self.root, text = "Escudería McLaren", font=("Gothic", 14), fg="red", bg="white")
        self.L_escuderia.place(x=15, y=160)
    

        self.boton_cerrar=Button(self.root, text='CERRAR', command=self.root.destroy,bg='white',fg='red',relief ="flat", height = 1, font = "Calibri 14")
        self.boton_cerrar.pack(fill= X, side = BOTTOM)
        self.boton_about= Button(self.root,text='ABOUT:',command=self.ventana_about,bg='white',fg='red',relief ="flat", height = 1, font = "Calibri 14")
        self.boton_about.pack(fill= X, side = BOTTOM)
        self.btn_logo = Button(self.root, text="SELECCIONA UN LOGO", command = self.seleccion_logo, fg = "red", bg = "white", relief = "flat", height = 1, font = "Calibri 14")
        self.btn_logo.pack(fill= X, side = BOTTOM)
        self.btn_escuderia = Button(self.root, text='LISTA', command=lambda:tabla(),bg='white',fg='red',relief ="flat", height = 1, font = "Calibri 14")
        self.btn_escuderia.pack(fill= X, side = BOTTOM)
        self.L_titulo=Label(self.root, text="CLASSIC \n FORMULA \n E", font=("Agency FB",30), bg="white",fg="red").place(x=10,y=10)
        self.L_temporada = Label(self.root, text="Temporada 01 2019", font=("Gothic", 14), bg="white", fg="red").place(x=15, y=200)
                                                                                                                            
        self.L_ubicacion = Label(self.root, text="Ubicación: Praga", font=("Gothic", 14), bg="white", fg="red").place(x=15, y=230)
        self.L_patroc = Label(self.root, text="Introduce un Patrocinador: ", font=("Gothic", 14), bg="white", fg="red").place(x=15, y=420)
        self.E_patroc = Entry(self.root, textvariable=self.patrocinio).place(x=252, y=423)
        self.btn_patrocin = Button(self.root, text='Añadir', command=self.añadir_patrocinador,bg='red',fg='light grey')
        self.btn_patrocin.place(x=425, y=420)
        self.L_patro = Label(self.root, text="Patrocinadores: ", font=("Gothic", 14), bg="white", fg="red", width = 14, anchor = "w").place(x=630, y=10)
        self.lee_lista( 0, 35)
        self.indice = Label(self.root, text="Indice Ganador: 0.7", font=("Gothic", 14), bg="white", fg="red").place(x=15, y=260)
        
            
        """"""
        self.root.mainloop()
    def lee_lista(self, x, t):
        if x <= len(self.text)-1:
            self.lab=Label(self.root, text=self.text[x], font=("Gothic", 14), bg="white", fg="red", width = 14, anchor = "w") .place(x=630, y=t)
            return self.lee_lista( x+1, t+25)


    def seleccion_logo(self):
        #global cargaLogo
        self.L_logo
        self.filename = filedialog.askopenfilename(initialdir = "sfv02", title = "Seleciona un logo: ", defaultextension=(("gif","*.gif")))
        if(self.filename!=''):
            shutil.copy(self.filename,"imag/logo.gif")
            self.cargaLogo=cargarImg("logo.gif")
            self.L_logo.config(image=self.cargaLogo)
    
    def añadir_patrocinador(self):
        self.archivo = open("patrocinadores.txt", "r+")
        text = self.archivo.readlines()
        print(text)
        self.archivo.write(self.patrocinio.get()+"\n")
        self.archivo.close()



    def ventana_about(self):
        """Función que crea la ventana de about
        Entradas: no tiene argumentos pero recibe la orden desde el botón de pantalla principal
        Salidas: ventana de about
        Restricciones: solo ejecuta la ventana about
        """
        self.about=Toplevel()
        self.about.title('Acerca de este software:')
        self.about.minsize(800,600)
        self.about.resizable(width=NO, height=NO)
    
        self.C_about=Canvas(self.about, width=800,height=600,bg='light green')
        self.C_about.place(x=0,y=0)
        self.E_about=Label(self.about,text=docu,font=('Agency FB',20)).place(x=115,y=30)
        
        self.btn_atras=Button(self.about, text="ATRAS", command=self.about.destroy,fg='green',bg='white')
        self.btn_atras.place(x=10,y=560)

    def escuderia(self):
        self.escuderia1 = Toplevel()
        self.escuderia1.title("Escuderías Participantes")
        self.escuderia1.minsize(600, 200)
        self.escuderia1.resizable(width = NO, height = NO)
    
        self.C_escuderia = Canvas(self.escuderia1, width=600, height=400, bg= "light green").place(x=0,y=0)
        self.lista_2 = ["Praga", "Viena", "Estambul", "El Cairo", "Sidney", "San Luis", "Ontario", "Cambridge", "Sao Paulo", "Shangai"]
        self.lista_2.sort()
        self.lista_3 = ["Mercedes Benz", "Toyota", "Marlboro", "Ursa", "Intel", "Playstation", "Shell", "Mitsubishi", "Nissan", "Tesla"]
        self.lista_3.sort()
    
        self.label1=Label(self.escuderia1, text = "Selecciona una Ubicación: ", font=("Agency FB",11), bg="grey",fg="light yellow").place(x=10,y=15)
        self.label3=Label(self.escuderia1, text = "Selecciona un patrocinador: ", font=("Agency FB",11), bg="grey",fg="light yellow").place(x=10,y=65)
        self.combo_ubic=self.combo_patroc = ttk.Combobox(self.escuderia1)
        self.combo_ubic["values"] = self.lista_2
        self.combo_ubic.place(x=270, y=15)
        self.combo_patroc = ttk.Combobox(self.escuderia1)
        self.combo_patroc["values"] = self.lista_3
        self.combo_patroc.place(x=270, y=65)
        print(self.combo_ubic.get())



## selec = 5(MOVIMIENTO ESPECIAL)
## selec = 6 (luces izquierdas) selec = 7 (luces derechas)

def movs(selec, luz):
    """"Función responsable de los movimientos del carro
    Entradas: selec y luz, manipulan los led's
    Salidas: manupulación de las luces de auto
    Restricciones: Solo opera con ambis parámetros preasignados
    """
    global byte
    if(selec == 4):
        if(luz == 1):
            byte[2], byte[3]  = 0, 0
            s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        else:
            byte[2], byte[3]  = 1, 1
            s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
    elif(selec == 5):  ###aca va el movimiento especial
        s.send((str(390) + "r").encode("utf-8"))
    elif(selec == 6):
        if(luz == 0):
            byte[7] = 0
            s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        else:
            byte[7] = 1
            s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
    elif(selec == 7):
        if(luz == 0):
            byte[6] = 0
            s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))           
        else:
            byte[6] = 1
            s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))     
    elif(selec == "Mae Parry"):
        byte[2], byte[3] = 1, 1
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        s.send((str(451) + "r").encode("utf-8"))
        byte[2], byte[3] = 0, 0
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        time.sleep(1)
        byte[2], byte[3] = 1, 1
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        time.sleep(1)
        byte[2], byte[3] = 0, 0
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        time.sleep(3)
        s.send((str(450) + "r").encode("utf-8"))  
    elif(selec == "Lola Bentley"):
        s.send((str(401) + "r").encode("utf-8"))
        s.send((str(451) + "r").encode("utf-8")) 
        time.sleep(3)
        s.send((str(450) + "r").encode("utf-8"))          
    elif(selec == "Astrid Guerrero"):
        s.send((str(451) + "r").encode("utf-8"))
        time.sleep(3)
        s.send((str(452) + "r").encode("utf-8"))
        time.sleep(2)
        s.send((str(450) + "r").encode("utf-8"))                             
    elif(selec == "Isra Woolley"):                   
        s.send((str(451) + "r").encode("utf-8"))
        time.sleep(1)
        s.send((str(401) + "r").encode("utf-8"))
        s.send((str(451) + "r").encode("utf-8")) 
        time.sleep(3)
        s.send((str(402) + "r").encode("utf-8"))
        s.send((str(451) + "r").encode("utf-8")) 
        time.sleep(3)
        s.send((str(401) + "r").encode("utf-8"))
        s.send((str(451) + "r").encode("utf-8")) 
        time.sleep(3)
        s.send((str(450) + "r").encode("utf-8"))
    elif(selec == "Aairah Cullen"):
        s.send((str(402) + "r").encode("utf-8"))
        s.send((str(451) + "r").encode("utf-8")) 
        time.sleep(3)
        s.send((str(450) + "r").encode("utf-8"))
    elif(selec == "Maude Walsh"):                  #pare 450, 451 acelere, y 452 reversa
        s.send((str(401) + "r").encode("utf-8"))
        s.send((str(451) + "r").encode("utf-8")) 
        time.sleep(1.5)
        s.send((str(402) + "r").encode("utf-8"))
        time.sleep(1.5)
        s.send((str(450) + "r").encode("utf-8"))
    elif(selec == "Bluebell Roberts"):            
        byte[2], byte[3] = 1, 1
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        s.send((str(401) + "r").encode("utf-8"))
        time.sleep(1)
        s.send((str(402) + "r").encode("utf-8"))
        time.sleep(0.5)
        byte[2], byte[3] = 0, 0
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        time.sleep(1)
        byte[2], byte[3] = 1, 1
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        time.sleep(1)
        byte[2], byte[3] = 0, 0
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        s.send((str(400) + "r").encode("utf-8"))   
    elif(selec == "Uzair Spooner"):
        byte[2], byte[3] = 1, 1
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        s.send((str(452) + "r").encode("utf-8"))
        time.sleep(2)
        s.send((str(450) + "r").encode("utf-8"))
        byte[2], byte[3] = 0, 0
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        time.sleep(1)
        byte[2], byte[3] = 1, 1
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        time.sleep(1)
        byte[2], byte[3] = 0, 0
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))  #byte[2] y byte[3] F, byte[4] y byte[5] T, byte[7] I, byte[6] D
    elif(selec == "Penny Hopkins"):                           
        s.send((str(401) + "r").encode("utf-8"))
        s.send((str(451) + "r").encode("utf-8")) 
        time.sleep(1)
        s.send((str(402) + "r").encode("utf-8"))
        time.sleep(1)
        s.send((str(401) + "r").encode("utf-8")) 
    elif(selec == "Marina Gibbs"):
        byte[2], byte[3] = 1, 1
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        s.send((str(451) + "r").encode("utf-8")) 
        time.sleep(2)
        s.send((str(450) + "r").encode("utf-8"))
        time.sleep(1)
        byte[2], byte[3] = 0, 0
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        time.sleep(1)
        byte[2], byte[3] = 1, 1
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        s.send((str(451) + "r").encode("utf-8")) 
        time.sleep(2)
        s.send((str(450) + "r").encode("utf-8"))
        time.sleep(1)
        byte[2], byte[3] = 0, 0
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        time.sleep(1)
        byte[2], byte[3] = 1, 1
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
    else:
        print("No llega name")


def puumAux(b,i,o,s):
    """Función que envía los datos de movimientos especiales y de luces
    Entradas: cuatro parámetros contadores y modificadores de lasseñales
    Salidas: el envio de las señales al NodeMCU
    Restricciones: Solo opera con los parámetros preasigados
    """
    if(len(b) >= i+1):
        num = b[s]
        build = (2**o)*num       
        return build +  puumAux(b,i+1,o+1,s-1)
    else:
        return 0


def test_drive(user_name, nacionalidad, auto_posc):
    """Función que inicializa la ventana de test drive
    Entradas: el nombre del piloto y la nacionalidad
    Salidas: el envío de los datos a puuumAux para ser enviados al NodeMCU
    Restricciones: Solo parrametros como cadenas
    """
    auto_posc=int(auto_posc)
    s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
    
    ## Text variables para las luces
    stateL = StringVar()
    stateL.set("OFF")
    stateE = StringVar()
    stateE.set("OFF")
    stateQ = StringVar()
    stateQ.set("OFF")
    stateF = StringVar()
    stateF.set("ON")

    ##Funciones de los eventos de las keys

    def funcW_Suelta(event):
        avanza(0)
    def funcW_Presiona(event):
        avanza(1)
    def avanza(num):
        global avanzar, vel
        if(num == 1 and avanzar == 0):
            stateF.set("OFF")
            btn_freno.configure(bg="#e74c3c")
            byte[4], byte[5] = 1, 1
            s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
            s.send((str(451) + "r").encode("utf-8"))
            cambiarlables(1)
            avanzar = 1
        elif(num == 0 and avanzar == 1):
            stateF.set("ON")
            btn_freno.configure(bg="#cf000f")
            s.send((str(450) + "r").encode("utf-8"))
            byte[4], byte[5] = 0, 0
            s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
            vel = 1
            avanzar = 0

    def funcA_Suelta(event):
        izquierda_gira(0)
    def funcA_Presiona(event):
        izquierda_gira(1)
    def izquierda_gira(num):
        global giraI
        if(num == 1 and giraI == 0):
            s.send((str(402) + "r").encode("utf-8"))
            giraI = 1
        elif(num == 0 and giraI == 1):
            s.send((str(400) + "r").encode("utf-8"))
            giraI = 0

    def funcS_Suelta(event):
        atrass(0)
    def funcS_Presiona(event):
        atrass(1) 
    def atrass(num):
        global retrocede, vel
        if(num == 1 and retrocede == 0):
            stateF.set("ON")
            btn_freno.configure(bg="#e74c3c")
            byte[4], byte[5] = 0, 0
            s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
            s.send((str(452) + "r").encode("utf-8"))
            cambiarlables(1)
            retrocede = 1
        elif(num == 0 and retrocede == 1):
            stateF.set("ON")
            btn_freno.configure(bg="#e74c3c")
            byte[4], byte[5] = 0, 0
            s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
            s.send((str(450) + "r").encode("utf-8"))
            vel = 1
            retrocede = 0
        
    def funcD_Suelta(event):
        derecha_gira(0)
    def funcD_Presiona(event):
        derecha_gira(1)
    def derecha_gira(num):
        global giraD
        if(num == 1 and giraD == 0):
            s.send((str(401) + "r").encode("utf-8"))
            giraD = 1
        elif(num == 0 and giraD == 1):
            s.send((str(400) + "r").encode("utf-8"))
            giraD = 0

    def retorna_movs():
        movs(5, None)

    def movE():
        print(user_name)
        movs(user_name, None)
       
    def llamafuncion(event):
        avanza(1)
    def cambiarlables(label):
        global vel
        if(vel == 0 and label == 1):
            vellbl1.configure(bg="green")
            vellbl2.configure(bg="white")
            vellbl3.configure(bg="white")
            vellbl4.configure(bg="white")
            pwm_label.configure(text = "PWM: 423")
            vellbl1.after(1000, lambda:cambiarlables(2))
        elif(vel == 0 and label == 2):
            pwm_label.configure(text = "PWM: 623")
            vellbl1.configure(bg="green")
            vellbl2.configure(bg="green")
            vellbl3.configure(bg="white")
            vellbl4.configure(bg="white")
            vellbl2.after(1000, lambda:cambiarlables(3))
        elif(vel == 0 and label == 3):
            pwm_label.configure(text = "PWM: 823")
            vellbl1.configure(bg="green")
            vellbl2.configure(bg="green")
            vellbl3.configure(bg="green")
            vellbl4.configure(bg="white")
            vellbl3.after(1000, lambda:cambiarlables(4))
        elif(vel == 0 and label == 4):
            pwm_label.configure(text = "PWM: 1023")
            vellbl1.configure(bg="green")
            vellbl2.configure(bg="green")
            vellbl3.configure(bg="green")
            vellbl4.configure(bg="green")
            vellbl3.after(50, lambda:cambiarlables(4))
        elif(vel==1):
            pwm_label.configure(text = "PWM: 0")
            vellbl1.configure(bg="white")
            vellbl2.configure(bg="white")
            vellbl3.configure(bg="white")
            vellbl4.configure(bg="white")
            vel = 0
            
    #Hace el mov especial y mide el rendimiento
    def rendimiento():
        batt_lvl1=battery()
        retorna_movs() #####
        batt_lvl2=battery()
        autos_txt=open("autos.txt", "r")
        sc3=autos_txt.readlines()
        autos_txt.close()
        rend=100-abs(int(batt_lvl1)-int(batt_lvl2))
        sc3[auto_posc*12+3]=str(rend)+'\n'
        autos_txt=open("autos.txt", "w")
        autos_txt.write("")
        autos_txt.close()
        autos_txt=open("autos.txt", "a")
        for b in sc3:
            autos_txt.write(b)
        autos_txt.close()
       
    def play():
        winsound.PlaySound("horn.wav", winsound.SND_ASYNC)


    def funcLuz(event):
        global contadorLuz
        contadorLuz=-contadorLuz
        if(contadorLuz == -1):
            stateL.set("OFF")
            btn_delanteras.configure(bg="#bdc3c7")
            return movs(4, 0)
        else:
            stateL.set("ON")
            btn_delanteras.configure(bg="#e8ecf1")
            return movs(4,1)

    #Solicita el estado de la bateria
    def battery():
        s.send("350r".encode("utf-8"))
        carga = s.recv(128)
        carga=str(carga, "utf-8")
        carga=int(carga)
        carga=carga-780
        carga=int((carga/140)*100)
        if(carga>=100):
            return "100"
        elif(carga<=0):
            return "0"
        else:
            return str(carga)

    #Destruye la ventana de test y reajusta los valores del auto en el texto
    def destroy_test():
        batt_lvl=battery()
        autos_txt=open("autos.txt", "r")
        sc3=autos_txt.readlines()
        autos_txt.close()
        sc3[auto_posc*12+8]=batt_lvl+'\n'
        if(batt_lvl=="0"):
            sc3[auto_posc*12+4]="Descargado\n"
        else:
            sc3[auto_posc*12+4]="Disponible\n"
        autos_txt=open("autos.txt", "w")
        autos_txt.write("")
        autos_txt.close()
        autos_txt=open("autos.txt", "a")
        for b in sc3:
            autos_txt.write(b)
        autos_txt.close()
        test_drive.destroy()
        
    #Muestra la ventana de test drive y sus configuraciones
    test_drive = Toplevel()
    test_drive.minsize(800, 600)
    test_drive.title("Test Drive!")
    test_drive.resizable(width=NO, height=NO)
    B_canvas=Canvas(test_drive, width = 800, height = 600, bg= "black")
    car4=cargarImg("pilotos_img2.gif")
    fondo=Label(test_drive, bg="black")
    bg_label = Label(test_drive)
    bg_label.place(x = 0, y =0)

    #Background Image de la test drive
    bg_image = cargarImg("noche.gif")
    bg_image2 = cargarImg("dia.gif")

    #### Botones de WASD de la ventana test drive:
    btn_arriba = Button(test_drive, text="W", bg="#2e3131", fg= "White", relief ="flat", width = 6, height = 3)
    test_drive.bind("<w>", llamafuncion)  ####
    test_drive.bind("<KeyRelease-w>", funcW_Suelta)
    btn_arriba.place(x=100, y=427)
    btn_izquierda = Button(test_drive, text="A", bg="#2e3131", fg= "White", relief ="flat", width = 6, height = 3)
    test_drive.bind("<a>", funcA_Presiona)
    test_drive.bind("<KeyRelease-a>", funcA_Suelta)
    btn_izquierda.place(x=45, y=485)
    btn_abajo = Button(test_drive, text="S", bg="#2e3131", fg= "White", relief ="flat", width = 6, height = 3)
    test_drive.bind("<s>", funcS_Presiona)
    test_drive.bind("<KeyRelease-s>", funcS_Suelta)
    test_drive.bind("<c>", funcLuz)    
    btn_abajo.place(x=100, y=485)
    btn_derecha = Button(test_drive, text="D", bg="#2e3131", fg= "White", relief ="flat", width = 6, height = 3)
    test_drive.bind("<d>", funcD_Presiona)
    test_drive.bind("<KeyRelease-d>", funcD_Suelta)    
    btn_derecha.place(x=155, y=485)

    ### Nombre, nacionalidad del piloto, label de la bateria, boton de cerrar, movimientos y pwm:
    name_label=Label(test_drive, text = user_name, bg="#2e3131", fg="White",width = 15, height = 2,anchor="e")
    name_label.place(x=670,y=20)
    name_label=Label(test_drive, text = nacionalidad, bg="#2e3131", fg="White",width = 15, height = 2, anchor="e")
    name_label.place(x=670,y=60)
    lvl_bat = battery() ## variable bateria que se envia de arduino 
    bat_lbl=Label(test_drive, text= lvl_bat, bg="#2e3131", fg="White",width = 11, height = 2,anchor="c", font = 18)
    bat_lbl.place(x=675,y=218)
    btn_cierra=Button(test_drive, text='X', command=destroy_test,bg='#d91e18',fg='white',relief ="flat", width = 3)  ### funcion para consultar y almacenar el nivel de batería del carro                                                                                                       
    btn_cierra.place(x=0,y=0)
    pilot_move=Button(test_drive, text='MOV. PILOTO', command= movE,bg='#e67e22',fg='black',relief ="flat",width = 13)                                                                                                        
    pilot_move.place(x=676,y=295)
    special_move=Button(test_drive, text='MOV. ESPECIAL', command= rendimiento,bg='#e67e22',fg='black',relief ="flat",width = 13)                                                                                                         
    special_move.place(x=676,y=265)
    piii=Button(test_drive, text='PIIII ', command= play,bg='#d91e18',fg='white',relief ="flat")                                                                                                         
    piii.place(x=35,y=0)
    pwm_label=Label(test_drive, text = ("PWM: 0"), bg="#2e3131", fg="White",width = 20, height = 2, anchor="e")
    pwm_label.place(x=601,y=440)  
 
    veltext = Label(test_drive, text = "VELOCIDAD:", bg="#2e3131", fg = "white", relief = "flat", width = 20)
    veltext.place(x = 601 ,y = 485)
    vellbl1 = Label(test_drive, bg = "white", relief = "flat", width = 5)
    vellbl2 = Label(test_drive, bg = "white", relief = "flat", width = 5) 
    vellbl3 = Label(test_drive, bg = "white", relief = "flat", width = 5)
    vellbl4 = Label(test_drive, bg = "white", relief = "flat", width = 5)
    vellbl1.place(x = 600-5, y=515)
    vellbl2.place(x = 641-5, y=515)
    vellbl3.place(x = 682-5, y=515)
    vellbl4.place(x = 723-5, y=515)

    ### funciones de encendido apagado de las luces direccionales (se puede enviar datos a arudino desde aca
    ### para controlarlas) ^^
    #Funcion luces direccionales izquierdas
    def funcQ(event):
        global blink_izq
        blink_izq=-blink_izq
        funcQ1()
    def funcQ1():
        global blink_izq
        if(blink_izq == 1):
            byte[7] = 0
            s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
            stateQ.set("ON")
            lbl_lucIzq.configure(bg="#f5e653")
            vellbl1.after(500, lambda:funcQ2())
    def funcQ2():
        byte[7] = 1
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        stateQ.set("OFF")
        lbl_lucIzq.configure(bg="#f0ff00")
        vellbl2.after(500, lambda:funcQ1())
    #Funcion luces direccionales derechas
    def funcE(event):
        global blink_der
        blink_der=-blink_der
        funcE1()
    def funcE1():
        global blink_der
        if(blink_der == 1):
            byte[6] = 0
            s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
            lbl_lucDer.configure(bg="#f5e653")
            stateE.set("ON")
            vellbl1.after(500, lambda:funcE2())
    def funcE2():
        byte[6] = 1
        s.send((str(puumAux(byte,0,0,-1)) + "r").encode("utf-8"))
        lbl_lucDer.configure(bg="#f0ff00")
        stateE.set("OFF")
        vellbl2.after(500, lambda:funcE1())
    
    ###Binds de Luces direccionales:

    btn_freno = Label(test_drive, textvariable = stateF, bg="#e74c3c", relief ="flat", width = 6, height = 3)
    btn_freno.place(x=675, y = 105)
    btn_delanteras = Label(test_drive, textvariable = stateL, bg= "#bdc3c7", relief ="flat", width = 6, height = 3)
    btn_delanteras.place(x=730, y = 105)
    lbl_lucIzq = Label(test_drive, textvariable = stateQ, bg="#f0ff00", relief ="flat", width = 6, height = 3)
    lbl_lucIzq.place(x=675, y = 160)
    test_drive.bind("<q>", funcQ)
    lbl_lucDer = Label(test_drive, textvariable = stateE, bg= "#f0ff00", relief ="flat", width = 6, height = 3)
    lbl_lucDer.place(x=730, y = 160)
    test_drive.bind("<e>", funcE)
    
    def sens_luz():
        s.send("300r".encode("utf-8"))
        luz_r = s.recv(128)
        luz_r=int.from_bytes(luz_r, byteorder='big')
        if(luz_r==1):
            bg_label.config(image=bg_image2)
        else:
            bg_label.config(image=bg_image)
        bg_label.after(2000, lambda:sens_luz())
    
    sens_luz()
    test_drive.mainloop()

docu1=cargarImg.__name__
docu_1=cargarImg.__doc__
print(docu1, ":")
print(docu_1)

docu2=main.__name__
docu_2=main.__doc__
print(docu2, ":")
print(docu_2)

docu3=cargarImg2.__name__
docu_3=cargarImg2.__doc__
print(docu3, ":")
print(docu_3)

docu4=cargarImg2.__name__
docu_4=cargarImg2.__doc__
print(docu4, ":")
print(docu_4)

docu5=tabla.__name__
docu_5=tabla.__doc__
print(docu5, ":")
print(docu_5)

docu6=clase_lista.__name__
docu_6=clase_lista.__doc__
print(docu6, ":")
print(docu_6)

docu7=main.__name__
docu_7=main.__doc__
print(docu7, ":")
print(docu_7)

docu8=principal.__name__
docu_8=principal.__doc__
print(docu8, ":")
print(docu_8)

docu9=movs.__name__
docu_9=movs.__doc__
print(docu9, ":")
print(docu_9)

docu10=puumAux.__name__
docu_10=puumAux.__doc__
print(docu10, ":")
print(docu_10)

docu11=test_drive.__name__
docu_11=test_drive.__doc__
print(docu11, ":")
print(docu_11) 
main()
