class Invoice(object):
    def __init__(self, *args, **kwargs):
        self.number = ''
        self.period = ''
        self.client = ''
        self.hours = ''
        self.status = ''
        self.timesheet = []
