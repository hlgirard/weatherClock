# weatherClock

Micropython project to indicate the current outside weather.

An ESP8266 development board (Wemos D1 mini) collects weather data from the openweathermap API and runs a decision tree to select relevant weather information: Ice, Snow, Rain, Cold, Warm, Sunny.  It then actuates a servomotor to indicate the weather on a clock face.
