from __future__ import division, print_function
from collections import deque
from spine_class import SpinePoint
import spine_math
# the copy function already exists in processing, cpalias prevents namespace trampling
from copy import copy as cpalias
from config import Config
config = Config()

# need to try higher bases than 2.
# need to figure out the translational properties of each spiney thing
"""
Todos:
1. Add a simple config file. DONE
2. Add a better way to alternate between different functions. DONE
3. Rotate the spine graph so it's the way you want it.
"""

drawn_nodes = set()
drawn_nodes_l = list()

# defines large color_space to be the same as the HSL standard
# no reason to change this
color_space = 360
color_inc = color_space / config.num_colors
# set the starting color value
color_val = 0 - color_inc

high = 0
low = 0
prev_node = None

def reset_background():
    background(0, 0, 99)


def setup():
    # HSB works as: hue, saturation, brightness, opacity. (HSL would be nicer)
    # colorMode defines maximum values for each dimension
    colorMode(HSB, color_space, 100, 100, 1.0)
    size(config.canvas_width, config.canvas_height)
    reset_background()
    frameRate(config.frame_rate)


def draw():
    pass

prev_len_nodes = 1
prev_prime = 0

class Data(object):
    def __init__(self):
        self.largest_order = 0
        self.base = config.base
        self.center_x = config.canvas_width / 2
        self.center_y = config.canvas_height / 2
        self.nodes = deque()

    def reset_nodes(self):
        self.nodes = deque()

data = Data()

def keyPressed():
    global high
    global low
    global drawn_nodes
    global drawn_nodes_l
    global color_val
    global prev_len_nodes
    global prev_prime
    global color_inc
    global prev_prime
    global prev_node

    prime_count = 0
    current_color = color(color_val, 70, 80, 100)

    if config.reset_after_each_step is True:
        reset_background()

    if config.step_by_exponential_range is True:
        low, high = spine_math.yield_next_range(high)
        step = range(low, high)
    else:
        if high == 0:
            low = 0
            high = 1
        else:
            low += 1
            high += 1
        step = range(low, high)

    for n in step:
        node = SpinePoint(n, current_color)
        if config.reverse_display_order is False:
            data.nodes.appendleft(node)
        else:
            prev_node = draw_node(prev_node, node)

    if config.reverse_display_order is False:
        prev_node = draw_nodes(prev_node)

    color_val += color_inc
    data.largest_order += 1


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

def draw_node(prev_node, node):
    if config.cartesian_plot is True:
        plot_it(node)

    if config.spine_length_is_its_number:
        node.vector_mode = True
    else:
        node.vector_mode = False

    if config.draw_spines:
        draw_spines(node)

    if prev_node and config.draw_connecting_lines:
        if not config.reverse_display_order:
            connect_nodes(node, prev_node)
        else:
            connect_nodes(prev_node, node)

    if node.isprime:

        if config.prime_gaps is True:
            reset_background()

            if config.save_prime_gaps is True:
                # save the image of the prime gap
                save(str(prev_prime) + "-" + str(node.number) + ".png")

            data.reset_nodes()
            prev_node = None
            prev_prime = node.number

    return node

def draw_nodes(start_node):
    prev_node = start_node
    for node in data.nodes:
        prev_node = draw_node(prev_node, node)

    return node

def draw_spines(node):
    strokeWeight(2)
    textSize(12)
    stroke(node.current_color)

    # shadow has to be drawn before the line that it relates to
    if config.draw_shadows:
        draw_shadows(node, node.number)

    x, y = final_x_y_coords(node)
    line(data.center_x, data.center_y, x, y)

    if config.write_text:
        write_text(node, x, y + 2)

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
    if config.connections_in_current_color is True:
        stroke(end_node.current_color)
    else:
        stroke(360, 50, 50, 50)
    strokeWeight(1)

    x1, y1 = final_x_y_coords(start_node)
    x2, y2 = final_x_y_coords(end_node)

    if config.offset_connecting_lines is True:
        # calculate the offset for start_node to make it easier to determine direction
        prev_node_offset_x, prev_node_offset_y = calc_offset(start_node, end_node)
        line(prev_node_offset_x, prev_node_offset_y, end_node.x, end_node.y)
    else:
        line(x1, y1, x2, y2)

    if config.draw_nodes:
        ellipse(x1, y1, 5, 5)

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

def write_text(node, x, y):
    fill(1, 1, 0)
    textSize(10)
    text(node.number, x+3, y-3)
    low, high = spine_math.yield_next_range((data.base**data.largest_order)-1)
    node.update_fraction(high)

    if config.write_fraction:
        text(node.display_fraction, x + 15, y+5)

def get_updated_numer_and_denom(node):
    low, high = spine_math.yield_next_range((data.base**data.largest_order)-1)
    node.update_fraction(high)
    numer, denom = node.get_numer_and_denom()

    return numer, denom

def plot_it(node, no_stroke=True):
    y_top = 20
    y_height = config.canvas_height - 30 # last value just used for bottom padding

    x_left = 10
    y_bottom = y_top + y_height

    numer, denom = get_updated_numer_and_denom(node)
    fraction = numer / denom

    stroke(node.current_color)
    strokeWeight(5)
    dot_color = color(0, 0, 0, 80)
    fill(dot_color)

    # no_stroke is an optional condition that can be passed in to do variable formatting
    if no_stroke is True:
        # remove outlines
        noStroke()

    if config.expansionary_plot is True:
        # tell us how much to move by for expansionary version
        x_inc = 5
        y_inc = 5
        ellipse(x_left + (x_inc * numer), y_bottom - (y_inc * node.number), 5, 5) # expansionary version

    x = fraction*(width-20) + x_left
    y = (node.number/denom)*(y_height-20)+10
    ellipse(x,y, 5, 5) # fit screen version

    if config.write_text:
        if config.expansionary_plot is True:
            write_text(node, x_left + (x_inc * numer) + 2, y_bottom - (y_inc * node.number) - 2)
        else:
            write_text(node, x + 5, y + 4)


def final_x_y_coords(node):
    """
    add the center_x and center_y values to get away from (0,0) the proper amount
    """
    x = node.x * config.scale_factor + data.center_x
    y = node.y * config.scale_factor + data.center_y
    return x, y
