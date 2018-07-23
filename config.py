class Config(object):
    def __init__(self):
        # specifies the number of colors to color orders with
        self.num_colors = 18

        self.base = 2

        self.canvas_width = 1100
        self.canvas_height = 1000

        # default is 60, but most of the time that cannot be achieved
        self.frame_rate = 60

        # TODO figure out what the hell this is
        self.prime_gap = True

        # writes the number associated with the each SpinePoint
        self.write_text = True
        # writes the fraction associated with the each SpinePoint
        self.write_fraction = True

        # TODO test this
        self.expansionary_plot = False
