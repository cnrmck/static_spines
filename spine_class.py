from __future__ import division
import spine_math

class SpinePoint(object):
    """
    Connor of the future:
    this class is pretty cool, but there are a couple attributes that I would be
    happy to modify to better streamline it.

    vx and vy are vector x and vector y points (they concern themselves with
    the magnitude of the direction)

    Wishlist:
        Fractions
        fractionality should be managed as two integers: numer and denom
        NOT as a string (as proud as connor was about figuring it out)
        in fact, I would be shocked to find that there isn't a module
        (probably math) that can simplify fractions and has a better
        class to handle them. (Tho there is a balance between creating
        too much object overhead when working in large computation)
        display_fraction should just be a tuple of numer, denom

    >>> from spine_math import sum_partial_sum

    >>> s = SpinePoint(12)

    >>> s.fractional_location
    '3/16'

    >>> s.partial_sums
    ['1/8', '1/16']

    >>> sum_partial_sum(s.partial_sums)
    '3/16'

    >>> s.display_fraction
    '3/16'

    >>> s.update_fraction(64)

    >>> s.display_fraction
    '12/64'
    """
    def __init__(self, number, current_color):
        """
        initialize all the variables in the SpinePoint class.

        Arguments:
        number - an integer, e.g. -1, 0, 1, 2, etc.
        current_color - an integer to indicate the correct color for this number
        can be returned by calling the processing `color` function
        """
        self.number = number
        self.current_color = current_color
        self.final_location, self.partial_sums = spine_math.gen_point(self.number)
        self.fractional_location = spine_math.sum_partial_sum(self.partial_sums)
        self.display_fraction = self.fractional_location
        self.vector_mode = True
        self.isprime = None
        self._x = None
        self._y = None
        self.vx = None
        self.vy = None

    def __getattribute__(self, attr):
        """ custom attribute handling to lazily calculate primality """
        if attr == 'isprime' and  object.__getattribute__(self, attr) is None:
            self.isprime = self.is_prime(self.number)
            return self.isprime

        elif attr == 'x' and object.__getattribute__(self, '_x') is None:
            self._x_coords()
            return self._x

        elif attr == 'y' and object.__getattribute__(self, '_y') is None:
            self._y_coords()
            return self._y

        elif attr == 'vx' and object.__getattribute__(self, attr) is None:
            self._vx_coords()
            return self.vx

        elif attr == 'vy' and object.__getattribute__(self, attr) is None:
            self._vy_coords()
            return self.vy

        elif attr == 'x':
            if self.vector_mode is True: return self.vx
            else: return self._x

        elif attr == 'y':
            if self.vector_mode is True: return self.vy
            else: return self._y

        else:
            return object.__getattribute__(self, attr)

    def update_fraction(self, desired_denom):
        """
        this function updates the display_fraction if its denominator does not
        match the desired_denom
        """
        numerator, denominator = self.get_numer_and_denom()
        # finds the index of the "/" and checks against what comes after it
        if denominator !=  desired_denom:
            numer, denom = spine_math.convert_fraction(numerator, denominator, desired_denom)
            self.display_fraction = str(int(numer)) + "/" + str(int(denom))

    def get_numer_and_denom(self):
        try:
            i = self.display_fraction.index("/")
            denominator = int(self.display_fraction[i+1:])
            numerator = int(self.display_fraction[:i])
            return numerator, denominator
        except ValueError:
            return 0, 1

    def _x_coords(self):
        """
        this function takes in the radian input given by self.final_location
        then finds the x value for the radians it scales the input by len_r to
        say how long the radius should be (default is 1)
        """
        self._x = cos(self.final_location)

    def _y_coords(self):
        """ this function does the same as _x_coords but for y """
        self._y = sin(self.final_location)

    def _vx_coords(self):
        """this function calculates a vector from the scalar x coord"""
        self.vx = self._x * self.number

    def _vy_coords(self):
        """this function calculates a vector from the scalar y coord"""
        self.vy = self._y * self.number

    def is_prime(self, n):
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

if __name__ == '__main__':
    import doctest
    doctest.testmod()
