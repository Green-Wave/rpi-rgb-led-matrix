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

from PIL import Image
from PIL import ImageDraw

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

            # color LED matrix
            print("Coloring LED...")
            self.color()
            
            # sleep
            print("Sleeping ...")
            time.sleep(0.05)
            print("Loop done.")
            print()

    def color(self):
        width = self.matrix.width  # 64
        height = self.matrix.height  # 32
     
        print("minipicture")
        # Then scroll image across matrix...
        img_file = "superheld.png"
        image = Image.open("img/" + img_file).rotate(90).convert('RGB')
        offset = -1
        if "held" in img_file:
            offset = -10
        for n in range(33):  # Start off top-left, move off bottom-right
            self.matrix.Clear()
            _image = image.crop((0, 0, 32, 32))
            self.matrix.SetImage(image, n, offset)
            _image = image.crop((32, 0, 64, 32))
            self.matrix.SetImage(image, n + 32, offset)
            time.sleep(0.05)
        for n in range(33):  # Start off top-left, move off bottom-right
            self.matrix.Clear()
            self.matrix.SetImage(image, 32 - n, offset)
            if n < 33:
                time.sleep(0.05)

# Main function
if __name__ == "__main__":
    grayscale_block = GrayscaleBlock()
    if (not grayscale_block.process()):
        grayscale_block.print_help()
