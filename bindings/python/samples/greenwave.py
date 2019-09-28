#!/usr/bin/env python3

import time
import json
import sys

import requests

# RGB MATRIX IMPORTS
from samplebase import SampleBase

# LORA IMPORTS
import board
import busio
import digitalio
import adafruit_rfm9x

# LORA CONFIG
RADIO_FREQ_MHZ = 868.0  
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
# LORA SETUP
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)


class GrayscaleBlock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GrayscaleBlock, self).__init__(*args, **kwargs)


    def run(self):
        while True:
            # get phase timing
            print("Starting loop...")
            # color, seconds_phase_left, seconds_phase_total = self.get_http_time()
            try:
                print("getting lora...")
                color, seconds_phase_left, seconds_phase_total = self.get_lora_time()
            except KeyboardInterrupt:
                raise
            except:
                print("Unexpected error:", sys.exc_info()[0])
                continue

            # make last seconds empty frame
            seconds_phase_left -= 5
            seconds_phase_total -= 5

            # color LED matrix
            print("Coloring LED...")
            ratio_left = seconds_phase_left / seconds_phase_total
            self.color(color=color, ratio_left=ratio_left)
            
            # sleep
            print("Sleeping ...")
            time.sleep(0.1)
            print("Loop done.")
            print()

    def get_lora_time(self):
        packet = rfm9x.receive(timeout=5)
        if packet is None:
            # Packet has not been received
            print('Received nothing! Listening again...') 
        else:
            print('Received (raw bytes): {0}'.format(packet))
            packet_text = str(packet, 'ascii')
            print('Received (ASCII): {0}'.format(packet_text))
            [green, seconds_left, seconds_total] = packet_text.split(";")
            if green == "1":
                color = "green"
            else:
                color = "red"
            print(f"color: {color}")
            print("seconds left:", seconds_left)
            print("seconds total:", seconds_total)
            # Also read the RSSI (signal strength) of the last received message and print it.
            rssi = rfm9x.rssi
            print('Received signal strength: {0} dB'.format(rssi))
            return color, float(seconds_left), float(seconds_total)

    def get_http_time(self):
        print("Getting seconds left for :phase...")
        response = requests.get("http://172.16.2.107/seconds_phase_left")
        res_dict = json.loads(response.text)
        print(res_dict)
        if res_dict["is_green"]:
            color = "green"
        else:
            color = "red"
        seconds_phase_left = res_dict["seconds_phase_left"]
        seconds_phase_total = res_dict["seconds_phase_total"]
        time.sleep(0.5)
        return color, seconds_phase_left, seconds_phase_total

    def color(self, color, ratio_left):
        width = self.matrix.width  # 64
        height = self.matrix.height  # 32
        if color == "green":
            brightness = 155
        else:
            brightness = 100   # 255 with red pull too much power
        width_on = width * ratio_left

        # draw 'ratio left'
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if x >= (width - int(width_on)):
                    if color == "green":
                        self.matrix.SetPixel(x, y, 0, brightness, 0)
                    elif color == "red": 
                        self.matrix.SetPixel(x, y, brightness, 0, 0)
                else:
                    self.matrix.SetPixel(x, y, 0, 0, 0)
         
        # draw frame
        for y in range(0, height):
            if color == "green":
                self.matrix.SetPixel(0, y, 0, brightness, 0)
                self.matrix.SetPixel(width - 1, y, 0, brightness, 0)
            elif color == "red": 
                self.matrix.SetPixel(0, y, brightness, 0, 0)
                self.matrix.SetPixel(width - 1, y, brightness, 0, 0)
        for x in range(0, width):
            if color == "green":
                self.matrix.SetPixel(x, 0, 0, brightness, 0)
                self.matrix.SetPixel(x, height - 1, 0, brightness, 0)
            elif color == "red": 
                self.matrix.SetPixel(x, 0, brightness, 0, 0)
                self.matrix.SetPixel(x, height - 1, brightness, 0, 0)

# Main function
if __name__ == "__main__":
    grayscale_block = GrayscaleBlock()
    if (not grayscale_block.process()):
        grayscale_block.print_help()
