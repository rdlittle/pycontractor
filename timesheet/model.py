class TimeSheet(object):

    def __init__(self, data={}):
        self.date = data['date']
        self.period = data['period']
        self.description = data['description']
        self.posted = data['posted']
        self.paid = data['paid']
        self.invoice = data['invoice']
