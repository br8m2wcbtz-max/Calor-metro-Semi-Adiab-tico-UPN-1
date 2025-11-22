#include <DHT.h>
#include <OneWire.h>                
#include <DallasTemperature.h>
 
OneWire ourWire1(2);                // Pin 2 como bus OneWire para termocupla 1
OneWire ourWire2(2);                // Pin 3 como bus OneWire para termocupla 2
#define DHTPIN 4
#define DHTTYPE DHT22               // ¡Corregido! Especificar DHT22
 
DallasTemperature sensors1(&ourWire1); // Objeto para sensor 1
DallasTemperature sensors2(&ourWire2); // Objeto para sensor 2
DHT dht(DHTPIN, DHTTYPE);           // Objeto para sensor DHT22

void setup() {
  delay(1000);
  Serial.begin(9600);
  sensors1.begin();   // Inicia sensor 1
  sensors2.begin();   // Inicia sensor 2
  dht.begin();
}
 
void loop() {
  // Leer termocuplas
  sensors1.requestTemperatures();
  float temp1 = sensors1.getTempCByIndex(0);
  
  sensors2.requestTemperatures();
  float temp2 = sensors2.getTempCByIndex(0);
  
  Leer DHT22 (con verificación de errores)
  float h = dht.readHumidity();
  float t = dht.readTemperature();  //
  
  // Verificar si las lecturas son válidas
  if (isnan(h) || isnan(t)) {
       Serial.println("Error leyendo el sensor DHT!");
       h = -1;
      t = -1;
  }
  
  // Imprimir datos
  Serial.print(temp1);
  Serial.print(", ");
  
  Serial.print(temp2);
  Serial.print(", ");
  
  Serial.print(h);
  Serial.print(", ");
  
  Serial.print(t);
  Serial.println();  // Mejor que "\n" para consistencia
  
  delay(2000);  // Aumenté el delay para DHT22 (necesita al menos 2s entre lecturas)                    
}
