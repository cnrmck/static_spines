from __future__ import division, print_function
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
1. Add a simple config file.
2. Add a better way to alternate between different functions.
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

def setup():
    colorMode(HSB, color_space, 100, 100, 1.0)
    size(config.canvas_width, config.canvas_height)
    background(10, 10, 100)
    frameRate(config.frame_rate)


def draw():
    pass

prev_len_nodes = 1
prev_prime = 0

class Data():
    largest_order = 0
    base = config.base
    center_x = config.canvas_width / 2
    center_y = config.canvas_height / 2
    nodes = []

def keyReleased():
    global high
    global drawn_nodes
    global drawn_nodes_l
    global color_val
    global prev_len_nodes
    global prev_prime
    global color_inc
    global prev_prime

    prime_gap = config.prime_gap

    prime_count = 0
    colorme = color(color_val, 70, 80, 100)

    low, high = spine_math.yield_next_range(high)
    for n in range(low, high):
        node = SpinePoint(n, colorme)
        node.prime = is_prime(node.number)
        Data.nodes.append(node)
    prev_node = None
    if prime_gap:
        for node in Data.nodes:
            draw_spines(node, config.canvas_width/2.3)
            if prev_node:
                connect_nodes(prev_node, node)
                pass
            if node.prime:
                save(str(prev_prime) + "-" + str(node.number) + ".png")
                Data.nodes = []
                prev_node = None
                prev_prime = node.number
                background(0, 0, 100)
            else:
                prev_node = node


    else:
        background(0,0,100)
        # nodes list has to be reversed
        nodes_rev = list(reversed(Data.nodes))
        for node in nodes_rev:
                # if node not in drawn_nodes:
                draw_nodes(node)
                if prev_node:
                    # connect_nodes(prev_node, node)
                    pass
                prev_node = node
                # if node.prime:
                    # prime_count += 1
                # drawn_nodes_l.append(node)
                # drawn_nodes.add(node)
    # take this ratio, plug it back into the equation. For whatever reason the
    # first one is the Fibonnoci sequence
    # print(prime_count - prev_prime, len(Data.nodes) - prev_len_nodes) # has something to do with prime locations
    #save("other" + str(Data.largest_order) + ".png")
    # prev_len_nodes = len(Data.nodes)
    # prev_prime = prime_count
    color_val += color_inc
    Data.largest_order += 1

def draw_nodes(node):
    # stroke(node.colorme)
    #stroke(node.colorme)
    # plot_it(node, 0, height) # plot all
    if node.prime:
        draw_spines(node, node.number, False)
        # plot_it(node, 0, height, True)
        return True
    else:
        draw_spines(node, node.number, False)
        # plot_it(node, 0, height)
        return False

def draw_spines(node, len_spine):

    # draw_shadows(node, node.number)

    x, y = final_x_y_coords(node, len_spine)
    strokeWeight(2)
    textSize(12)
    stroke(node.colorme)
    line(Data.center_x, Data.center_y, x-2, y-2)
    node.x = x
    node.y = y
    if config.write_text:
        write_text(node, x, y + 2)

def calc_offset(node1, node2, changeval = 50):
    """
    this function doesn't work and I don't want to try to figure it out anymore
    """
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

def connect_nodes(node1, node2, offset=False):
    stroke(360, 50, 50, 50)
    strokeWeight(1)

    if offset:
        # calculate the offset for node1 to make it easier to determine direction
        node1_offset_x, node1_offset_y = calc_offset(node1, node2)
        line(node1_offset_x, node1_offset_y, node2.x, node2.y)
    else:
        line(node1.x, node1.y, node2.x, node2.y)

    ellipse(node2.x, node2.y, 5, 5)

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
    line(Data.center_x, Data.center_y, x-4, y+4)

def write_text(node, x, y, display_fraction = True):
    fill(1, 1, 0)
    textSize(10)
    text(node.number, x+3, y-3)
    low, high = spine_math.yield_next_range((Data.base**Data.largest_order)-1)
    node.update_fraction(high)

    if config.write_fraction:
        text(node.display_fraction, x + 15, y+5)

def get_updated_numer_and_denom(node):
    low, high = spine_math.yield_next_range((Data.base**Data.largest_order)-1)
    node.update_fraction(high)
    numer, denom = node.get_numer_and_denom()

    return numer, denom

def plot_it(node, y_top, y_height, no_stroke=False):

    x_left = 10
    y_bottom = y_top + y_height - 30 # last value just used for bottom padding

    numer, denom = get_updated_numer_and_denom(node)
    fraction = numer / denom

    stroke(node.colorme)
    strokeWeight(5)
    dot_color = color(0, 0, 0, 80)
    fill(dot_color)

    # no_stroke is an optional condition that can be passed in to do variable formatting
    if no_stroke == False:
        # remove outlines
        noStroke()

    if config.expansionary_plot:
        # tell us how much to move by for expansionary version
        x_inc = 5
        y_inc = 5
        ellipse(x_left + (x_inc * numer), y_bottom - (y_inc * node.number), 5, 5) # expansionary version
        if config.write_text:
            write_text(node, x_left + (x_inc * numer) + 2, y_bottom - (y_inc * node.number) - 2)

    x = fraction*(width-20) + x_left
    y = (node.number/denom)*(y_height-20)+10
    ellipse(x,y, 5, 5 ) # fit screen version
    # write_text(node, x + 5, y + 4)
    node.x = x
    node.y = y


def final_x_y_coords(node, len_r=1):
    """
    this function takes in the radian input given by node.final_location
    then finds the x and y values for the radians
    it scales the input by len_r to say how long the radius should be (default is 1)
    it then adds the center_x and center_y values to get away from (0,0) the proper amount
    """
    x = cos(node.final_location) * len_r + Data.center_x
    y = sin(node.final_location) * len_r + Data.center_y
    return x, y

def is_prime(n):
    """Returns True if n is prime."""
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return False

        i += w
        w = 6 - w

    return True
