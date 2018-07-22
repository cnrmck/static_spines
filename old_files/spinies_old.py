from linked_list import Node
import spiney

class Spine(Node):
    """
    >>> from spiney import sum_partial_sum

    >>> s = Spine(12)

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
    def __init__(self, number):
        self.number = number
        self.final_location, self.partial_sums = spiney.get_point(self.number)
        self.fractional_location = spiney.sum_partial_sum(self.partial_sums)
        self.display_fraction = self.fractional_location

    def update_fraction(self, desired_denom):
        """
        this function updates the display_fraction if its denominator does not
        match the desired_denoms
        """
        i = self.display_fraction.index("/")
        denominator = int(self.display_fraction[i+1:])
        # finds the index of the "/" and checks against what comes after it
        if denominator !=  desired_denom:
            numerator = int(self.display_fraction[:i])
            numer, denom = spiney.convert_fraction(numerator, denominator, desired_denom)
            self.display_fraction = str(int(numer)) + "/" + str(int(denom))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
