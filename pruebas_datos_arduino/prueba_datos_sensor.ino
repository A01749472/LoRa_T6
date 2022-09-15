#include <LoRa.h>
#include "boards.h"
float Temperatura;
float Humedad;
float CO2;   

void setup()
{
    Serial.begin(115200);
    initBoard();
    // When the power is turned on, a delay is required.
    delay(1500);

    Serial.println("LoRa Sender");
    LoRa.setPins(RADIO_CS_PIN, RADIO_RST_PIN, RADIO_DI0_PIN);
    if (!LoRa.begin(LoRa_frequency)) {
        Serial.println("Starting LoRa failed!");
        while (1);
    }
    Serial.setTimeout(1);

}

void loop()
{ 
    while (!Serial.available());
    Temperatura = Serial.readString().toFloat();
    Humedad = Serial.readString().toFloat();
    CO2 = Serial.readString().toFloat();
    delay(1000); // Wait for 10 seconds 
    Serial.print("Sending packet: ");
    // send packet
    LoRa.beginPacket();
    LoRa.print("Temperatura es: ");
    LoRa.print(Temperatura);
    LoRa.endPacket();

#ifdef HAS_DISPLAY
    if (u8g2) {
        char buf[256];
        u8g2->clearBuffer();
        u8g2->drawStr(0, 12, "Transmitting: OK!");
        snprintf(buf, sizeof(buf), "Sending: %d", Temperatura);
        u8g2->drawStr(0, 30, buf);
        u8g2->sendBuffer();
    }
#endif
    delay(5000); 
}
