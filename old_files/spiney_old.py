from math import tau

def convert_fraction(numerator, denominator, desired_denom):
    # converts to desired denominator
    factor = desired_denom/denominator
    numerator *= factor
    denominator *= factor
    return numerator, denominator

def sum_partial_sum(partial_sum, desired_denom = None):
    """
    this function calculates the partial sum of the passed in list of '1/n'
    fractions.
    optionally, a parameter can be set to force a certain denominator

    e.g.
    >>> partial_sum = ['1/2', '1/4', '1/8', '1/16']
    >>> sum_partial_sum(partial_sum)
    '15/16'

    >>> partial_sum = ['1/2', '1/4', '1/8', '1/16']
    >>> sum_partial_sum(partial_sum, 32)
    '30/32'

    >>> partial_sum = ['1/2', '1/4', '1/8', '1/16']
    >>> sum_partial_sum(partial_sum, 64)
    '60/64'

    honestly, this could just use the counted index of each spine,
    but just in case that pattern doesn't hold it's nice to have the function
    this also assumes that all fractions have 1 as the numerator to begin
    this allows for clean divisions regardless of base
    """
    try:
        # extracts 128 from ['1/2', '1/4', '1/64', '1/128']
        # last fraction in list, from index 2 onward (skipping '1/')
        # also removes with pop() so as to not double count
        partial_sum = [psum for psum in partial_sum]
        largest_denom = int(partial_sum.pop()[2:])
        numerator = 1

    except IndexError:
        # list is empty, happens only with 0
        return ""

    for fraction in partial_sum:
        denominator = int(fraction[2:]) # keeps only "n" from "1/n"
        numerator += int(largest_denom/denominator) # "* non_1 numerator"

    if desired_denom:
        largest_denom, numerator = convert_fraction(numerator, largest_denom, desired_denom)

    return str(numerator) + "/" + str(largest_denom)

def yield_next_range(n, base = 2, start_from_n = False):
    """
    this function returns a tuple that can go straight in a range function
    in order to call the next complete set of 'n's

    it can return the entire range
    >>> yield_next_range(16)
    (16, 32)
    >>> yield_next_range(7)
    (4, 8)

    or you can start from the n that's passed in
    >>> yield_next_range(7, start_from_n = True)
    (7, 8)

    you can also change the base
    >>> yield_next_range(10, 10)
    (10, 100)
    >>> yield_next_range(9, 10)
    (1, 10)
    >>> yield_next_range(9, 10, True)
    (9, 10)
    """
    order = 0
    while n % base**(order) != n:
        order += 1
    if start_from_n:
        # doesn't need to check for > 0 because return index 0 is replaced anyway
        return n, base**(order)
    elif order > 0:
        return base**(order-1), base**(order)
    else:
        # if starting_n is 0, just return (0,1)
        return 0, 1

def orders_for_n(n, b):
    """
    this function returns a tuple of b^(order) + b^(order) + ... + b^(order)
    that sum to variable n
    it's essentially the same as converting to a base, but instead of a value
    represented by numbers, the symbol index is listed however many times it
    ought to show up
    e.g.

    look what happens when we try 20 in base 10, we get 2 '1's back
    this is because in index 1 we want a symbol to represent the value 2
    there are no '0's, so in index 0 we want a symbol for 0
    i.e. the symbol '2' in index 1, '0' in index 0 solution: "20"
    >>> orders_for_n(20, 10)
    (1, 1)

    10 in base 10 returns a tuple with only '1' in it
    this is because index 1 should have a symbol representing the value "1"
    there are no '0's, so we need a symbol for the value "0" in the 0 index
    i.e. 1 in index 1, 0 in index 0 solution: "10"
    >>> orders_for_n(10, 10)
    (1,)

    for 9 in base 10 we get 9 '0's back.
    this is because index 0 wants a symbol for the value 9 solution: "9"
    >>> orders_for_n(9, 10)
    (0, 0, 0, 0, 0, 0, 0, 0, 0)

    for 2 in base 2, it's easy. we get 1 '1' back and no '0's
    therefore we just need a symbol for '1' in index 1 and '0' in index 0
    the solution: "10"
    >>> orders_for_n(2, 2)
    (1,)

    now we can go faster. got back 1 '0', therefore: "1"
    >>> orders_for_n(1, 2)
    (0,)

    just for fun: got back 1 '8', 1 '7', 1 '6', 1 '5', 1 '4', and 1 '2'
    therefore: "111110100"
    notice that indices 0, 1, and 3 have 0s because they didn't show up
    >>> orders_for_n(500, 2)
    (2, 4, 5, 6, 7, 8)

    Note that the order of output is reversed
    """
    orders = []
    while n > 0:
        order = 0
        while n % b**(order+1) != n:
            order += 1

        orders.append(order)
        n -= b**order
    try:
        orders.reverse()
    except TypeError:
        pass

    return tuple(orders)

def get_point(num, base = 2):
    """
    this function gathers the orders to sum b^order to get n
    it converts those numbers to the fractional coordinate and multiplies by tau
    it returns that location as a tuple

    right now this only is tested to work with base 2
    hopefully, (but likely not,) higher bases will be as easy as 2
    """
    orders = orders_for_n(num, base)

    partial_sums = ["1/" + str(base**(order+1)) for order in orders]

    final_location = 0
    for summ in partial_sums:
        final_location += (tau * eval(summ))

    return final_location, partial_sums



if __name__ == "__main__":
    import doctest
    doctest.testmod()
