#include <OneWire.h>                
#include <DallasTemperature.h>

OneWire ourWire2(2);                // Pin 3 como bus OneWire para termocupla 2

DallasTemperature sensors2(&ourWire2); // Objeto para sensor 2


void setup() {
  delay(1000);
  Serial.begin(9600);
  sensors2.begin();   // Inicia sensor 2
}
 
void loop() { 
  sensors2.requestTemperatures();
  float temp2 = sensors2.getTempCByIndex(0);
  
  Serial.print(temp2);
  Serial.println();  // Mejor que "\n" para consistencia
  
  delay(2000);
}
