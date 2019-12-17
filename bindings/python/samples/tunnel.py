#!/usr/bin/env python
import time

from samplebase import SampleBase

RED = list(range(35, 64))
GREEN = range(0, 35)

class SimpleSquare(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleSquare, self).__init__(*args, **kwargs)

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        for x in range(0, self.matrix.width):
            for y in range(0, self.matrix.height):
                if x in GREEN:
                    offset_canvas.SetPixel(x, y, 0, 255, 0)
                if x in RED:
                    offset_canvas.SetPixel(x, y, 150, 0, 0)
                # for y in range(self.matrix.height - 15, self.matrix.height):
                #    offset_canvas.SetPixel(x, y, 0, 0, 0)

        offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
        time.sleep(10)


# Main function
if __name__ == "__main__":
    simple_square = SimpleSquare()
    if (not simple_square.process()):
        simple_square.print_help()
