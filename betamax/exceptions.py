class BetamaxError(Exception):
    def __init__(self, message):
        super(BetamaxError, self).__init__(message)

    def __repr__(self):
        return 'BetamaxError("%s")' % self.message
