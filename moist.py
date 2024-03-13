#potrzebne biblioteki
import time, machine

# inicjalizacja czujnika ADC
mvalue = machine.ADC(machine.Pin(27))

#funkcja kalibrująca odczyt higrometru.
def cal(raw_value, in_min, in_max, out_min, out_max):
    return int((raw_value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

#funkcja  przetwarzająca sygnał z czujnika wilgoci A -> C
def CalculateMoist():
    raw_value = mvalue.read_u16()

    moisture_val = cal(raw_value,65536,13000,0,100)

    if moisture_val > 100:
        moisture_val = 100

    return moisture_val,raw_value

def PrintMoist(moisture_val,raw_value):
        print(moisture_val, '%')
        print(raw_value) #raw value, odczyt bitowy potrzebny do okreslania minimum i 
        # maksimum użytecznego zakresu czujnika
        return moisture_val,raw_value

#pętla programowa wykonująca zadanie
while True:
    moisture_val, raw_value = CalculateMoist()
    PrintMoist(moisture_val,raw_value)
    print(mvalue)
    time.sleep(1)