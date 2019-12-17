#!/usr/bin/env python
import time

from samplebase import SampleBase

RED = list(range(10, 13)) + list(range(20, 24)) + list(range(30, 64))
ORANGE = list(range(24, 30))

class SimpleSquare(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleSquare, self).__init__(*args, **kwargs)

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        while True:
            for x in range(0, self.matrix.width):
                for y in range(0, self.matrix.height):
                    offset_canvas.SetPixel(x, y, 0, 255, 0)
                    if x in RED:
                        offset_canvas.SetPixel(x, y, 150, 0, 0)
                    if x in ORANGE:
                        offset_canvas.SetPixel(x, y, 255, 100, 0)
                    # for y in range(self.matrix.height - 15, self.matrix.height):
                    #    offset_canvas.SetPixel(x, y, 0, 0, 0)

            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
            time.sleep(10)


# Main function
if __name__ == "__main__":
    simple_square = SimpleSquare()
    if (not simple_square.process()):
        simple_square.print_help()
