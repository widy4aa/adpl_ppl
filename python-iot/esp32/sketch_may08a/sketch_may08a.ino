#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "time.h"

// WiFi Credentials
const char* ssid = "widy4aa";
const char* password = "12345678";

// MQTT Configuration
const char* mqtt_broker = "broker.emqx.io";
const int mqtt_port = 1883;
const char* device_id = "Esp-Widya";

// Topics
const char* topic_control = "maggot/device/control";
const char* topic_device_info = "maggot/device/info";
const char* topic_sensor_info = "maggot/sensor/info";
const char* topic_timestamp = "maggot/timestamp";

// Device Status
struct {
  String fan = "off";
  String water = "off";
  String lamp = "off";
  String mode = "manual";
} device_status;

WiFiClient espClient;
PubSubClient client(espClient);

// NTP Server for timestamp
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 7 * 3600; // GMT+7
const int   daylightOffset_sec = 0;

void setup_wifi() {
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

String getCurrentTimestamp() {
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return "0000-00-00 00:00:00";
  }
  
  char timeString[20];
  strftime(timeString, sizeof(timeString), "%Y-%m-%d %H:%M:%S", &timeinfo);
  return String(timeString);
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Parse JSON
  DynamicJsonDocument doc(1024);
  deserializeJson(doc, payload, length);

  // Update device status
  if (doc.containsKey("device_status")) {
    JsonObject status = doc["device_status"];
    
    if (status.containsKey("fan") && (status["fan"] == "on" || status["fan"] == "off")) {
      device_status.fan = status["fan"].as<String>();
    }
    if (status.containsKey("water") && (status["water"] == "on" || status["water"] == "off")) {
      device_status.water = status["water"].as<String>();
    }
    if (status.containsKey("lamp") && (status["lamp"] == "on" || status["lamp"] == "off")) {
      device_status.lamp = status["lamp"].as<String>();
    }
    if (status.containsKey("mode") && (status["mode"] == "auto" || status["mode"] == "manual")) {
      device_status.mode = status["mode"].as<String>();
    }
    
    Serial.println("Updated device status:");
    Serial.print("Fan: "); Serial.println(device_status.fan);
    Serial.print("Water: "); Serial.println(device_status.water);
    Serial.print("Lamp: "); Serial.println(device_status.lamp);
    Serial.print("Mode: "); Serial.println(device_status.mode);
    
    publish_device_info();
  }
}

void publish_device_info() {
  DynamicJsonDocument doc(256);
  doc["device_id"] = device_id;
  doc["timestamp"] = getCurrentTimestamp();
  
  JsonObject status = doc.createNestedObject("device_status");
  status["fan"] = device_status.fan;
  status["water"] = device_status.water;
  status["lamp"] = device_status.lamp;
  status["mode"] = device_status.mode;

  String output;
  serializeJson(doc, output);
  
  client.publish(topic_device_info, output.c_str());
  Serial.println("Published device info:");
  Serial.println(output);
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(device_id)) {
      Serial.println("connected");
      client.subscribe(topic_control);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  
  // Init and get the time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  
  // Initial connection
  if (client.connect(device_id)) {
    client.subscribe(topic_control);
    publish_device_info();
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Generate random sensor data
  DynamicJsonDocument sensorDoc(256);
  sensorDoc["device_id"] = device_id;
  sensorDoc["timestamp"] = getCurrentTimestamp();
  
  JsonObject sensor = sensorDoc.createNestedObject("sensor");
  sensor["suhu_udara"] = random(200, 400) / 10.0;
  sensor["kelembapan_udara"] = random(30, 90);
  sensor["suhu_tanah"] = random(180, 350) / 10.0;
  sensor["kelembapan_tanah"] = random(20, 80);

  String sensorOutput;
  serializeJson(sensorDoc, sensorOutput);
  
  client.publish(topic_sensor_info, sensorOutput.c_str());
  Serial.println("Published sensor data:");
  Serial.println(sensorOutput);

  // Publish timestamp separately
  DynamicJsonDocument timeDoc(100);
  timeDoc["device_id"] = device_id;
  timeDoc["timestamp"] = getCurrentTimestamp();
  
  String timeOutput;
  serializeJson(timeDoc, timeOutput);
  client.publish(topic_timestamp, timeOutput.c_str());

  delay(2000); // Wait 2 seconds
}
