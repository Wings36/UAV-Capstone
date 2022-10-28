# Import Python System Libraries
from ast import IsNot
from email import message
from time import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import RFM9x
import adafruit_rfm9x
import datetime

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None
packetLossCount = 0
packetCount = 0
x = datetime.datetime.now()
fileName = "test_" + str(x) + ".txt"
file1 = open(fileName, 'w')

lastTime = int(time() * 1000)
key = bytes("TESTUW", "utf-8")

while True:
    packet = None
    rfm9x.send(key)
    
    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        print("Waiting...")
        if packetCount != 0:
            packetLossCount = packetLossCount + 1

    else:
        # Display the packet text and rssi
        x2 = datetime.datetime.now()
        packetCount = packetCount + 1
        currentTime = int(time()*1000)
        pingTime = currentTime - lastTime
        lastTime = currentTime
        rssi = rfm9x.last_rssi
        snr = rfm9x.last_snr
        logMessege = "Ping: "+ str(pingTime) + "  Packet Loss: "+ str(packetLossCount)+ "  RSSI: "+ str(rssi)+ "  SNR: "+ str(snr) + " " + str(x2) + "\n"
        print(logMessege)
        file1.write(logMessege)
