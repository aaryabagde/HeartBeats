
#include <WiFi.h>
#include "ThingSpeak.h"
/*#include <Adafruit_BME280.h>
#include <Adafruit_Sensor.h>*/

const char* ssid = "SANJAY";   // your network SSID (name) 
const char* password = "9820404475";   // your network password

WiFiClient  client;

unsigned long myChannelNumber = 2095762;
const char * myWriteAPIKey = "LAEFG42PGX2RB623";
 
// Timer variables
unsigned long lastTime = 0;
unsigned long timerDelay = 500;

// Variable to hold temperature readings
float sensor;
#define SENSOR A0 // Set the A0 as SENSOR

char payload[100];
char topic[150];
// Space to store values to send
char str_sensor[10];

//uncomment if you want to get temperature in Fahrenheit
//float temperatureF;

// Create a sensor object Adafruit_BME280 bme; //BME280 connect to ESP32 I2C (GPIO 21 = SDA, GPIO 22 = SCL)


void setup() {
  Serial.begin(115200);  //Initialize serial
  WiFi.mode(WIFI_STA);   
  pinMode(SENSOR, INPUT);
  ThingSpeak.begin(client);  // Initialize ThingSpeak
}

void loop() {
  if ((millis() - lastTime) > timerDelay) {
    
    // Connect or reconnect to WiFi
    if(WiFi.status() != WL_CONNECTED){
      Serial.print("Attempting to connect");
      while(WiFi.status() != WL_CONNECTED){
        WiFi.begin(ssid, password); 
        delay(5000);     
      } 
      Serial.println("\nConnected.");
    }

    // Get a new temperature reading
    float sensor = analogRead(SENSOR); 
    Serial.print("ECG: ");
    Serial.println(SENSOR);
    
    //uncomment if you want to get temperature in Fahrenheit
    /*temperatureF = 1.8 * bme.readTemperature() + 32;
    Serial.print("Temperature (ºC): ");
    Serial.println(temperatureF);*/
    
    
    // Write to ThingSpeak. There are up to 8 fields in a channel, allowing you to store up to 8 different
    // pieces of information in a channel.  Here, we write to field 1.
    int x = ThingSpeak.writeField(myChannelNumber, 1,sensor, myWriteAPIKey);
    //uncomment if you want to get temperature in Fahrenheit
    //int x = ThingSpeak.writeField(myChannelNumber, 1, temperatureF, myWriteAPIKey);

    if(x == 200){
      Serial.println("Channel update successful.");
    }
    else{
      Serial.println("Problem updating channel. HTTP error code " + String(x));
    }
    lastTime = millis();
  }
}
