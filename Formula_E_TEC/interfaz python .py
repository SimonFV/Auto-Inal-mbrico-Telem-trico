docu = """INSTITUTO TECNOLÓGICO DE COSTA RICA.
CURSO DE TALLER DE PROGRAMACIÓN
TERCER PROYECTO PROGRAMADO: FÓRMULA E CE
PROFESOR: Msc. PEDRO GUITIERREZ
ESTUDIANTES: MARCO PICADO 2018310184
SIMÓN FALLAS 2019324313
BRANDON
PRIMER SEMESTRE 2019
FECHA DE ENTREGA 18 DE JUNIO DE 2019
FECHA DE EMISIÓN: 03 DE JUNIO DE 2019
FECHA DE ÚLTIMA MODIFICACIÓN: 
VERSIÓN 0.1.4"""


####################################Bibliotecas necesarias####################
from tkinter import *
import os
import time




###########cargando la imagen, TOMADA DE TURORIA TK#############################
def cargarImg(nombre):
    """Recibe una imagen que carga desde la ruta especificada
       Entradas: Nombre de la imagen que se quiera cargar
       Salidas: imagen que se cargó
       Restricciones: solo recibe un nombre dado desde otra función.
       """
    ruta=os.path.join('imag',nombre)
    imagen=PhotoImage(file=ruta)
    return imagen



######### Crea la tabla de posiciones de pilotos y autos #########
def tabla():
    ventana_lista=Toplevel()
    objeto_lista=clase_lista(ventana_lista)
    
class clase_lista():
    def __init__(self, master):
        #Conf de la ventana
        ve=master
        ve.title("Tabla de posiciones de pilotos y autos")
        ve.minsize(800,600)
        ve.resizable(width=NO, height=NO)

        #Titulos de la tabla
        
        
        self.score=open("Puntuaciones.txt", "r")
        self.sc=self.score.readlines()
        self.construir_tabla(0)
        self.score.close()
    def construir_tabla(self,b):
        if(b<19):
            Label(self.gr3, text=self.sc[b][:-1]).grid(pady=2, padx=2, row=b+1, column=0, sticky=(N, S, E, W))
            Label(self.gr3, text=self.sc[b+1][:-1], bd=2, relief="ridge").grid(pady=2, padx=2, row=b+1, column=1, sticky=(N, S, E, W))
            self.construir_tabla(b+2)



def ventana_about():
    """Función que crea la ventana de about
    Entradas: no tiene argumentos pero recibe la orden desde el botón de pantalla principal
    Salidas: ventana de about
    Restricciones: solo ejecuta la ventana about
    """
    about=Toplevel()
    about.title('Acerca de este software:')
    about.minsize(800,600)
    about.resizable(width=NO, height=NO)
    
    C_about=Canvas(about, width=800,height=600,bg='light green')
    C_about.place(x=0,y=0)
    E_about=Label(about,text=docu,font=('Agency FB',20)).place(x=115,y=30)

    #foto=cargarImg('mi_foto.gif')
    #F_about=Label(about, image=foto,bg='light blue')
    #F_about.photo=foto
    #F_about.place(x=550,y=0)

    btn_atras=Button(about, text="ATRAS", command=about.destroy,fg='green',bg='white')
    btn_atras.place(x=10,y=560)




root = Tk()
root.title("Tercer proyecto Marco, Simón y Brandon. 2019")
root.minsize(800, 600)
root.resizable(width=NO, height=NO)

C_root=Canvas(root, width = 800, height = 600, bg= "white")

#####imagen de pantalla principal####################
carg=cargarImg("formula e.gif")#extraida de: https://www.kienyke.com/deportes/mas-deportes/disenos-carros-de-formula-1-en-el-mundial-de-rusia
imag_prin=Label(root, bg='white')
imag_prin.place(x=0,y=0)
imag_prin.config(image=carg)


##botones de la ventana principal:

boton_juego = Button(root, text='TABLA', command=tabla,fg='yellow',bg='blue')
boton_juego.place(x=370,y=520)
boton_about= Button(root,text='ABOUT:',command=ventana_about,bg='blue',fg='yellow')
boton_about.place(x=620,y=520)
boton_cerrar=Button(root, text='CERRAR', command=root.destroy,bg='blue',fg='yellow')
boton_cerrar.place(x=100,y=520)

#entry de ventana principal:
#etiqueta_nombre= Label(ventana,text="Ingresa tu nombre:",font=('helvetica',14),fg='light yellow', bg="grey")
#etiqueta_nombre.place(x=560,y=49)
#caja_nombre= Entry(ventana,width=20,font=('helvetica',14))
#caja_nombre.place(x=560,y=75)
L_titulo=Label(root, text="CLASSIC \n FORMULA \n E", font=("Agency FB",30), bg="grey",fg="light yellow").place(x=10,y=10)
