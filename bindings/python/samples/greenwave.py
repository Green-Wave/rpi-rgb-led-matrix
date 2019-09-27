#!/usr/bin/env python
from samplebase import SampleBase
import time


class GrayscaleBlock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GrayscaleBlock, self).__init__(*args, **kwargs)

    def run(self):
        while True:
            print("Starting loop...")
            # request time
            # TODO
            # color LED matrix
            print("Coloring LED...")
            self.color(color="green", ratio_left=0.5)
            # sleep
            print("Sleeping ...")
            time.sleep(1)
            print("Loop done.")
            print()

    def color(self, color="green", ratio_left=0.6):
        width = self.matrix.width  # 64
        height = self.matrix.height  # 32
        brightness = 150  # 255 with red pulls too much power
        width_on = width * ratio_left

        for y in range(0, height):
            for x in range(int(width - width_on), width):
                if color == "green":
                    self.matrix.SetPixel(x, y, 0, brightness, 0)
                elif color == "red": 
                    self.matrix.SetPixel(x, y, brightness, 0, 0)

# Main function
if __name__ == "__main__":
    grayscale_block = GrayscaleBlock()
    if (not grayscale_block.process()):
        grayscale_block.print_help()
