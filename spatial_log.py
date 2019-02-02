import logging

class SpatialLog():
    def __init__(self, logger = None, ident_size = 4, log_level = 'DEBUG'):
        """
        Args:
        ident_size -- the number of spaces to indent by
        """
        if logger is None:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.getLevelName(log_level))
        else:
            self.logger = logger

        self.ident_size = ident_size
        self.ident_level = None
        self.log_format = '%(lineno)d %(levelname)-4s %(message)s'
        self.handler = logging.StreamHandler()

    def _gen_padding(self):
        """ Use the indent size to specify return a string of the appropriate padding length """
        return (self.ident_size * self.ident_level) * ' '

    def _set_logger(self, padding):
        formatter = logging.Formatter(padding + self.log_format)
        self.handler.setFormatter(formatter)
        # may need to reset the handlers here
        self.logger.addHandler(self.handler)

    def __enter__(self):
        """Increment the indent level, modify the format accordingly"""
        if self.ident_level is None:
            self.ident_level = 0
        else:
            self.ident_level += 1

        # get the padding
        padding = self._gen_padding()

        # update the format to include the proper amount of padding
        self._set_logger(padding)

        return self.logger

    def __exit__(self, type, value, traceback):
        """ Decrement the indent level, modify the format accordingly"""
        self.ident_level -= 1

        # get the padding
        padding = self._gen_padding()

        # update the format to include the proper amount of padding
        self._set_logger(padding)
