from umqtt.robust import MQTTClient
import network
import uasyncio
import machine
import ujson

wifiUsername = ''
wifiPassword = ''
mqttClientId = ''
mqttHost = ''
mqttPort = 1883
mqttUsername = ''
mqttPassword = ''

async def connectWifi():

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifiUserName, wifiPassword)
    await uasyncio.sleep_ms(3000)
    return wlan.isconnected()

def connectMQTT():

    try:
        client = MQTTClient(mqttClientId, mqttHost, mqttPort, mqttUsername, mqttPassword)
        client.set_callback(alarm)
        client.connect()
        client.subscribe('alarm')
        return client
    except:
        return False

def alarm(topic, message):
    print((topic, message))

async def checkqueue(client):
    while True:
        await uasyncio.sleep_ms(1)
        client.check_msg()

async def sendData(client, pir):
    obj = {}
    statusPir = False

    while True:
        await uasyncio.sleep_ms(1000)

        if(pir.value() == 1):
            statusPir = True
        else:
            statusPir = False

        obj = {
            'kind':'sensorpir',
            'status': statusPir
        }

        client.publish('send', ujson.dumps(obj))

async def main():

    pir = machine.Pin(2, machine.Pin.IN, machine.Pin.IN)

    if(uasyncio.run(connectWifi())):
        print('WIFI: OK')
        client = connectMQTT()
        if(client):
            print('MQTT: OK')
            event_loop = uasyncio.get_event_loop()
            event_loop.create_task(sendData(client, pir))
            event_loop.create_task(checkqueue(client))
            event_loop.run_forever()
        else:
            print('MQTT: FAIL')
    else:
        print('WIFI: FAIL')

uasyncio.run(main())
