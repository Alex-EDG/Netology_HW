class DiskException(Exception):
    code = None

    def __init__(self, code, text):
        super(DiskException, self).__init__(text)
        self.code = code

    def __str__(self):
        return "%d. %s" % (self.code, super(DiskException, self).__str__())