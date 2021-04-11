#Install esptool
pip install esptool

esptool.py  --port COM5 --baud 115200 flash_id
esptool.py  --port COM5 --baud 115200 erase_flash
esptool.py  --port COM5 --baud 460800 write_flash --flash_size=detect 0 esp-01.bin


##Importante instalar estas dependencias
import upip

upip.install('micropython-umqtt.robust')
upip.install('micropython-umqtt.simple')
upip.install('micropython-uasyncio')