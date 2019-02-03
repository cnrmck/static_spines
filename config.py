class Config(object):
    def __init__(self):
        """
        Options that are listed one on top of the other are linked.

        E.g.
        # set the config for car to True if you want cars
        car = True
        # how many wheels does your car have?
        wheels = 4

        If car were not true then there would not be any wheels to define

        Options that have a newline between them are separate
        # what color are your trees?
        tree_color = 'green'

        # what color is the sky
        sky_color = 'blue'
        """
        self.log_level = 'DEBUG'

        # the path to the location you want images (and other data) to be saved
        self.image_path = '/Users/Connor/code/static_spines/data/'

        # specifies the number of colors to color exponents with
        self.num_colors = 18

        self.base = 2

        # if True saves having to redraw the image every time, but less beautiful
        # test this
        self.reverse_display_order = True
        # clear the screen before every step
        self.clear_before_each_step = True

        # the width of the canvas
        self.canvas_width = 1000

        # the height of the canvas
        self.canvas_height = 1000

        # default is 60, but most of the time that cannot be achieved
        self.frame_rate = 60

        # if True the next display will be range(n^exp - n^(exp - 1), n^(exp))
        # if False the next step will be the next number
        self.step_by_exponential_range = True

        self.color_primes = True

        self.prime_gaps = False
        # save prime gaps
        self.save_prime_gaps = True

        # writes the number associated with the each SpinePoint
        self.write_text = False
        # writes the fraction associated with the each SpinePoint
        self.write_fraction = False

        # draw spines as long as their number (if 5 spine is 5 units long)
        self.spine_length_is_its_number = False
        # TODO: Make this work
        # draw the connecting lines with an offset
        self.offset_connecting_lines = False
        # draw the connecting lines in the current color
        self.connections_in_current_color = True

        # draw the spines
        self.draw_spines = False
        # draws shadows for the spines
        self.draw_shadows = False
        # draw the connecting lines
        self.draw_connecting_lines = True
        # draw points at the end of each
        self.indicate_end_of_spine = True
        self.only_indicate_primes = True

        # if not using spine_length_is_its_number, should be < canvas_height/2
        self.scale_factor = 490

        # plot the number and magnitude as if they were cartesian (x,y) coordinates
        self.cartesian_plot = False
        # plot just like above, but don't limit to the size of the screen
        self.expansionary_plot = False
        # how many units to step by for each increment (in expansionary_plot)
        self.expansion_increment = 2

        self.config_tests()

    def config_tests(self):
        """
        Some simple tests that you can run to find out whether you have any undesireable config settings
        """
        if self.only_indicate_primes == True and self.indicate_end_of_spine == False:
            print("CONFIG WARNING: Cannot indicate primes if spine indication is false."
            "\n    Change indicate_end_of_spine to True")

        if self.offset_connecting_lines is True:
            print("CONFIG WARNING: offsetting connecting lines doesn't work. Change so that offset_connecting_lines = False")
