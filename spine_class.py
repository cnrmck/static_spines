from __future__ import division
import spine_math

class Spine(object):
    """
    Connor of the future:
    this class is pretty cool, but there are a couple attributes that I would be
    happy to modify to better streamline it.

    Wishlist:
        Fractions
        fractionality should be managed as two integers: numer and denom
        NOT as a string (as proud as connor was about figuring it out)
        in fact, I would be shocked to find that there isn't a module
        (probably math) that can simplify fractions and has a better
        class to handle them. (Tho there is a balance between creating
        too much object overhead when working in large computation)
        display_fraction should just be a tuple of numer, denom

        Primality
        I think the primality check could be performed within this class
        (since it's an attribute of this class) rather than performed on it and fed in from
        outside. Best case, I think, would be to structure it as an optional
        parameter that runs the proper function at runtime.
        Better still would be a dict with the known primalities.
        But perhaps this has its own downsides.




    >>> from spiney import sum_partial_sum

    >>> s = Spoke(12)

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
    def __init__(self, number, colorme):
        self.number = number
        self.final_location, self.partial_sums = spiney.gen_point(self.number)
        self.fractional_location = spiney.sum_partial_sum(self.partial_sums)
        self.display_fraction = self.fractional_location
        self.colorme = colorme
        self.prime = False

    def update_fraction(self, desired_denom):
        """
        this function updates the display_fraction if its denominator does not
        match the desired_denoms
        """
        numerator, denominator = self.get_numer_and_denom()
        # finds the index of the "/" and checks against what comes after it
        if denominator !=  desired_denom:
            numer, denom = spiney.convert_fraction(numerator, denominator, desired_denom)
            self.display_fraction = str(int(numer)) + "/" + str(int(denom))
    def get_numer_and_denom(self):
        try:
            i = self.display_fraction.index("/")
            denominator = int(self.display_fraction[i+1:])
            numerator = int(self.display_fraction[:i])
            return numerator, denominator
        except ValueError:
            return 0, 1



if __name__ == '__main__':
    import doctest
    doctest.testmod()
