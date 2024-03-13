import machine, onewire, ds18x20, time, socket, network, loginData, plants, mailBase
from time import sleep
from machine import ADC, Pin
from collections import namedtuple

mvalue = ADC(Pin(27))

tempsens = machine.Pin(22)
sensor = ds18x20.DS18X20(onewire.OneWire(tempsens))
datas = sensor.scan()

ssid = loginData.ssid
password = loginData.password

sender_email = mailBase.sender_email
sender_name = mailBase.sender_name
sender_app_password = mailBase.sender_app_password
recipient_email = mailBase.recipient_email
email_subject = mailBase.email_subject


# funkcja kalibrująca i normalizująca odczyt higrometru.
def cal(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def Moisture():
    mvalue = ADC(Pin(27))
    raw_value = mvalue.read_u16()
    moisture_val = cal(raw_value, 65536, 13000, 0, 100)
    if moisture_val > 100:
        moisture_val = 100
    soilmoisture = moisture_val
    return soilmoisture


def Temperature():
    soiltemperature = 0
    sensor.convert_temp()
    time.sleep_ms(750)
    for data in datas:
        soiltemperature = round(sensor.read_temp(data), 1)
    return soiltemperature


def connect():
    good_connection = False

    while good_connection == False:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        for ct in range(5):
            if wlan.isconnected() == True:
                good_connection = True
            else:
                print("Waiting for connection...")
                sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip


def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(2)
    return connection


def webpage(soilmoisture, soiltemperature):
    plants_list_html = ""

    # iteracja po roślinach w celu skrócenia kodu html
    for plant_name, plant_data in plants.Plants.items():
        plants_list_html += f"""
        <details>
            <summary class="plants_list">
                <b>{plant_name}</b>
            </summary>
            <p> Temperatura optymalna: {plant_data.temp}°C</p>
            <p> Minimalna wilgotność gleby: {plant_data.minMoist}%</p>
            <p> Maksymalna wilgotność gleby: {plant_data.maxMoist}%</p>
        </details>
        """

    html = f"""
<!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="utf-8">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
        <style>
          body{{
            font-family: 'Roboto', sans-serif; background-color: #d8d8d8;
            margin: 0;
            padding: 0;
          }}
            input[type=submit] {{
                    box-shadow:inset 0px 1px 0px 0px #ffffff;
	                background:linear-gradient(to bottom, #f9f9f9 5%, #e9e9e9 100%);
	                background-color:#f9f9f9;
	                border-radius:6px;
	                border:1px solid #dcdcdc;
	                display:inline-block;
	                cursor:pointer;
	                color:#545454;
	                font-family:Arial;
	                font-size:15px;
	                font-weight:bold;
	                padding:6px 24px;
	                text-decoration:none;
	                text-shadow:0px 1px 0px #ffffff;
                    width: 150px;
            }}
          input[type=submit]:hover {{
                background:linear-gradient(to bottom, #e9e9e9 5%, #f9f9f9 100%);
	            background-color:#e9e9e9;
            }}
          #header{{
            display: flex;
            background: rgb(46,147,60);
            background: linear-gradient(180deg, rgba(46,147,60,1) 0%, rgba(216,216,216,1) 95%);
            margin-bottom: 100px;
            flex-direction: row;
            align-items: center;
            height: 150px;

          }}
          #czas-na-zywo{{
          margin-bottom: 13px;
                     
          }}
          #header_left{{
            width: 50%;
            align-items: center;
            padding-left: 15px;
          }}
          
          #header_right{{
            width: 50%;
            display: flex;
          }}
          
          #header_right_left{{
            width: 20%;
            margin-left: 40%;
            line-height: 0.1;
          }}
          
          #header_right_mid{{
            width: 20%;
            text-align: center;
            line-height: 0.1;
            font-size: 20px;
           
            
          }}
          
          #header_right_right{{
            width: 20%;
            text-align: center;
            line-height: 0.1;
            font-size: 20px;
            
            
          }}
          
            .button1 {{
                display: inline-block;
            }}
            .div_left {{
                width: 40%;
                margin-left: 5%;
                margin-right: 5%;
                line-height: 1;
                margin-right: 5%;
            }}
            .div_right {{
                width: 40%;
                margin-left: 5%;
                margin-right: 5%;
                line-height: 1;
            }}
            .plants_list {{
                font-size: 18px;
                line-height: 2;
                margin-left: 0;
            }}
          
            hr {{
            display: block;
            margin-bottom: 0.5em;
            margin-left: 0;
            margin-right: auto;
            border-style: inset;
            border-width: 1px;
            border: 1.5px solid green;
            width: 75%;
            text-align: left;
            }}
        </style>
        <script>
            function updateTime() {{
                var data = new Date();
                var hour = data.getHours();
                var minute = data.getMinutes();
                var second = data.getSeconds();

                minute = minute < 10 ? '0' + minute : minute;
                second = second < 10 ? '0' + second : second;

                var time = hour + ':' + minute + ':' + second;
                document.getElementById('current_time').innerHTML = time;

                setTimeout(updateTime, 1000);
            }}

            window.onload = function() {{
                updateTime();
            }};
        </script>
    </head>
    <body>
         <div id="header">
            <div id="header_left"><h1>Stacja pomiaru warunków gleby</h1>
            </div>
            <div id="header_right">
              <div id="header_right_left">
                <b><p id="current_time" style="text-align: center; font-size: 20px;"></p>
                <center><img src="https://www.svgrepo.com/show/59567/wall-clock-of-circular-shape.svg" alt="Wilgotność gleby"
                         style="width: 50px;" /> </center>
                </b> 
              </div>
              <div id="header_right_mid">
                    <p><b>{soilmoisture}%</b><br>
                    <img src="https://www.svgrepo.com/show/341055/soil-moisture.svg" alt="Wilgotność gleby"
                         style="width: 70px;" />
                </p>
              </div>
              <div id="header_right_right">
                <p><b>{soiltemperature}°C</b><br>
                    <img src="https://www.svgrepo.com/show/341059/soil-temperature.svg" alt="Temperatura gleby"
                         style="width: 70px;">
                </p>
              </div>
            </div>
        </div>
        <div style="display: flex;">
            <div class="div_left">
                <h2>Lista roślin</h2>
                <hr>
                {plants_list_html}
            </div>
            <div class="div_right">
            <h2>Wybierz roślinę do monitorowania</h2>
            <hr>
            <p>
            <form class="button1" action="./ogorek"> <input type="submit" value="Ogórek" /></form>
            <form class="button1" action="./malina"> <input type="submit" value="Malina" /></form>
            <form class="button1" action="./salata"> <input type="submit" value="Sałata" /></form>
            </p>
            <p>
            <form class="button1" action="./zurawina"> <input type="submit" value="Żurawina" /></form>
            <form class="button1" action="./agawa"> <input type="submit" value="Agawa" /></form>
            <form class="button1" action="./truskawka"> <input type="submit" value="Truskawka" /></form>
            </p>
            <p>
            <form class="button1" action="./tulipan"> <input type="submit" value="Tulipan" /></form>
            <form class="button1" action="./kaktus"> <input type="submit" value="Kaktus" /></form>
            <form class="button1" action="./kocimietka"> <input type="submit" value="Kocimiętka" /></form>
            </p>
            <p>
            <form class="button1" action="./pomidor"> <input type="submit" value="Pomidor" /></form>
            <form class="button1" action="./cebula"> <input type="submit" value="Cebula" /></form>
            </p>
            <br>
            <p style= "line-height: 2; width: 458px; text-align: justify;"> 
            Przed wybraniem rośliny należy umieścić czujniki w glebie i upewnić się, że jest ona nawodniona. 
            Następnie wybrać odpowiednią roślinę i oczekiwać na alert o zbyt niskim nawodnieniu.
            Nie należy wybierać monitorowania drugiej rośliny podczas trwającego procesu.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return str(html)


def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)

        soilmoisture = Moisture()
        sleep(1)

        soiltemperature = Temperature()
        sleep(1)

        try:
            request = request.split()[1]
        except IndexError:
            pass
        while request == "/agawa?":
            soilmoisture = Moisture()
            if soilmoisture < plants.Plants["Ogórek"].minMoist:
                mailBase.SendMail(sender_email, sender_name, sender_app_password, recipient_email, "Twoja agawa ma za mało wody")
                print("Mail sent")
                break
            print("Poziom nawodnienia w normie")
            time.sleep(5)

        while request == "/cebula?":
            soilmoisture = Moisture()
            if soilmoisture < plants.Plants["Cebula"].minMoist:
                mailBase.SendMail(
                    sender_email, sender_name, sender_app_password, recipient_email, "Twoja cebula ma za mało wody"
                )
                break
            print("Poziom nawodnienia w normie")
            time.sleep(5)

        while request == "/kaktus?":
            soilmoisture = Moisture()
            if soilmoisture < plants.Plants["Kaktus"].minMoist:
                mailBase.SendMail(sender_email, sender_name, sender_app_password, recipient_email, "Twój kaktus za mało wody")
                break
            print("Poziom nawodnienia w normie")
            time.sleep(5)

        while request == "/kocimietka?":
            soilmoisture = Moisture()
            if soilmoisture < plants.Plants["Kocimiętka"].minMoist:
                mailBase.SendMail(
                    sender_email, sender_name, sender_app_password, recipient_email, "Twoja kocimiętka ma za mało wody"
                )
                break
            print("Poziom nawodnienia w normie")
            time.sleep(5)

        while request == "/malina?":
            soilmoisture = Moisture()
            if soilmoisture < plants.Plants["Malina"].minMoist:
                mailBase.SendMail(
                    sender_email, sender_name, sender_app_password, recipient_email, "Twoje maliny mają za mało wody"
                )
                break
            print("Poziom nawodnienia w normie")
            time.sleep(5)

        while request == "/ogorek?":
            soilmoisture = Moisture()
            if soilmoisture < plants.Plants["Ogórek"].minMoist:
                mailBase.SendMail(
                    sender_email, sender_name, sender_app_password, recipient_email, "Twoje ogórki mają za mało wody"
                )
                break
            print("Poziom nawodnienia w normie")
            time.sleep(5)

        while request == "/pomidor?":
            soilmoisture = Moisture()
            if soilmoisture < plants.Plants["Pomidor"].minMoist:
                mailBase.SendMail(
                    sender_email, sender_name, sender_app_password, recipient_email, "Twoje pomidory mają za mało wody"
                )
                break
            print("Poziom nawodnienia w normie")
            time.sleep(5)

        while request == "/sałata?":
            soilmoisture = Moisture()
            if soilmoisture < plants.Plants["Sałata"].minMoist:
                mailBase.SendMail(
                    sender_email, sender_name, sender_app_password, recipient_email, "Twoja sałata ma za mało wody"
                )
                break
            print("Poziom nawodnienia w normie")
            time.sleep(5)

        while request == "/truskawka?":
            soilmoisture = Moisture()
            if soilmoisture < plants.Plants["Truskawka"].minMoist:
                mailBase.SendMail(
                    sender_email, sender_name, sender_app_password, recipient_email, "Twoje truskawki mają za mało wody"
                )
                break
            print("Poziom nawodnienia w normie")
            time.sleep(5)

        while request == "/tulipan?":
            soilmoisture = Moisture()
            if soilmoisture < plants.Plants["Tulipan"].minMoist:
                mailBase.SendMail(
                    sender_email, sender_name, sender_app_password, recipient_email, "Twoje tulipany mają za mało wody"
                )
                break
            time.sleep(5)

        while request == "/zurawina?":
            soilmoisture = Moisture()
            if soilmoisture < plants.Plants["Żurawina"].minMoist:
                mailBase.SendMail(
                    sender_email, sender_name, sender_app_password, recipient_email, "Twoja żurawina ma za mało wody"
                )
                break
            print("Poziom nawodnienia w normie")
            time.sleep(5)

        html = webpage(soilmoisture, soiltemperature)
        client.sendall(html)
        client.close()


try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
