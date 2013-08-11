class VCRError(Exception):
    def __init__(self, message):
        super(VCRError, self).__init__(message)

    def __repr__(self):
        return 'VCRError("%s")' % self.message
