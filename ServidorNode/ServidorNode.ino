#include <ESP8266WiFi.h>

char ssid[] = "Samsung";  //Nombre de la SSID 
char pass[] = "simonjfv";  //Contraseña
String data;  //String que almacena los char recibidos por el cliente concatenados
int data2;

//Se crea el servidor TCP con su respectivo puerto
WiFiServer server(7070);

void setup(){
  Serial.begin(9600);

  analogWriteFreq(120); //Cambia la frecuencia de PWM

  //Pines para controlar los motores
  pinMode(0, OUTPUT); //Direccion: adelante/atras In-1
  pinMode(4, OUTPUT); //In-2
  pinMode(2, OUTPUT); //PWM, Enb-A
  pinMode(5, OUTPUT); //Direccion: izquierda/derecha In-3
  pinMode(16, OUTPUT); //In-4
  pinMode(14, OUTPUT); //PWM, Enb-B
  //Pin de la fotoresistencia
  pinMode(13, INPUT);
  //Pines para el registro de corrimiento
  pinMode(12, OUTPUT);
  pinMode(15, OUTPUT); 

  //IP estatica
  IPAddress ip(192,168,43,200);     
  IPAddress gateway(192,168,43,1);   
  IPAddress subnet(255,255,255,0);
  //Modo de conexion
  WiFi.mode(WIFI_STA);
  WiFi.config(ip, gateway, subnet);
  
  //Se intenta conectar al WiFi y espera hasta que ocurra
  Serial.printf("Conectandose a %s ", ssid);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println("Conectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  //Inicializa el servidor
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  //Espera a que se conecte un cliente
  if (client){
    Serial.println("\n[Cliente conectado]");
    //Las acciones que se realizan mientras haya un cliente conectado
    while (client.connected()){
      //Lee los datos recibidos del cliente
      while(client.available()>0){
        char c = client.read();
        data += c;
      }
      if(data!=""){
        data2=data.toInt(); //Convierte el dato a int para procesarlo
     
        //Se realizan las acciones dependiendo de la peticion del cliente
        if(data2<256){
          shiftOut(12,15, MSBFIRST,data2); //Enciende los LEDs
        }else if(data2==300){
          int LUZ = digitalRead(13);
          Serial.println(LUZ);
          //client.write(LUZ); //Devuelve el valor de luz ambiente
        }else if(data2==350){
          int CARGA = analogRead(A0);
          Serial.println(CARGA);
          //client.write(CARGA); //Devuelve la carga de bateria
        }else if(data2>1423){
          data2=data2-1000;
          digitalWrite(0, HIGH);  //Se mueve haia atras
          digitalWrite(4, LOW);
          analogWrite(2, data2);
        }else if(data2>423){;
          digitalWrite(0, LOW);   //Se mueve hacia adelante
          digitalWrite(4, HIGH);
          analogWrite(2, data2);
        }else if(data2==423){
          digitalWrite(0, LOW);   //Se detiene
          digitalWrite(4, LOW);
          analogWrite(2, 0);
        }else if(data2==401){
          digitalWrite(5, HIGH);   //Izquierda
          digitalWrite(16, LOW);
          analogWrite(14, 1023);
        }else if(data2==402){
          digitalWrite(5, LOW);   //Derecha
          digitalWrite(16, HIGH);
          analogWrite(14, 1023);
        }else if(data2==400){
          digitalWrite(5, LOW);   //Centrado
          digitalWrite(16, LOW);
          analogWrite(14, 0);
        }
      }
      data = "";
      delay(10);
    }

    //Cierra la conexion cuando el cliente se desconecta
    client.stop();
    Serial.println("[Cliente desconectado]");
  }
}
