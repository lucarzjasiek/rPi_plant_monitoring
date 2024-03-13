#potrzebne biblioteki
import machine, time
from ds18x20 import DS18X20
from onewire import OneWire

#zadeklarowanie wejścia sygnałowego
temperature = machine.Pin(22)

#wczytanie czujnika
sensor = DS18X20(OneWire(temperature))

#skanowanie w celu poszukiwania czujnika
datas = sensor.scan()

#funkcja wyświetlająca temperaturę
def PrintTemp(sensor, datas):
    sensor.convert_temp()
 
    time.sleep_ms(750)
 
    for data in datas:
 
      print(sensor.read_temp(data))

#pętla programowa wykonująca zadanie
while True:
 
  PrintTemp(sensor,datas)
 
  time.sleep(1)

  