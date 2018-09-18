class Config(object):
    def __init__(self):
        # specifies the number of colors to color exponents with
        self.num_colors = 18

        self.base = 2
        # saves having to redraw the image every time, but less beautiful
        self.reverse_display_order = False

        self.canvas_width = 1000
        self.canvas_height = 1000

        # default is 60, but most of the time that cannot be achieved
        self.frame_rate = 60

        # if true the next display will be range(n^exp - n^(exp - 1), n^(exp))
        self.step_by_exponential_range = True
        # clear the screen after every number
        # self.clear_after_every_prime = True
        self.reset_after_each_step = True

        self.color_primes = True

        self.prime_gaps = False
        # save prime gaps
        self.save_prime_gaps = False

        # writes the number associated with the each SpinePoint
        self.write_text = False
        # writes the fraction associated with the each SpinePoint
        self.write_fraction = False

        # draw spines as long as their number (if 5 spine is 5 units long)
        self.spine_length_is_its_number = False
        # draw the connecting lines
        self.draw_connecting_lines = True
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
        self.draw_nodes = False

        # if not using spine_length_is_its_number, should be < canvas_height/2
        self.scale_factor = 490

        # plot the number and magnitude as if they were cartesian (x,y) coordinates
        self.cartesian_plot = False
        # plot just like above, but don't limit to the size of the screen
        self.expansionary_plot = False
        # how many units to step by for each increment (in expansionary_plot)
        self.expansion_increment = 2
