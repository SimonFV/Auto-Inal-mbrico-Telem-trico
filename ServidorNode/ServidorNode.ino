#include <ESP8266WiFi.h>

char ssid[] = "Samsung";  //Nombre de la SSID 
char pass[] = "simonjfv";  //Contraseña
String data;  //String que almacena los char recibidos por el cliente concatenados
int data2;  //Entero que le indica al esp8266 que hacer

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
  shiftOut(12,15, MSBFIRST,255); 

  //IP estatica
  IPAddress ip(192,168,43,200);     
  IPAddress gateway(192,168,43,1);   
  IPAddress subnet(255,255,255,0);
  //Modo de conexion
  WiFi.mode(WIFI_STA);
  WiFi.config(ip, gateway, subnet);
  
  //Se intenta conectar al WiFi y espera hasta que ocurra
  //Serial.printf("Conectandose a %s ", ssid);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    //Serial.print(".");
  }
  shiftOut(12,15, MSBFIRST,63);
  //Serial.println("Conectado!");
  //Serial.print("IP: ");
  //Serial.println(WiFi.localIP());

  //Inicializa el servidor
  server.begin();
}

void loop() {
  if(WiFi.status() != WL_CONNECTED){
    shiftOut(12,15, MSBFIRST,255);
  }
  WiFiClient client = server.available();
  //Espera a que se conecte un cliente
  if (client){
    //Serial.println("\n[Cliente conectado]");
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
          client.write(LUZ); //Devuelve el valor de luz ambiente
        }else if(data2==350){
          int CARGA = analogRead(A0);
          data = String(CARGA);
          char data3[5];
          data.toCharArray(data3, 5);
          Serial.println(data3);
          client.write(data3); //Devuelve la carga de bateria
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
          digitalWrite(5, HIGH);   //Derecha
          digitalWrite(16, LOW);
          analogWrite(14, 1023);
        }else if(data2==402){
          digitalWrite(5, LOW);   //Izquierda
          digitalWrite(16, HIGH);
          analogWrite(14, 1023);
        }else if(data2==400){
          digitalWrite(5, LOW);   //Centrado
          digitalWrite(16, LOW);
          analogWrite(14, 0);
        }else if(data2==360){  //CIRCULO DERECHA
          digitalWrite(0, LOW);   //Se impulsa
          digitalWrite(4, HIGH);
          analogWrite(2, 1023);
          delay(500);
          analogWrite(2, 0);
          digitalWrite(5, LOW);   //Gira izquierda levemente
          digitalWrite(16, HIGH);
          analogWrite(14, 1023);
          delay(200);
          digitalWrite(16, LOW);
          digitalWrite(5, HIGH);   //Gira derecha
          analogWrite(2, 1023);   //Acelera
          delay(8000);
          analogWrite(2, 0);   //Se detiene
          analogWrite(14, 0);
        }else if(data2==365){  //CIRCULO IZQUIERDA
          digitalWrite(0, LOW);   //Se impulsa
          digitalWrite(4, HIGH);
          analogWrite(2, 1023);
          delay(500);
          analogWrite(2, 0);
          digitalWrite(5, HIGH);   //Gira derecha levemente
          digitalWrite(16, LOW);
          analogWrite(14, 1023);  
          delay(250);
          digitalWrite(5, LOW);   //Gira izquierda
          digitalWrite(16, HIGH);
          analogWrite(2, 1023);   //Acelera
          delay(8000);
          analogWrite(2, 0);   //Se detiene
          analogWrite(14, 0);
        }else if(data2==370){  //CIRCULO INFINITO u OCHO
          digitalWrite(0, LOW);   //Se impulsa
          digitalWrite(4, HIGH);
          analogWrite(2, 1023);
          delay(500);
          analogWrite(2, 0);
          digitalWrite(5, LOW);   //Gira izquierda levemente
          digitalWrite(16, HIGH);
          analogWrite(14, 1023);
          delay(250);
          digitalWrite(16, LOW);
          digitalWrite(5, HIGH);   //Gira derecha medio circulo
          analogWrite(2, 1023);  //Acelera
          delay(4000);
          digitalWrite(5, LOW);   //Gira izquierda un circulo
          digitalWrite(16, HIGH);
          delay(8000);
          digitalWrite(16, LOW);
          digitalWrite(5, HIGH);   //Gira derecha medio circulo
          delay(4000);
          analogWrite(2, 0);   //Se detiene
          analogWrite(14, 0);
      }else if(data2==380){  //ZIG ZAG
          digitalWrite(0, LOW);   //Se impulsa
          digitalWrite(4, HIGH);
          analogWrite(2, 1023);
          delay(500);
          analogWrite(2, 0);
          digitalWrite(5, HIGH);   //Gira derecha levemente
          digitalWrite(16, LOW);
          analogWrite(14, 1023);
          delay(250);
          digitalWrite(5, LOW);   //Gira izquierda semi-circulo
          digitalWrite(16, HIGH);
          analogWrite(2, 1023);  //Acelera
          delay(1000);
          digitalWrite(16, LOW);
          digitalWrite(5, HIGH);   //Gira derecha medio circulo
          delay(2000);
          digitalWrite(5, LOW);   //Gira izquierda medio circulo
          digitalWrite(16, HIGH);
          delay(2000);
          digitalWrite(16, LOW);
          digitalWrite(5, HIGH);   //Gira derecha medio circulo
          delay(2000);
          digitalWrite(5, LOW);   //Gira izquierda semi-circulo
          digitalWrite(16, HIGH);
          delay(1000);
          analogWrite(2, 0);   //Se detiene
          analogWrite(14, 0);
      }else if(data2==390){  //ESPECIAL
          digitalWrite(0, HIGH);   //Se impulsa hacia atras
          digitalWrite(4, LOW);
          analogWrite(2, 1023);
          delay(500);
          analogWrite(2, 0);
          digitalWrite(5, HIGH);   //Gira derecha levemente
          digitalWrite(16, LOW);
          analogWrite(14, 1023);
          delay(250);
          digitalWrite(5, LOW);   //Gira izquierda
          digitalWrite(16, HIGH);
          analogWrite(2, 1023);  //Acelera en reversa
          delay(2000);
          analogWrite(2, 0);   //Se detiene
          analogWrite(14, 0);
          delay(1000);
          digitalWrite(0, LOW);   //Direccion hacia adelante
          digitalWrite(4, HIGH);
          analogWrite(2, 1023);  //Acelera
          delay(4000);
          analogWrite(2, 0);   //Se detiene
          delay(1000);
          digitalWrite(4, LOW);
          digitalWrite(0, HIGH);   //Direccion hacia atras
          analogWrite(2, 1023);  //Acelera en reversa
          delay(4000);
          analogWrite(2, 0);   //Se detiene
          delay(1000);
          digitalWrite(0, LOW);   //Se impulsa
          digitalWrite(4, HIGH);
          analogWrite(2, 1023);
          delay(500);
          analogWrite(2, 0);
          digitalWrite(5, HIGH);   //Gira derecha levemente
          digitalWrite(16, LOW);
          analogWrite(14, 1023);
          delay(250);
          digitalWrite(5, LOW);   //Gira izquierda
          digitalWrite(16, HIGH);
          analogWrite(2, 1023);  //Acelera
          delay(2000);
          analogWrite(2, 0);
          analogWrite(14, 0);
      }
      }
      data = "";
      delay(10);
    }

    //Cierra la conexion cuando el cliente se desconecta
    client.stop();
    //Serial.println("[Cliente desconectado]");
  }
}
