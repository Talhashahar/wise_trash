// This #include statement was automatically added by the Particle IDE.
#include <HC_SR04.h>


///////TRYYYYY

// This #include statement was automatically added by the Particle IDE.
#include <HttpClient.h>

// This #include statement was automatically added by the Particle IDE.
#include <httpsclient-particle.h>

#include "application.h"
#include "HttpClient.h"

// This #include statement was automatically added by the Particle IDE.
#include "HC_SR04/HC_SR04.h"

double cm = 0.0;

int trigPin = A0;
int echoPin = D0;


HC_SR04 rangefinder = HC_SR04(trigPin, echoPin);






/**
* Declaring the variables.
*/
unsigned int nextTime = 0;    // Next time to contact the server
HttpClient http;

// Headers currently need to be set at init, useful for API keys etc.
http_header_t headers[] = {
    //  { "Content-Type", "application/json" },
    //  { "Accept" , "application/json" },
    { "Accept" , "*/*"},
    { NULL, NULL } // NOTE: Always terminate headers will NULL
};

http_request_t request;
http_response_t response;




void setup() {
    Serial.begin(9600);
    pinMode(D7, OUTPUT);
    Particle.variable("cm", &cm, DOUBLE);
}

void loop() {
    if (nextTime > millis()) {
        return;
    }


    cm = rangefinder.getDistanceCM();
    Serial.printf("Distance: %.2f cm\n", cm);
    //// Uncomment for extra experiment with Distance sensor
    //setRemoteServo(cm);
    blinkLed();
    




    Serial.println();
    Serial.println("Application>\tStart of Loop.");
    // Request path and body can be set at runtime or at setup.
    request.hostname = "34.253.231.214";
    request.port = 5000;
    request.path = "/update_sensor_by_id/1000_"+String(cm);

    // The library also supports sending a body with your request:
    //request.body = "{\"key\":\"value\"}";

    // Get request
    http.get(request, response, headers);
    Serial.print("Application>\tResponse status: ");
    Serial.println(response.status);

    Serial.print("Application>\tHTTP Response Body: ");
    Serial.println(response.body);

    nextTime = millis() + 1050;
}



void blinkLed() {
    digitalWrite(D7,HIGH);
    delay(150);   
    digitalWrite(D7,LOW);    
}

