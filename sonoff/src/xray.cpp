#include <Arduino.h>
#include <ArduinoOTA.h>
#include "ConnectionManager.h"
#include "Relay.h"
#include "Button.h"
#include "ESPLed.h"
#include "MqttTopic.h"

#define HOSTNAME  "SONOFF"
#define SERVER    "192.168.1.248"
#define PORT      1883

struct Pinmap {
  gpio_num_t b;
  gpio_num_t l;
  gpio_num_t r;
};

// Nodemcu
//Pinmap nodemcu = {0,2,16};

// Sonoff / SV
Pinmap p = {0, 13, 12};

Button b(p.b);
Led led(p.l, INVERTED);
Relay r(p.r);

bool needs_reset = false;

void cm_setup() {

  ConnectionManager::parameter("hostname", "hostname", 30);
  ConnectionManager::parameter("mqtt_server", "mqtt_server", 30);
  ConnectionManager::parameter("trigger_delay", "trigger_delay");

  // /command, /state, and /exposure
  ConnectionManager::parameter("topic", "topic");

  ConnectionManager::onConnect([]() {
    Serial.println("Connected!");
    led.stop().off();
  });

  // If a hostname cant be found, create one from chip ID for use as AP SSID
  std::string ap = ConnectionManager::parameter("hostname");
  if(ap.empty()) ap = "Sonoff-" + ESP.getChipId();
  ConnectionManager::autoConnect(ap.c_str());

  // Check again if hostname has been set
  // If not, create one so that the ESP will have a hostname
  std::string host = ConnectionManager::parameter("hostname");
  if(host.empty()) host = ap;
  Serial.print("Hostname: "); Serial.println(host.c_str());
  ArduinoOTA.setHostname(host.c_str());

}


void setup() {
  Serial.begin(115200); Serial.println("\r\n\r\n");

  r.off();

  led.setPeriod(3000);
  led.pulse().start();

  b.holdCallback([]() {
    ConnectionManager::erase();
    needs_reset = true;
  });

  cm_setup();

  ArduinoOTA.setPassword("bangels1");
  ArduinoOTA.onStart([](){
    led.setDuration(50).setInterval(200);
    led.blink().start();
  });
  ArduinoOTA.begin();



  std::string topic = ConnectionManager::parameter("topic");
  std::string st = topic + "/state";
  std::string ct = topic + "/command";
  std::string et = topic + "/exposure";

  static MqttTopic state(st.c_str());
  static MqttTopic command(ct.c_str());
  static MqttTopic exposure(et.c_str());

  command.callback("ON", []() {
      Serial.println("ON");
      r.on();
      light_state.publish("ON");
  });
  command.callback("OFF", []() {
      Serial.println("OFF");
      r.off();
      light_state.publish("OFF");
  });
  exposure.callback("", []() {
      Serial.println("OFF");
      r.off();
      light_state.publish("OFF");
  });

  std::string server = ConnectionManager::parameter("mqtt_server");
  Serial.print("Server: "); Serial.println(server.c_str());
  MqttTopic::setServer(server.c_str(), 1883);

  MqttTopic::onConnect([]() {
    Serial.println("Connected MQTT");
  });


  b.pressCallback([]() {
    r.toggle();
    light_state.publish(r.isOn() ? "ON" : "OFF");
  });


  configTime(5 * 3600, 0, "pool.ntp.org", "time.nist.gov"); // GMT+5 = central
}

void loop() {
  ArduinoOTA.handle();
  MqttTopic::loop();
  if(needs_reset) ESP.reset();
}
