#include <WiFi.h>
#include <ESPAsyncWebServer.h>

// WiFi configuration
String wifi_ssid = "ESP32 Acces Point"; // Variable to store the user input SSID
String wifi_password = "pass"; // Variable to store the user input wifi_password
bool received_wifi_data = false;

// MQTT configuration
String mqtt_server = "Enter the MQTT Broker Address";
int mqtt_port = 1883;
String mqtt_username = "Enter the MQTT Username";
String mqtt_password = "Enter the MQTT Password";
String mqtt_topic = "Enter the MQTT Topic";

// Pins for voltage and current sensors
const int VOLTAGE_SENSOR_1_PIN = 2;
const int VOLTAGE_SENSOR_2_PIN = 3;
const int VOLTAGE_SENSOR_3_PIN = 4;
const int CURRENT_SENSOR_1_PIN = 5;
const int CURRENT_SENSOR_2_PIN = 6;
const int CURRENT_SENSOR_3_PIN = 7;

AsyncWebServer server(80); // Create an AsyncWebServer instance with port 80

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_AP);
  WiFi.softAP(wifi_ssid, wifi_password);

  Serial.println("ESP32 Access Point created");
  Serial.print("SSID: ");
  Serial.println(wifi_ssid);
  Serial.print("Password: ");
  Serial.println(wifi_password);

  IPAddress ip = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(ip);
  

  // Serve the web page for user input
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    String html = "<html><body>";
    html += "<h1>ESP32 Configuration</h1>";
    html += "<form method='post' action='/submit'>";
    html += "<label>WiFi SSID: <input type='text' name='ssid'></label><br>";
    html += "<label>WiFi Password: <input type='password' name='wifi_password'></label><br>";
    html += "<label>MQTT Server: <input type='text' name='mqtt_server'></label><br>";
    html += "<label>MQTT Port: <input type='number' name='mqtt_port'></label><br>";
    html += "<label>MQTT Username: <input type='text' name='mqtt_username'></label><br>";
    html += "<label>MQTT Password: <input type='password' name='mqtt_password'></label><br>";
    html += "<label>MQTT Topic: <input type='text' name='mqtt_topic'></label><br>";
    html += "<input type='submit' value='Save'>";
    html += "</form>";
    html += "</body></html>";
    request->send(200, "text/html", html);
    });

  // Handle form submission
  server.on("/submit", HTTP_POST, [](AsyncWebServerRequest *request){
    wifi_ssid = request->arg("wifi_ssid");
    wifi_password = request->arg("wifi_password");
    mqtt_server = request->arg("mqtt_server");
    mqtt_port = request->arg("mqtt_port").toInt();
    mqtt_username = request->arg("mqtt_username");
    mqtt_password = request->arg("mqtt_password");
    mqtt_topic = request->arg("mqtt_topic");

    // Setting flag to true
    received_wifi_data = true;

    // Send a response to the client
    request->send(200, "text/html", "Configuration submitted! You can close this tab now");
    });

  server.begin();
}

void loop() {
  // Attempt to connect to the WiFi network with user input
  if (received_wifi_data == true){
    Serial.print("WiFi SSID: ");
    Serial.println(wifi_ssid);
    Serial.print("WiFi Password: ");
    Serial.println(wifi_password);
    Serial.print("MQTT Server: ");
    Serial.println(mqtt_server);
    Serial.print("MQTT Port: ");
    Serial.println(mqtt_port);
    Serial.print("MQTT Username: ");
    Serial.println(mqtt_username);
    Serial.print("MQTT Password: ");
    Serial.println(mqtt_password);
    Serial.print("MQTT Topic: ");
    Serial.println(mqtt_topic);
    received_wifi_data = false;
  }
}
