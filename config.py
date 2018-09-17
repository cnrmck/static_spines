class Config(object):
    def __init__(self):
        # specifies the number of colors to color orders with
        self.num_colors = 18

        self.base = 2
        # saves having to redraw the image every time, but less beautiful
        self.reverse_display_order = False

        self.canvas_width = 1000
        self.canvas_height = 1000

        # default is 60, but most of the time that cannot be achieved
        self.frame_rate = 60

        # the next display will be range(n^exp - n^(exp - 1), n^(exp))
        self.step_by_exponential_range = True

        self.prime_gaps = False
        # save prime gaps
        self.save_prime_gaps = False

        # writes the number associated with the each SpinePoint
        self.write_text = False
        # writes the fraction associated with the each SpinePoint
        self.write_fraction = False

        # draw the connecting lines
        self.draw_connecting_lines = False
        # TODO: Make this work
        # draw the connecting lines with an offset
        self.offset_connecting_lines = False
        # draw the connecting lines in the current color
        self.connections_in_current_color = True
        # draw the spines
        self.draw_spines = False
        # draws shadows for the lines
        self.draw_shadows = False
        # draw points to indicate each node
        self.draw_nodes = True
        # draw spines as long as their number is (number 5 is 5 units long)
        self.spine_length_is_its_number = False

        # if not using spine_length_is_its_number, should be < canvas_height/2
        self.scale_factor = 490

        # clear the screen after every number
        # self.clear_after_every_prime = True
        self.reset_after_each_step = False

        # plot the number and magnitude as if they were cartesian (x,y) coordinates
        self.cartesian_plot = False
        # TODO test this
        self.expansionary_plot = False
