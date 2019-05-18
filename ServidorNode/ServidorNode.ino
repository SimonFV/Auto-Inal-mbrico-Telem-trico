#include <ESP8266WiFi.h>

char ssid[] = "Familia Munoz";  //Nombre de la SSID 
char pass[] = "patipamipatu";  //Contraseña
String data;  //String que almacena los char recibidos por el cliente concatenados
int data2;

//Se crea el servidor TCP con su respectivo puerto
WiFiServer server(7070);

void setup() {
  pinMode(13, INPUT);
  pinMode(12, OUTPUT);
  pinMode(15, OUTPUT);
  Serial.begin(9600);

  //Se intenta conectar al WiFi y espera hasta que ocurra
  Serial.printf("Conectandose a %s ", ssid);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED)
  {
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
      //Se realizan las acciones dependiendo de la peticion del cliente
      if(data!=""){
        data2=data.toInt();
        shiftOut(12,15, MSBFIRST,data2);
        int LUZ = digitalRead(13);
        Serial.println(LUZ);
      }
      data = "";
      delay(10);
    }

    //Cierra la conexion cuando el cliente se desconecta
    client.stop();
    Serial.println("[Cliente desconectado]");
  }
}
