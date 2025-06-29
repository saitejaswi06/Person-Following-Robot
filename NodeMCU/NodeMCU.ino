#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

// Wi-Fi credentials
const char* ssid = "SSID";
const char* password = "PASSWORD";

WiFiServer server(80);

// Motor control pins (L293D)
const int EN1 = D5;          // Enable for Motor A
const int motorA_in1 = D1;   // IN1 for Motor A
const int motorA_in2 = D2;   // IN2 for Motor A

const int EN2 = D6;          // Enable for Motor B
const int motorB_in3 = D3;   // IN3 for Motor B
const int motorB_in4 = D4;   // IN4 for Motor B

void motorL(int speed){
    if (speed > 0){
        digitalWrite(motorA_in1, HIGH);
        digitalWrite(motorA_in2, LOW);
    }
    else if (speed < 0){
        digitalWrite(motorA_in1, LOW);
        digitalWrite(motorA_in2, HIGH);
    }
    else {
        digitalWrite(motorA_in1, LOW);
        digitalWrite(motorA_in2, LOW);
    }
    analogWrite(EN1, abs(speed));
}

void motorR(int speed){
    if (speed > 0){
        digitalWrite(motorB_in3, HIGH);
        digitalWrite(motorB_in4, LOW);
    }
    else if (speed < 0){
        digitalWrite(motorB_in3, LOW);
        digitalWrite(motorB_in4, HIGH);
    }
    else {
        digitalWrite(motorB_in3, LOW);
        digitalWrite(motorB_in4, LOW);
    }
    analogWrite(EN2, abs(speed));
}

void setup() {
  Serial.begin(9600);

  // Initialize motor control pins as OUTPUT
  pinMode(EN1, OUTPUT);
  pinMode(motorA_in1, OUTPUT);
  pinMode(motorA_in2, OUTPUT);

  pinMode(EN2, OUTPUT);
  pinMode(motorB_in3, OUTPUT);
  pinMode(motorB_in4, OUTPUT);
 
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to Wi-Fi...");
  }

  Serial.print("Connected to Wi-Fi. IP Address: ");
  Serial.println(WiFi.localIP());

  // Start the server
  server.begin();
  Serial.println("Server started");
}


void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("Client connected");
    while (client.connected()) {
      if (client.available()) {
        String jsonString = client.readStringUntil('\n');
        jsonString.trim();

        DynamicJsonDocument doc(200);

        DeserializationError error = deserializeJson(doc, jsonString);
        if (error) {
          Serial.println("parseObject() failed");
        } else {
          int pwmL = doc["pwmL"];
          int pwmR = doc["pwmR"];
          Serial.printf("\n L - %d , R - %d\n", pwmL, pwmR); 
          motorL(pwmL);
          motorR(pwmR);
        }
      }
    }
  }    
}
