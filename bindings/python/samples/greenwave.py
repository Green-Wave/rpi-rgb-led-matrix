#!/usr/bin/env python
from samplebase import SampleBase
import time

RESPONSE_MOCKUP = {
    "id_light": 1,
    "is_green": True,
    "is_red": False,
    "seconds_phase_left": 4.1,
    "seconds_phase_total": 50.0,
}

class GrayscaleBlock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GrayscaleBlock, self).__init__(*args, **kwargs)

    def run(self):
        while True:
            print("Starting loop...")
            response = self.get_seconds_phase_left()
            # color LED matrix
            print("Coloring LED...")
            if response["is_green"]:
                color = "green"
            else:
                color = "red"
            ratio_left = response["seconds_phase_left"] / response["seconds_phase_total"]
            self.color(color=color, ratio_left=ratio_left)
            # sleep
            print("Sleeping ...")
            time.sleep(1)
            print("Loop done.")
            print()

    def get_seconds_phase_left(self) -> dict:
        return RESPONSE_MOCKUP

    def color(self, color, ratio_left):
        width = self.matrix.width  # 64
        height = self.matrix.height  # 32
        brightness = 150  # 255 with red pulls too much power
        width_on = (width) * ratio_left  # TODO: check calculation

        # draw 'ratio left'
        for y in range(0, height):
            for x in range(int(width - width_on), width):
                if color == "green":
                    self.matrix.SetPixel(x, y, 0, brightness, 0)
                elif color == "red": 
                    self.matrix.SetPixel(x, y, brightness, 0, 0)

        # draw frame
        #widths_frame = [0, width]
        #heights_frame = [0, height]
        #for y in range(0, height):
        #    for x in widths_frame:
        #        self.matrix.SetPixel(x, y, brightness, brightness, 0)


# Main function
if __name__ == "__main__":
    grayscale_block = GrayscaleBlock()
    if (not grayscale_block.process()):
        grayscale_block.print_help()
