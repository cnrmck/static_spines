from __future__ import division, print_function


import os
import sys
import time
import logging
import spine_math
from config import Config
from collections import deque
# the copy function already exists in processing, cpalias prevents namespace trampling
from copy import copy as cpalias
from spine_class import SpinePoint
from spatial_log import SpatialLog

config = Config()
sl = SpatialLog(log_level = config.log_level)


# need to try higher bases than 2.
# need to figure out the translational properties of each spiney thing
"""
Todos:
1. Add a simple config file. DONE
2. Add a better way to alternate between different functions. DONE
3. Rotate the spine graph so it's the way you want it.
"""

# defines large color_space to be the same as the HSL standard
# no reason to change this
color_space = 360
color_inc = color_space / config.num_colors
# set the starting color value
color_val = 0 - color_inc

high = 0
low = 0
prev_node = None

def get_current_color(color_val):
    """ return the current color based on the color val passed in """
    return color(color_val, 70, 80, 100)
# INITIALIZE starting values
prev_len_nodes = 1
prev_prime = 0
# initialize the most_recent_prime_node to prev_prime and whatever the current_color starts as
most_recent_prime_node = SpinePoint(prev_prime, get_current_color(color_val))

# this has to be the first function that is encountered
def setup():
    # HSB works as: hue, saturation, brightness, opacity. (HSL would be nicer)
    # colorMode defines maximum values for each dimension
    colorMode(HSB, color_space, 100, 100, 1.0)
    size(config.canvas_width, config.canvas_height)
    clear_background()
    frameRate(config.frame_rate)

# this has to be the second function that is encountered
def draw():
    pass

class Data(object):
    """
    Hold onto some data we would like to make accessible for the entire module
    """
    def __init__(self):
        self.largest_order = 0
        self.base = config.base
        self.center_x = config.canvas_width / 2
        self.center_y = config.canvas_height / 2
        self.nodes = deque()

    def reset_nodes(self):
        self.nodes = deque()

data = Data()

def calc_offset(prev_node, node2, changeval = 50):
    """
    this function doesn't work and I don't want to try to figure it out anymore
    """
    print("turn off offset_connecting_lines, it's broken")
    side_x = node1.x - node2.x
    side_y = node1.y - node2.y

    m = side_y / side_x

    abs_change_x = (1/m) * changeval
    abs_change_y = (m) * changeval

    if node1.x < node2.x:
        node1_offset_x = node1.x + abs_change_x
    else:
        node1_offset_x = node1.x - abs_change_x

    if node1.y < node2.y:
        node1_offset_y = node1.y + abs_change_y
    else:
        node1_offset_y = node1.y - abs_change_y

    return node1_offset_x, node1_offset_y

def connect_nodes(start_node, end_node):
    with sl as l:
        l.debug("Connecting node {} to {}".format(start_node.number, end_node.number))

        if config.connections_in_current_color is True:
            stroke(end_node.current_color)
        else:
            stroke(360, 50, 50, 50)
        strokeWeight(1)

        x1, y1 = final_x_y_coords(start_node)
        x2, y2 = final_x_y_coords(end_node)

        if config.offset_connecting_lines is True:
            # calculate the offset for start_node to make it easier to determine direction visually
            # TODO: Make this work, right now it's trash
            prev_node_offset_x, prev_node_offset_y = calc_offset(start_node, end_node)
            line(prev_node_offset_x, prev_node_offset_y, end_node.x, end_node.y)
        else:
            # Connects nodes directly to each other
            line(x1, y1, x2, y2)

def draw_spine_point(node):
  if config.color_primes == True and node.isprime == True:
      dot_color = node.current_color
  else:
      dot_color = color(0, 0, 0, 80)

  if config.only_indicate_primes is True and node.isprime == False:
      # if you are only indicating primes, and this one isn't prime, do nothing
      pass

  else:
      x, y = final_x_y_coords(node)
      fill(dot_color)
      ellipse(x, y, 5, 5)

def final_x_y_coords(node):
    """
    add the center_x and center_y values to get away from (0,0) the proper amount
    """
    x = node.x * config.scale_factor + data.center_x
    y = node.y * config.scale_factor + data.center_y
    return x, y

def draw_shadows(node, len_r = 50, auto_shadow_len = False):
    """
    this function can be used to draw shadows on the spines.
    These are not sophisticated shadows, but they can add a certain depth
    when done right.
    """
    if auto_shadow_len:
        numer, denom = get_updated_numer_and_denom(node)
        len_r = (denom / (node.number+1))

    x, y = final_x_y_coords(node, len_r)
    strokeWeight(2)
    stroke(0, 0, 0, 20)
    line(data.center_x, data.center_y, x-4, y+4)

def draw_spines(node):
    strokeWeight(2)
    textSize(12)
    stroke(node.current_color)

    # shadow has to be drawn before the line that it relates to
    if config.draw_shadows:
        draw_shadows(node, node.number)

    x, y = final_x_y_coords(node)
    line(data.center_x, data.center_y, x, y)

def get_updated_numer_and_denom(node):
    low, high = spine_math.yield_next_range((data.base**data.largest_order)-1)
    node.update_fraction(high)
    numer, denom = node.get_numer_and_denom()

    return numer, denom

def write_text(node, x, y):
    with sl as l:

        fill(1, 1, 0)
        textSize(10)
        if config.write_text is True:
            l.debug("Writing text for number {}".format(node.number))
            text(node.number, x+3, y-3)

        low, high = spine_math.yield_next_range((data.base**data.largest_order)-1)
        node.update_fraction(high)

        if config.write_fraction:
            l.debug("Writing fraction {} for number {}".format(node.display_fraction, node.number))
            text(node.display_fraction, x + 15, y+5)

def plot_it(node):
    y_top = data.center_y - config.scale_factor
    x_left = data.center_x - config.scale_factor

    y_height = config.scale_factor*2
    x_width = config.scale_factor*2

    y_bottom = y_top + y_height
    x_right = x_left + x_width

    numer, denom = get_updated_numer_and_denom(node)
    fraction = numer / denom

    stroke(node.current_color)
    dot_color = color(0, 0, 0, 80)

    if config.color_primes is True and node.isprime:
        strokeWeight(3)
    else:
        noStroke()

    fill(dot_color)


    if config.expansionary_plot is True:
        expan_inc = config.expansion_increment
        ellipse(x_left + (expan_inc * numer), y_top
                + (expan_inc * node.number), 5, 5)

    else:
        x = fraction*(x_width) + x_left
        y = (node.number/denom)*(y_height) + y_top
        ellipse(x, y, 5, 5) # fit screen version

    if config.write_text:
        if config.expansionary_plot is True:
            # TODO:
            write_text(node, x_left + (expan_inc * numer), y_top) + (expan_inc * node.number)
        else:
            write_text(node, x + 5, y + 4)

def draw_node(prev_node, node):
    """
    Use the given prev_node and node and draw them to the canvas.
    Depending on the config settings you have the drawings will look different

    Return the node so that it can be passed in as the previous node next time

    Arguments
    prev_node - the node that was drawn before this one
    node - the current node of interest
    """
    with sl as l:
        global most_recent_prime_node
        l.debug("Most recent prime node is: {}".format(most_recent_prime_node.number))

        if config.cartesian_plot is True:
            with sl as l:
                l.debug("Cartesian plotting node {}".format(node.number))
                plot_it(node)

        if config.spine_length_is_its_number:
            node.vector_mode = True
        else:
            node.vector_mode = False

        with sl as l:
            if config.draw_spines:
                l.debug('Drawing spine for node {}'.format(node.number))
                draw_spines(node)

            if prev_node and config.draw_connecting_lines:
                if not config.reverse_display_order:
                    connect_nodes(node, prev_node)
                else:
                    connect_nodes(prev_node, node)

            if config.indicate_end_of_spine:
                draw_spine_point(node)

            if config.write_text and (config.draw_connecting_lines or config.draw_spines):
                x, y = final_x_y_coords(node)
                write_text(node, x, y)

            if config.prime_gaps is True and node.isprime is True:

                if config.reverse_display_order is False:
                    sys.exit("ERROR: Cannot do prime_gaps = True and reverse_display_order = True at the same time.")

                if config.save_prime_gaps is True:
                    # save the image of the prime gap
                    save(str(config.image_path) + str(most_recent_prime_node.number)) + "-" + str(node.number) + ".png"

                most_recent_prime_node = node
                clear_background()

        return node

def draw_nodes(start_node, data):
    prev_node = start_node
    with sl as l:
        for node in data.nodes:
            l.debug("Drawing node {}".format(node.number))
            prev_node = draw_node(prev_node, node)

    # should this be returning node or prev_node?
    return prev_node

def clear_background():
    background(0, 0, 99)

def keyPressed():
    global low
    global data
    global high
    global color_val
    global color_inc
    global prev_node
    global prev_prime
    global prev_prime
    global prev_len_nodes

    with sl as l:
        l.info("Working...")

        if key == 's':
            l.info("Saving...")
            save(str(time.time()) + ".png")

        # if not saving, run another step
        else:
            prime_count = 0 # not used
            current_color = get_current_color(color_val)

            if config.clear_before_each_step is True:
                l.info("Clearing background")
                clear_background()

            if config.step_by_exponential_range is True:
                l.info("Stepping exponentially")
                low, high = spine_math.yield_next_range(high)
                with sl as l:
                    step = range(low, high)
                    l.debug("Next step is {}-{} with len {}".format(low, high, len(step)))
                data.largest_order += 1

            else:
                l.info("Stepping linearly")
                # step one number at a time (this could be configured eventually)
                if high == 0:
                    low = 0
                    high = 1
                else:
                    low += 1
                    high += 1
                with sl as l:
                    step = range(low, high)
                    l.debug("Next step is {}-{} with len {}".format(low, high, len(step)))

            with sl as l:
                if config.draw_individually is False:
                    l.info("Drawing All Nodes")
                    if config.reverse_display_order is False:
                        for n in step:
                            node = SpinePoint(n, current_color)
                            data.nodes.appendleft(node)

                        l.info("Drawing nodes up to: {}".format(n))
                        prev_node = draw_nodes(prev_node, data)

                    elif config.reverse_display_order is True:
                        for n in step:
                            node = SpinePoint(n, current_color)
                            data.nodes.append(node)

                        l.info("Drawing nodes in reverse up to: {}".format(n))
                        prev_node = draw_nodes(node, data)

                else:
                    l.info("Drawing step individually")
                    for n in step:
                        node = SpinePoint(n, current_color)
                        prev_node = draw_node(prev_node, node)




            color_val += color_inc
            l.info("Done")


                # if node.isprime:
                    # prime_count += 1
                # drawn_nodes_l.append(node)
                # drawn_nodes.add(node)
    # take this ratio, plug it back into the equation. For whatever reason the
    # first one is the Fibonnoci sequence
    # has something to do with prime location
    # print(prime_count - prev_prime, len(data.nodes) - prev_len_nodes)
    #save("other" + str(data.largest_order) + ".png")
    # prev_len_nodes = len(data.nodes)
    # prev_prime = prime_count
